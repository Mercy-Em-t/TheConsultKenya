# UC-18: Personalize Two-Pass Discovery Feed
*Diagram Type: Data Flow Diagram (DFD Level 1 - Two-Pass Feed Recommendation Engine)*

Details the two-pass retrieval architecture: Pass 1 fast vector candidate generation ($<50\text{ms}$) followed by Pass 2 heavy business ranking with East Africa weighting.

```mermaid
flowchart TD
    Client((Active Viewer)) -->|1: Request Feed Generation| FeedOrchestrator[Feed Orchestration Service]
    
    subgraph Data Stores
        UserVectorDB[(User Interaction History & Preferences)]
        PostVectorDB[(Case Study 128D Embedding Index)]
        CASDB[(Creator Authority Scores DB)]
        GeoDB[(Regional Context & Location Index)]
    end
    
    subgraph Pass 1: Candidate Retrieval Stage
        UserVectorDB -->|User Interest Embeddings| ANNRetriever[Approximate Nearest Neighbor Retriever]
        PostVectorDB -->|5,000+ Case Study Vectors| ANNRetriever
        ANNRetriever -->|Top 200 Semantic Candidate Cards in <50ms| CandidatePool[200-Card Candidate Pool]
    end
    
    subgraph Pass 2: Heavy Business Ranking Stage
        CandidatePool --> HeavyRanker[Multi-Objective Scoring Function]
        CASDB -->|Creator CAS Weights: 0.00-10.00| HeavyRanker
        GeoDB -->|East Africa Regional Multiplier: 1.25x| HeavyRanker
        HeavyRanker --> DiversityFilter[Cold-Start & Cross-Discipline Diversity Injector]
    end
    
    DiversityFilter -->|Final Top 20 Ranked Cards| FeedOrchestrator
    FeedOrchestrator -->|Deliver Stream Cards with <200ms Latency| Client
```
