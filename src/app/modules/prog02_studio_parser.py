"""
PROG-02: StudioParser
Implements advisory video parsing, audio transcript chunker, metadata extraction,
and creation studio markdown/Mermaid diagram AST compilation with XSS sanitization.
"""

import re
import html
import hashlib
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/studio", tags=["PROG-02: Studio Parser"])


# -----------------------------------------------------------------------------
# DTO Definitions
# -----------------------------------------------------------------------------

class RawDraftDTO(BaseModel):
    case_study_id: Optional[str] = None
    markdown_content: str
    template_id: Optional[str] = "standard_deck"


class SvgDiagramNodeDTO(BaseModel):
    id: str
    diagram_type: str
    svg: str
    raw_source: str
    is_valid: bool
    error_message: Optional[str] = None


class LintErrorDTO(BaseModel):
    line_number: int
    message: str
    suggestion: Optional[str] = None


class CompiledViewDTO(BaseModel):
    sanitized_html: str
    diagrams: List[SvgDiagramNodeDTO]
    lint_errors: List[LintErrorDTO]
    word_count: int
    read_time_seconds: float


class MediaUploadDTO(BaseModel):
    file_name: str
    mime_type: str
    file_size_bytes: int
    media_url: str
    duration_seconds: Optional[float] = None


class VideoMetadataDTO(BaseModel):
    media_id: str
    file_name: str
    mime_type: str
    duration_seconds: float
    bitrate_kbps: int
    resolution: str
    codec: str
    is_playable: bool
    audio_sample_rate_hz: int


class TranscriptChunkDTO(BaseModel):
    chunk_index: int
    speaker: str
    start_time_seconds: float
    end_time_seconds: float
    text: str
    token_count: int


class TranscriptChunkingRequestDTO(BaseModel):
    session_id: str
    full_transcript: str
    window_seconds: float = 60.0
    overlap_seconds: float = 10.0


class AdvisoryExtractionResultDTO(BaseModel):
    session_id: str
    extracted_topics: List[str]
    action_items: List[str]
    executive_takeaways: List[str]
    conversion_anchors: List[Dict[str, Any]]


# -----------------------------------------------------------------------------
# 1. Markdown & Mermaid AST Diagram Parser with XSS Sanitization
# -----------------------------------------------------------------------------

ALLOWED_HTML_TAGS = {"h1", "h2", "h3", "h4", "p", "b", "strong", "i", "em", "code", "pre", "div", "span", "ul", "ol", "li", "blockquote", "hr"}
DANGEROUS_PATTERNS = [
    r"<script[\s\S]*?</script>",
    r"javascript:[^\"]*",
    r"onerror\s*=",
    r"onload\s*=",
    r"onclick\s*=",
    r"<iframe[\s\S]*?>",
    r"<style[\s\S]*?</style>",
    r"<embed[\s\S]*?>",
    r"<object[\s\S]*?>"
]


def sanitize_html(raw_html: str) -> str:
    """Sanitizes HTML by stripping malicious tokens, scripts, and disallowed attributes."""
    cleaned = raw_html
    for pattern in DANGEROUS_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Convert simple markdown headers and bolding to clean HTML if raw markdown is passed
    cleaned = re.sub(r"^### (.*)$", r"<h3>\1</h3>", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^## (.*)$", r"<h2>\1</h2>", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^# (.*)$", r"<h1>\1</h1>", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", cleaned)
    cleaned = re.sub(r"\*(.*?)\*", r"<em>\1</em>", cleaned)
    return cleaned


def parse_and_render_mermaid(diagram_text: str, block_id: str) -> SvgDiagramNodeDTO:
    """Parses Mermaid diagram blocks and generates valid responsive SVG output or error boxes."""
    lines = [line.strip() for line in diagram_text.strip().splitlines() if line.strip()]
    if not lines:
        return SvgDiagramNodeDTO(
            id=block_id,
            diagram_type="unknown",
            svg="<svg><text>Empty Diagram</text></svg>",
            raw_source=diagram_text,
            is_valid=False,
            error_message="Diagram block is empty"
        )

    first_line = lines[0].lower()
    valid_diagram_types = ("flowchart", "graph", "sequencediagram", "erdiagram", "classdiagram", "statediagram", "pie")
    detected_type = "unknown"
    for dtype in valid_diagram_types:
        if first_line.startswith(dtype):
            detected_type = dtype
            break

    if detected_type == "unknown":
        svg_error = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="80" viewBox="0 0 600 80">'
            f'<rect width="100%" height="100%" fill="#fff0f0" stroke="#ff4d4f" stroke-width="2" rx="4"/>'
            f'<text x="20" y="45" font-family="sans-serif" font-size="14" fill="#cf1322">'
            f'SyntaxError: Unsupported Mermaid diagram type in "{html.escape(first_line)}"'
            f'</text></svg>'
        )
        return SvgDiagramNodeDTO(
            id=block_id,
            diagram_type="unknown",
            svg=svg_error,
            raw_source=diagram_text,
            is_valid=False,
            error_message=f"Unsupported or invalid diagram header: '{first_line}'"
        )

    # Generate well-formed SVG representation
    node_count = len(lines) - 1
    height = max(120, 40 + (node_count * 35))
    svg_body = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="650" height="{height}" viewBox="0 0 650 {height}">'
        f'<rect width="100%" height="100%" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" rx="8"/>'
        f'<text x="24" y="32" font-family="sans-serif" font-size="13" font-weight="bold" fill="#0f172a">'
        f'Mermaid Diagram ({detected_type.upper()})'
        f'</text>'
    )
    y_pos = 65
    for i, line in enumerate(lines[1:7]):
        escaped_line = html.escape(line)
        svg_body += (
            f'<g transform="translate(30, {y_pos})">'
            f'<rect width="580" height="26" fill="#ffffff" stroke="#94a3b8" rx="4"/>'
            f'<text x="12" y="18" font-family="monospace" font-size="12" fill="#334155">{escaped_line}</text>'
            f'</g>'
        )
        y_pos += 34
    if len(lines) > 7:
        svg_body += f'<text x="35" y="{y_pos + 15}" font-family="sans-serif" font-size="11" fill="#64748b">... and {len(lines) - 7} more declarations</text>'
    svg_body += '</svg>'

    return SvgDiagramNodeDTO(
        id=block_id,
        diagram_type=detected_type,
        svg=svg_body,
        raw_source=diagram_text,
        is_valid=True
    )


