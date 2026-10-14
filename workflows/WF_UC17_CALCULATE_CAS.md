# UC-17: Calculate Creator Authority Score (CAS)
*Diagram Type: Data Flow Diagram (DFD Level 1 - Authority Computation Pipeline)*

Traces incoming signals from credential registries, completed contracts, telemetry dwell-times, and peer endorsements into the normalized Creator Authority Score.

```mermaid
flowchart LR
    subgraph Data Sources & Telemetry
        KYCStore[(Verified Identity & Board DB)]
        ContractStore[(Completed Escrow Contracts DB)]
        TelemetryStream[(Dwell-Time & Bookmark Telemetry)]
        PeerStore[(Peer Endorsement Graph)]
    end
    
    subgraph Authority Processing Pipeline
        AnomalyDetector[Bot & Anti-Gaming Anomaly Filter]
        WeightCalculator[Multi-Factor Weighted Aggregator]
        DecayApplier[180-Day Inactivity Time-Decay Module]
        Normalizer[0.00 - 10.00 Score Normalizer]
    end
    
    subgraph Consumers
        CreatorProfile[(Creator Profile Record)]
        FeedRanker[(Two-Pass Feed Ranking Engine)]
    end
    
    KYCStore -->|Verified Licenses: 40% Weight| WeightCalculator
    ContractStore -->|Completed Contracts & Ratings: 30% Weight| WeightCalculator
    
    TelemetryStream -->|Saves & Dwell Events| AnomalyDetector
    AnomalyDetector -->|Sanitized Save Signals: 15% Weight| WeightCalculator
    
    PeerStore -->|Cryptographic Attestations: 15% Weight| WeightCalculator
    
    WeightCalculator -->|Raw Aggregate Score| DecayApplier
    DecayApplier -->|Decayed Score| Normalizer
    
    Normalizer -->|Final Normalized CAS: 0.00-10.00| CreatorProfile
    Normalizer -->|CAS Multiplier| FeedRanker
```
