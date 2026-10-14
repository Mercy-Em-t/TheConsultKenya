"""
PROG-03: TwoPassRecommendationAndCASRankingEngine
Executes Two-Pass AI Vector Search & Semantic Matching:
Pass 1: Approximate Nearest Neighbor (ANN) 256-dim vector cosine similarity retrieval.
Pass 2: Creator Authority Score (CAS) weighting, Kenyan geo-boost, freshness decay, and anti-saturation diversity filtering.
"""

import math
import time
import base64
import datetime
from typing import List, Dict, Optional, Any
import numpy as np
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.app.core.config import settings
from src.app.core.database import (
    get_db,
    get_redis_client,
    CaseStudyDeck,
    ConsultantProfile,
    User
)

router = APIRouter(prefix="/discovery", tags=["PROG-03: Vector Recommendation Engine"])


# -----------------------------------------------------------------------------
# DTO Definitions
# -----------------------------------------------------------------------------

class ClientSessionContextDTO(BaseModel):
    user_id: Optional[str] = None
    query_text: Optional[str] = None
    query_embedding: Optional[List[float]] = None
    geo_tag: str = Field(default="KE", description="Kenyan/East African localized region code")
    mode_preference: str = Field(default="VISUAL_FIRST", description="VISUAL_FIRST or TECHNICAL_DEEP_DIVE")
    limit: int = Field(default=20, ge=1, le=50)


class CaseStudyCardDTO(BaseModel):
    case_study_id: str
    author_id: str
    author_name: Optional[str] = None
    author_handle: Optional[str] = None
    case_title: str
    slug: str
    executive_summary: str
    target_region: str
    cosine_similarity: float
    author_cas: float
    composite_score: float
    published_at: Optional[datetime.datetime] = None
    conversion_anchor: Optional[Dict[str, Any]] = None


class FeedResponseDTO(BaseModel):
    cards: List[CaseStudyCardDTO]
    total_candidates_retrieved: int
    next_cursor: Optional[str] = None
    telemetry_latency_ms: float


class IndexCaseStudyDTO(BaseModel):
    author_id: str
    case_title: str
    executive_summary: str
    content_blueprint: Dict[str, Any] = Field(default_factory=dict)
    conversion_anchor: Dict[str, Any] = Field(default_factory=dict)
    target_region: str = "KE"
    custom_embedding: Optional[List[float]] = None


# -----------------------------------------------------------------------------
# Vector Generation & Math Helpers (256-dimensional normalized vectors)
# -----------------------------------------------------------------------------

