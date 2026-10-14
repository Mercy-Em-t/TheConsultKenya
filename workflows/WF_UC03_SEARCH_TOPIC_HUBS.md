# UC-03: Search & Filter Topic Hubs
*Diagram Type: Data Flow Diagram (DFD Level 1 - Semantic Query Pipeline)*

Specifies how user search tokens flow into dense vector embeddings, topic filtering, and ranked card retrieval.

```mermaid
flowchart LR
    Client((Client)) -->|1: Raw Search Query + Filter Tags| SearchService[Process Search Request]
    
    subgraph Data Stores
        TopicDB[(Topic Hubs & Category Store)]
        VectorDB[(Vector Embedding Index)]
        ConsultantDB[(Verified Consultant DB)]
    end
    
    SearchService -->|2: Query String| Embedder[Semantic Text Embedder]
    Embedder -->|3: 128D Dense Vector| VectorSearch[Cosine Vector Matcher]
    
    VectorDB -->|Vectors & Card Metadata| VectorSearch
    VectorSearch -->|4: Top Semantic Matches| Ranker[Filter & Ranking Engine]
    
    TopicDB -->|Category Taxonomies| Ranker
    ConsultantDB -->|CAS Weights & Badges| Ranker
    
    Ranker -->|5: Ranked Result Set| ResultFormatter[Format Multi-Hub Response]
    ResultFormatter -->|6: Bento Topic Grid + Consultant Profiles| Client
    
    Ranker -.->|Zero Matches Detected| SuggestionEngine[Generate Nearest Topic Suggestions]
    SuggestionEngine -.->|Alternate Topic Chips| ResultFormatter
```
