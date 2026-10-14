# Business Process Specification: Discover, Search & Personalize Content Delivery
**Process ID:** `PROC-3.0` | **Owner:** Client / AI Recommendation Daemon

### Description
Retrieves and delivers hyper-relevant case studies and specialist profiles via a Two-Pass algorithmic engine combining pgvector semantic search, Creator Authority Scores (CAS), and regional East African weights.

### Associated External Entities
- **Client**
- **Guest Visitor**

### Associated Data Stores
- **D3: Case Studies & Artifacts Datastore**
- **D5: Creator Authority & Telemetry Cache (Redis)**
- **D7: User Collections & Bookmarks DB**

### Data Flow Analysis (Inputs & Outputs)
| Flow Direction | Data Flow Name / Payload | Source / Origin | Destination |
| :---: | :--- | :--- | :--- |
| $\longleftarrow$ (Inflow) | Feed request & display preference (Vertical vs. Grid) | Client | `PROC-3.0` |
| $\longleftarrow$ (Inflow) | Natural language search query & facet filters | Client | `PROC-3.0` |
| $\longleftarrow$ (Inflow) | Dwell time & interaction telemetry | Client Device | `PROC-3.0` |
| $\longleftarrow$ (Inflow) | Bookmark & Collection save requests | Client | `PROC-3.0` |
| $\longrightarrow$ (Outflow) | Two-Pass Ranked Discovery Feed Payload | `PROC-3.0` | Client Display |
| $\longrightarrow$ (Outflow) | Segmented Search Results (Decks, Experts, Tags) | `PROC-3.0` | Client Display |
| $\longrightarrow$ (Outflow) | Personalized Collection Index | `PROC-3.0` | Client Display / D7 |
| $\longrightarrow$ (Outflow) | 5x Engagement Multiplier Signal | `PROC-3.0` | D5: Telemetry Cache |

### Decomposed Sub-Processes (Level 1 DFD Scope)
| Sub-Process ID | Sub-Process Name | Operational Description |
| :---: | :--- | :--- |
| **3.1** | Ingest Client Session Context & Geo-Intent | Captures client domain history and regional location data. |
| **3.2** | Execute Pass-1 ANN Vector Retrieval | Performs high-speed approximate nearest neighbor search across embeddings. |
| **3.3** | Execute Pass-2 CAS & Diversity Re-Ranking | Applies business weights (CAS, freshness, geo) and author diversity limits. |
| **3.4** | Deliver Dual-Mode Feed Stream | Serves pre-buffered responsive cards with low-bandwidth fallbacks. |
| **3.5** | Process Semantic Search & Facet Filters | Executes hybrid vector + full-text filtering across topic hubs. |
| **3.6** | Manage Bookmarks & Organize Collections | Stores curated decks in client folders and emits algorithmic boosts. |