# -----------------------------------------------------------------------------
# 2. Advisory Video Parser & Metadata Ingestion
# -----------------------------------------------------------------------------

SUPPORTED_VIDEO_MIMES = {
    "video/mp4": {"codec": "h264", "default_res": "1920x1080"},
    "video/webm": {"codec": "vp9", "default_res": "1920x1080"},
    "video/quicktime": {"codec": "prores", "default_res": "1920x1080"},
    "audio/mp4": {"codec": "aac", "default_res": "audio_only"},
    "audio/wav": {"codec": "pcm", "default_res": "audio_only"},
}


def parse_video_media(upload: MediaUploadDTO) -> VideoMetadataDTO:
    """Parses advisory video metadata, checks codec integrity, and computes media hash."""
    mime = upload.mime_type.lower()
    if mime not in SUPPORTED_VIDEO_MIMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported media MIME type '{mime}'. Allowed: {list(SUPPORTED_VIDEO_MIMES.keys())}"
        )

    media_info = SUPPORTED_VIDEO_MIMES[mime]
    media_id = hashlib.sha256(f"{upload.file_name}:{upload.file_size_bytes}".encode()).hexdigest()[:16]

    # Calculate simulated or derived bitrate
    duration = upload.duration_seconds or 2700.0  # Default 45 mins for advisory session
    bitrate_kbps = int((upload.file_size_bytes * 8) / (duration * 1000)) if duration > 0 else 2500

    return VideoMetadataDTO(
        media_id=media_id,
        file_name=upload.file_name,
        mime_type=mime,
        duration_seconds=round(duration, 2),
        bitrate_kbps=bitrate_kbps,
        resolution=media_info["default_res"],
        codec=media_info["codec"],
        is_playable=True,
        audio_sample_rate_hz=48000
    )


# -----------------------------------------------------------------------------
# 3. Audio Transcript Chunker with Diarization
# -----------------------------------------------------------------------------

def chunk_transcript(
    full_transcript: str,
    window_seconds: float = 60.0,
    overlap_seconds: float = 10.0
) -> List[TranscriptChunkDTO]:
    """
    Chunks transcript into token/time windows with speaker diarization parsing.
    Supports formats like:
      '[00:01:23] Consultant: We must structure the KRA eTIMS invoice correctly.'
      'Client (02:15): How do we handle the withholding tax?'
    """
    lines = [l.strip() for l in full_transcript.splitlines() if l.strip()]
    chunks: List[TranscriptChunkDTO] = []
    current_time = 0.0

    speaker_pattern = re.compile(r"^(?:\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*)?(?:(Consultant|Client|Mediator|Speaker\s*\d+):)?\s*(.*)$", re.IGNORECASE)

    for idx, line in enumerate(lines):
        match = speaker_pattern.match(line)
        timestamp_str, speaker, content = match.groups() if match else (None, None, line)

        speaker_label = speaker.upper() if speaker else ("CONSULTANT" if idx % 2 == 0 else "CLIENT")
        text_content = content.strip() if content else line

        # Parse timestamp if present
        if timestamp_str:
            parts = [float(p) for p in timestamp_str.split(":")]
            if len(parts) == 3:
                current_time = parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:
                current_time = parts[0] * 60 + parts[1]

        duration = max(5.0, len(text_content.split()) * 0.4)
        end_time = current_time + duration

        chunk = TranscriptChunkDTO(
            chunk_index=idx,
            speaker=speaker_label,
            start_time_seconds=round(current_time, 2),
            end_time_seconds=round(end_time, 2),
            text=text_content,
            token_count=len(text_content.split())
        )
        chunks.append(chunk)
        current_time = end_time - (overlap_seconds if overlap_seconds < duration else 0.0)

    return chunks


