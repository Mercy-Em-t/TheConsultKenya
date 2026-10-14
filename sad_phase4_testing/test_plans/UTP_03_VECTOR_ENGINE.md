# UNIT TEST PLAN: UTP-03 TWO-PASS AI VECTOR ENGINE (PROG-03)
**System:** Consult Kenya  
**Module Target:** `src/app/modules/prog03_vector_engine.py`  
**Test Objective:** Validate the two-pass retrieval architecture: Pass 1 fast cosine similarity candidate selection via pgvector HNSW index, Pass 2 reciprocal rank fusion & contextual reranking, handling arbitrary query vectors, zero matches, and high dimension integrity.  
**Test Approach:** Hybrid (Black-Box Top-K Retrieval Precision + White-Box HNSW & Cosine Math Boundary Checks).  
**Minimum Required Test Cases:** 8 (Defined: 8).  

---

## Test Cases Specification & Execution Matrix

| Test Case ID | Test Category | Objective & Input Parameters | Expected Result | Observed Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UTP03-01** | Black-Box (Valid) | Query: `"Corporate tax compliance KRA eTIMS withholding tax"`, Top-K: 5. | Returns 5 consultant profiles ranked by relevance score ($> 0.82$ cosine similarity). Response time $< 45\text{ms}$. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-02** | Black-Box (Zero Match) | Query with unrelated gibberish: `"zxqwy123987!#@$%&"`. | Low similarity scores below confidence cutoff ($< 0.35$). Returns empty list or suggested broad categories. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-03** | Black-Box (Boundary) | Request Top-K with $K=1$ (minimum boundary) vs $K=50$ (maximum permitted API boundary) vs $K=51$ (overflow). | $K=1$: Exactly 1 item returned. $K=50$: Exactly 50 items returned. $K=51$: HTTP 422 ("Top-K must be between 1 and 50"). | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-04** | Black-Box (Malformed) | Query vector array with 255 dimensions or 257 dimensions (Mismatch against 256-dim standard). | Dimensionality validation guard raises `InvalidVectorDimensionError`. Returns HTTP 400. Zero DB crash. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-05** | White-Box (Path) | Two-pass fusion path: Pass 1 returns 20 items from HNSW index, Pass 2 re-ranks using normalised CAS, geo boost and freshness decay (PROG-03 spec). | Composite score $= 0.35 \cdot \cos + 0.40 \cdot (CAS/1000) + 0.15 \cdot geo + 0.10 \cdot e^{-0.05 \cdot days}$, sorted descending; max 2 cards per author in top 20. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-06** | White-Box (Branch) | All candidates have identical cosine similarity (Tie-breaker branch). | Secondary sorting rule (Total completed verified sessions, then registration timestamp) breaks ties deterministically. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-07** | White-Box (Condition) | Vector embedding contains `NaN` or `Infinity` floating-point values. | Sanitization check detects `isnan()` / `isinf()`, raises `VectorValueAnomalyError`. | _Pending — not yet executed_ | **NOT RUN** |
| **TC-UTP03-08** | White-Box (Mutation) | Empty query string (`""` or `"   "`). | Fast-path interceptor returns bad request error before invoking downstream vector embedding model. | _Pending — not yet executed_ | **NOT RUN** |

---

## Pass / Fail Summary
- **Execution status:** NOT RUN. This plan has been designed but not yet executed.
- **Observed results:** to be recorded only from actual execution, with a link to the test run / CI job as evidence.
- **Coverage:** to be measured with `pytest --cov` when executed. No coverage figure has been measured yet.

> [!NOTE]
> An earlier version of this file showed observed results and coverage figures that were never measured. They were removed on 13 Oct 2026 (CR-2026-002).