def generate_text_embedding_256(text_content: str) -> List[float]:
    """
    Generates a normalized 256-dimensional dense embedding vector from text.
    Uses deterministic token-hash projections with L2 normalization.
    """
    dim = 256
    vector = np.zeros(dim, dtype=np.float32)
    tokens = text_content.lower().split()
    if not tokens:
        vector[0] = 1.0
        return vector.tolist()

    for token in tokens:
        import hashlib
        # Hash token into 2 indices and weights
        h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
        idx1 = h % dim
        idx2 = (h >> 16) % dim
        weight = 1.0 + (len(token) / 10.0)
        vector[idx1] += weight
        vector[idx2] -= (weight * 0.5)

    # L2 normalize
    norm = np.linalg.norm(vector)
    if norm > 1e-9:
        vector = vector / norm
    else:
        vector[0] = 1.0

    return vector.tolist()


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes cosine similarity between two vectors."""
    a = np.array(vec_a, dtype=np.float32)
    b = np.array(vec_b, dtype=np.float32)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a < 1e-9 or norm_b < 1e-9:
        return 0.0
    return float(dot / (norm_a * norm_b))


# -----------------------------------------------------------------------------
# Two-Pass Recommendation Algorithm Core
# -----------------------------------------------------------------------------

def execute_two_pass_recommendation(
    context: ClientSessionContextDTO,
    db: Session
) -> FeedResponseDTO:
    """
    Executes the Two-Pass feed generation algorithm:
    Pass 1: Retrieve top 200 candidates by vector similarity.
    Pass 2: Score with CAS, Kenyan geo-boost, freshness decay, and anti-saturation diversity filter.
    """
    start_time = time.time()
    redis_client = get_redis_client()

    # 1. Resolve Query Embedding
    query_vec = context.query_embedding
    if not query_vec:
        text_to_embed = context.query_text or "Kenya professional consulting advisory fintech tax engineering legal"
        query_vec = generate_text_embedding_256(text_to_embed)

    # 2. PASS 1: Candidate Retrieval (ANN Vector Cosine Search)
    # Check if native pgvector is available; fallback to in-memory cosine ranking over published decks
    candidates: List[Dict[str, Any]] = []

    # Query published decks from database
    published_decks = db.query(CaseStudyDeck).filter(
        CaseStudyDeck.publication_status == "PUBLISHED"
    ).all()

    for deck in published_decks:
        embedding = deck.semantic_embedding
        sim = cosine_similarity(query_vec, embedding) if embedding else 0.5
        candidates.append({
            "deck": deck,
            "cosine_similarity": max(0.0, min(1.0, sim))
        })

    # Sort candidates by raw cosine similarity and pick top 200
    candidates.sort(key=lambda x: x["cosine_similarity"], reverse=True)
    candidates = candidates[:200]

    # 3. Retrieve pre-computed CAS scores from Redis or ConsultantProfiles
    author_ids = list({c["deck"].author_id for c in candidates})
    cas_cache = {}
    for aid in author_ids:
        cached_cas = redis_client.get(f"cas_score:{aid}")
        if cached_cas is not None:
            try:
                cas_cache[aid] = float(cached_cas.decode() if isinstance(cached_cas, bytes) else cached_cas)
            except Exception:
                cas_cache[aid] = 100.0
        else:
            profile = db.query(ConsultantProfile).filter(ConsultantProfile.consultant_id == aid).first()
            score = float(profile.cas_score) if profile else 100.0
            cas_cache[aid] = score
            redis_client.set(f"cas_score:{aid}", str(score), ex=3600)

    # 4. PASS 2: Heavy Business Re-Ranking
    now = datetime.datetime.utcnow()
    scored_candidates = []

    for item in candidates:
        deck: CaseStudyDeck = item["deck"]
        sim: float = item["cosine_similarity"]
        author_cas: float = cas_cache.get(deck.author_id, 100.0)

        # Normalize CAS (0 to 1000 scale -> 0.0 to 1.0)
        norm_cas = max(0.0, min(1.0, author_cas / 1000.0))

        # Geo-Boost: 25% boost for Kenyan/East African localized content
        geo_boost = 1.25 if deck.target_region == context.geo_tag else 1.0

        # Freshness Decay: exp(-0.05 * days_since_published)
        pub_date = deck.published_at or deck.created_at
        if pub_date.tzinfo is not None:
            pub_date = pub_date.replace(tzinfo=None)
        days_since = max(0.0, (now - pub_date).total_seconds() / 86400.0)
        freshness_decay = math.exp(-0.05 * days_since)

        # Composite Scoring Model
        composite_score = (
            (sim * 0.35) +
            (norm_cas * 0.40) +
            (geo_boost * 0.15) +
            (freshness_decay * 0.10)
        )

        author_profile = deck.author
        author_user = author_profile.user if author_profile else None

        card_dto = CaseStudyCardDTO(
            case_study_id=deck.case_study_id,
            author_id=deck.author_id,
            author_name=author_user.full_name if author_user else "KenyaConsult Expert",
            author_handle=author_profile.public_handle if author_profile else None,
            case_title=deck.case_title,
            slug=deck.slug,
            executive_summary=deck.executive_summary,
            target_region=deck.target_region,
            cosine_similarity=round(sim, 4),
            author_cas=round(author_cas, 2),
            composite_score=round(composite_score, 4),
            published_at=deck.published_at,
            conversion_anchor=deck.conversion_anchor_json
        )
        scored_candidates.append(card_dto)

    # Sort descending by composite score
    scored_candidates.sort(key=lambda x: x.composite_score, reverse=True)

    # 5. Diversity & Anti-Saturation Filter (Max 2 cards per author in top 20)
    top_feed: List[CaseStudyCardDTO] = []
    author_counts: Dict[str, int] = {}
    target_limit = min(context.limit, 20)

    for card in scored_candidates:
        count = author_counts.get(card.author_id, 0)
        if count < 2:
            top_feed.append(card)
            author_counts[card.author_id] = count + 1
        if len(top_feed) >= target_limit:
            break

    # Next page cursor
    cursor = None
    if top_feed:
        last_id = top_feed[-1].case_study_id
        cursor = base64.b64encode(f"cursor:{last_id}:{time.time()}".encode()).decode()

    latency_ms = round((time.time() - start_time) * 1000.0, 2)

    return FeedResponseDTO(
        cards=top_feed,
        total_candidates_retrieved=len(candidates),
        next_cursor=cursor,
        telemetry_latency_ms=latency_ms
    )


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/feed", response_model=FeedResponseDTO)
def get_two_pass_feed(
    context: ClientSessionContextDTO,
    db: Session = Depends(get_db)
):
    """Generates two-pass personalized discovery feed with CAS weighting and anti-saturation."""
    return execute_two_pass_recommendation(context, db)


@router.post("/index-case-study")
def index_case_study(
    payload: IndexCaseStudyDTO,
    db: Session = Depends(get_db)
):
    """Indexes a newly published case study deck with 256-dim embedding vector."""
    author = db.query(ConsultantProfile).filter(ConsultantProfile.consultant_id == payload.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author consultant profile not found")

    embedding = payload.custom_embedding
    if not embedding:
        content_for_embedding = f"{payload.case_title} {payload.executive_summary}"
        embedding = generate_text_embedding_256(content_for_embedding)

    slug = payload.case_title.lower().replace(" ", "-")[:80] + f"-{int(time.time())}"

    deck = CaseStudyDeck(
        author_id=payload.author_id,
        case_title=payload.case_title,
        slug=slug,
        executive_summary=payload.executive_summary,
        content_blueprint_json=payload.content_blueprint,
        conversion_anchor_json=payload.conversion_anchor,
        semantic_embedding=embedding,
        publication_status="PUBLISHED",
        target_region=payload.target_region,
        published_at=datetime.datetime.utcnow()
    )
    db.add(deck)
    db.commit()
    db.refresh(deck)

    return {
        "status": "INDEXED",
        "case_study_id": deck.case_study_id,
        "slug": deck.slug,
        "embedding_dimensions": len(embedding)
    }
