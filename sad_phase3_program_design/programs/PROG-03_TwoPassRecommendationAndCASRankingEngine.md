# Program Specification: TwoPassRecommendationAndCASRankingEngine
**Program ID:** `PROG-03` | **Module Type:** Algorithmic & AI Inference Service
**Language / Framework:** `Python 3.12 / NumPy / pgvector / Redis`

### Description
Executes the core algorithmic feed personalization: Pass 1 retrieves candidate case studies via Approximate Nearest Neighbor (ANN) vector cosine search; Pass 2 re-ranks candidates using weighted Creator Authority Scores (CAS) and anti-saturation diversity filters.

### Systems Design Characteristics
- **Cohesion Type:** Functional Cohesion (Mathematical vector dot-product and scoring pipeline)
- **Coupling Level:** Data Coupling (Input context vector, returns ranked list)
- **Fan-In:** `2` (High reuse by upstream callers)
- **Fan-Out:** `3` (Optimal controlled subordinate delegations)

### Associated Events & Triggers
- `EVT-FEED-REQUEST: Client initiates discovery feed query.`
- `EVT-HOURLY-CRON: Batch daemon recalculates creator CAS multipliers.`

### Program Input Parameters
| Input Parameter | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`client_context`** | `ClientSessionContextDTO` | user_id, session_vector, geo_region, mode_preference |

### Program Output Returns
| Output Return | Data Transfer Object (DTO) | Internal Elements |
| :--- | :--- | :--- |
| **`ranked_feed`** | `FeedResponseDTO` | top_20_cards, next_cursor, ranking_telemetry_id |

### Detailed Algorithmic Pseudocode
```python
FUNCTION GenerateTwoPassFeed(client_context: ClientContext) -> FeedResponse:
    INPUT: client_context (user_id, query_embedding, geo_tag)
    OUTPUT: FeedResponse (card_list, next_page_token)

    // PASS 1: Candidate Retrieval (ANN Vector Cosine Search)
    // Query top 200 candidates from pgvector using HNSW index
    candidates = Database.pgvector.CosineSimilarityQuery(
        vector=client_context.query_embedding,
        limit=200,
        filter_status="PUBLISHED"
    )

    // Retrieve pre-computed CAS scores from Redis in single MGET
    author_ids = ExtractUniqueAuthorIDs(candidates)
    cas_weights = Redis.MGet("cas_score:" + author_id FOR author_id IN author_ids)

    scored_candidates = []

    // PASS 2: Heavy Business Re-Ranking
    FOR EACH card IN candidates:
        author_cas = cas_weights.Get(card.author_id, DEFAULT=100.0) // 0 to 1000 scale
        norm_cas = author_cas / 1000.0
        
        geo_boost = 1.0
        IF card.target_region == client_context.geo_tag THEN
            geo_boost = 1.25 // 25% boost for Kenyan/East African localized content
        END IF

        freshness_decay = Math.Exp(-0.05 * DaysSince(card.published_at))

        // Composite Scoring Model
        composite_score = (card.cosine_similarity * 0.35) + 
                          (norm_cas * 0.40) + 
                          (geo_boost * 0.15) + 
                          (freshness_decay * 0.10)

        scored_candidates.Append(card, composite_score)
    END FOR

    // Sort descending by composite score
    SortDescending(scored_candidates, KEY=composite_score)

    // Diversity & Anti-Saturation Filter (Max 2 cards per author in top 20)
    top_20_feed = []
    author_counts = Map()

    FOR EACH item IN scored_candidates:
        author_count = author_counts.Get(item.author_id, 0)
        IF author_count < 2 THEN
            top_20_feed.Append(item.card)
            author_counts.Set(item.author_id, author_count + 1)
        END IF
        IF Length(top_20_feed) == 20 THEN
            BREAK
        END IF
    END FOR

    RETURN FeedResponse(cards=top_20_feed, cursor=GenerateCursor(top_20_feed.Last()))
END FUNCTION
```
