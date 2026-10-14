# UNIT TEST PLAN: UTP-02 ADVISORY MEDIA STUDIO PARSER (PROG-02)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog02_studio_parser.py`  
**Test Objective:** Ensure video/audio uploads are parsed into clean transcript chunks, speech timestamps are aligned, video resolution/bitrate conform to CDN constraints, and malformed/oversized files are rejected gracefully.  
**Test Approach:** Hybrid (Black-Box Boundary/MIME Validation + White-Box Segment Splitter Branch Analysis).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP02-01** | Black-Box (Valid) | MP4 video container, H.264 video, AAC audio, duration 180s, file size 45MB. | HTTP 200 OK. Audio track extracted to MP3, Whisper stub produces timestamped JSON chunks, DB record created in `MediaAssets`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-02** | Black-Box (Boundary) | Video duration exactly 600s (10.0 min max allowed limit) vs 601s. | 600s: Processed successfully. 601s: Rejected with HTTP 400 ("Advisory video exceeds maximum permitted limit of 10 minutes"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-03** | Black-Box (Malformed) | Binary file with extension `.mp4` but containing raw text ASCII (`"Not a real video stream"`). | FFprobe header inspection detects invalid container header. Raises `InvalidMediaContainerError`. HTTP 415 Unsupported Media Type. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-04** | Black-Box (Nonsense) | Upload file with size 0 bytes (Empty file). | Detected at file streaming barrier. Returns HTTP 400 ("Uploaded media payload cannot be zero bytes"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-05** | White-Box (Path) | Audio with extended silence (>30 seconds of quiet room audio). | Silence detection branch splits chunks cleanly without hallucinating empty text or dividing into infinite micro-chunks. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-06** | White-Box (Branch) | Transcription returns mixed Swahili and English words ("Sheng" legal and tax consultation jargon). | NLP chunker normalizes Swahili terms, preserves token boundaries, and assigns correct language metadata tag `sw-KE/en-KE`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-07** | White-Box (Condition) | Storage upload failure (Mock S3/Wasabi bucket throws `ConnectionResetError` mid-stream). | Circuit breaker catches storage exception, marks record `TRANSCODE_FAILED`, triggers rollback, deletes local temp files. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP02-08** | White-Box (Mutation) | Corrupted UTF-8 characters in Whisper transcript payload. | Text cleaner sanitizes Unicode surrogates, preserves emojis and standard punctuation, writes clean UTF-8 string to DB. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