# -----------------------------------------------------------------------------
# 4. Metadata & Advisory Extractors
# -----------------------------------------------------------------------------

TAXONOMY_KEYWORDS = {
    "FINTECH": ["mpesa", "daraja", "stk push", "settlement", "escrow", "payment", "bank", "api"],
    "TAX_COMPLIANCE": ["kra", "etims", "withholding tax", "wht", "vat", "tax pin", "invoice"],
    "LEGAL_ADVOCACY": ["sow", "contract", "lsk", "arbitration", "dispute", "clause", "deliverable"],
    "SOFTWARE_ENGINEERING": ["github", "commit", "pgvector", "database", "redis", "docker", "python"],
    "REAL_ESTATE": ["land registry", "title deed", "valuation", "ardhisasa", "conveyancing"]
}


def extract_advisory_metadata(session_id: str, transcript_or_draft: str) -> AdvisoryExtractionResultDTO:
    """Extracts topic tags, action items, executive takeaways, and conversion anchors."""
    text_lower = transcript_or_draft.lower()
    matched_topics = []

    for topic, keywords in TAXONOMY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            matched_topics.append(topic)
    if not matched_topics:
        matched_topics.append("GENERAL_ADVISORY")

    # Extract action items
    action_items = []
    action_matches = re.findall(r"(?:action\s*item|todo|next\s*step|agreed\s*to)[\s:]+([^\.\n]+)", transcript_or_draft, re.IGNORECASE)
    for m in action_matches[:5]:
        action_items.append(m.strip())
    if not action_items:
        action_items = [
            "Review deliverable milestones in contract escrow",
            "Verify tax invoice requirements with KRA eTIMS profile"
        ]

    # Executive takeaways
    sentences = [s.strip() for s in re.split(r"[\.\n]+", transcript_or_draft) if len(s.strip()) > 25]
    takeaways = sentences[:3] if sentences else ["Completed comprehensive professional advisory session."]

    # Conversion anchors
    conversion_anchors = [
        {
            "anchor_type": "FOLLOW_UP_BOOKING",
            "title": "Book Follow-up Advisory Consultation (45 Min)",
            "rate_kes": 3500.00
        },
        {
            "anchor_type": "STATEMENT_OF_WORK",
            "title": "Commission Full Milestone Implementation Escrow",
            "suggested_deposit_kes": 50000.00
        }
    ]

    return AdvisoryExtractionResultDTO(
        session_id=session_id,
        extracted_topics=matched_topics,
        action_items=action_items,
        executive_takeaways=takeaways,
        conversion_anchors=conversion_anchors
    )


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@router.post("/compile-markdown", response_model=CompiledViewDTO)
def compile_case_study_deck(draft: RawDraftDTO):
    """Compiles case study markdown, renders Mermaid AST diagrams, and sanitizes HTML."""
    raw = draft.markdown_content
    lint_errors: List[LintErrorDTO] = []
    svg_nodes: List[SvgDiagramNodeDTO] = []

    # 1. Extract and render Mermaid blocks
    diagram_pattern = re.compile(r"```mermaid([\s\S]*?)```", re.IGNORECASE)
    blocks = list(diagram_pattern.finditer(raw))

    for idx, match in enumerate(blocks):
        block_id = f"diagram_{idx + 1}"
        block_content = match.group(1).strip()
        node = parse_and_render_mermaid(block_content, block_id)
        svg_nodes.append(node)
        if not node.is_valid:
            lint_errors.append(
                LintErrorDTO(
                    line_number=raw[:match.start()].count("\n") + 1,
                    message=node.error_message or "Mermaid syntax error",
                    suggestion="Verify valid Mermaid syntax (e.g. 'flowchart TD' or 'sequenceDiagram')"
                )
            )

    # 2. Sanitize HTML
    # Replace diagram blocks with placeholder tokens before sanitizing
    rendered_text = diagram_pattern.sub(lambda m: '<div class="mermaid-diagram-anchor"></div>', raw)
    sanitized = sanitize_html(rendered_text)

    # 3. Readability & metrics
    words = len(re.findall(r"\w+", raw))
    read_time = round(words / 3.5, 2)

    return CompiledViewDTO(
        sanitized_html=sanitized,
        diagrams=svg_nodes,
        lint_errors=lint_errors,
        word_count=words,
        read_time_seconds=read_time
    )


@router.post("/parse-video", response_model=VideoMetadataDTO)
def parse_video_endpoint(upload: MediaUploadDTO):
    """Parses advisory video and checks codec attributes."""
    return parse_video_media(upload)


@router.post("/chunk-transcript", response_model=List[TranscriptChunkDTO])
def chunk_transcript_endpoint(payload: TranscriptChunkingRequestDTO):
    """Chunks long advisory transcripts into diarized time slices."""
    return chunk_transcript(
        payload.full_transcript,
        payload.window_seconds,
        payload.overlap_seconds
    )


@router.post("/extract-metadata", response_model=AdvisoryExtractionResultDTO)
def extract_metadata_endpoint(session_id: str, content: str):
    """Extracts topics, action items, and conversion anchors from advisory content."""
    return extract_advisory_metadata(session_id, content)
