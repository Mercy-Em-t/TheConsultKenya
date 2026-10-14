# Phase 3: Systems Design — Architecture Design & Infrastructure Specification Report
*System: Consult Kenya (Visual-First Professional Advisory & Authority Network)*  
*Standard: IEEE 1016 Software Design Description (SDD) / Dennis, Wixom & Tegarden (SAD) Architecture Standards*

---

## 1. Executive Summary & Architectural Vision

In Systems Analysis & Design (SAD), **Architecture Design** maps the logical functional processes (DFD) and data stores (ERD) onto physical hardware, software runtime environments, network fabrics, and client form factors.

For **Consult Kenya**, the architecture must bridge three demanding operational requirements:
1. **Ultra-Low Latency Visual Streaming:** Delivering interactive, high-contrast, swipeable visual case study cards and dynamic Mermaid SVG architecture blueprints to mobile and desktop clients across East Africa (frequently over 3G/4G cellular connections).
2. **Deterministic Financial & Legal Rigor:** Supporting high-concurrency Safaricom M-Pesa STK push callbacks, double-entry escrow ledger accounting, cryptographic SHA-256 deliverable fingerprinting, and automated Kenya Revenue Authority (KRA) eTIMS electronic tax invoicing with zero transactional loss.
3. **Continuous Algorithmic Intelligence:** Performing two-pass candidate retrieval via vector embeddings combined with real-time Creator Authority Score (CAS) re-ranking and anti-gaming heuristics.

This document presents a comprehensive evaluation of architectural archetypes, analyzes advanced and emerging configurations, establishes a custom **Multi-Tier Edge-Accelerated Composable Architecture**, evaluates 10 non-functional architectural requirements, and provides precise **Hardware, Software & Network Specifications** including a Cloud Bill of Materials (BOM).

---

## 2. In-Depth Analysis of Architectural Components & Patterns

```
+----------------------------------------------------------------------------------------------------+
|                                    THE FOUR ARCHITECTURAL LAYERS                                   |
+----------------------------------------------------------------------------------------------------+
| 1. DATA STORAGE TIER       : Physical persistence of structured, vector, and blob assets.         |
| 2. DATA ACCESS LOGIC TIER  : Object-relational mapping, database pooling, indexing, and caching.   |
| 3. APPLICATION LOGIC TIER  : Core business domain rules (CAS, Escrow, Moderation, Billing).        |
| 4. PRESENTATION LOGIC TIER : User interface rendering, interactive gestures, and client viewport. |
+----------------------------------------------------------------------------------------------------+
```

### A. Classic Client-Server Architectures & Tiering
How the four architectural layers are distributed across client devices and server hosts determines system scalability, security, and network overhead:

| Architecture Archetype | Allocation of Layers | Key Advantages | Fatal Deficiencies for Consult Kenya |
| :--- | :--- | :--- | :--- |
| **Server-Based Architecture** (Host-Centric / Mainframe) | • Presentation: Terminal / Dummy Client<br>• Application: Server<br>• Data: Server | Zero client-side computation; centralized control. | Incapable of interactive client-side gesture swiping, offline caching, and responsive Mermaid SVG client-side rendering. |
| **Client-Based Architecture** (Fat Client / File-Server) | • Presentation: Client<br>• Application: Client<br>• Data: File Server | Minimal server compute required. | Catastrophic security hazard: business logic and financial ledger rules live on client device; excessive network load downloading raw database files over mobile bandwidth. |
| **Two-Tier Client-Server** (Thick Client) | • Presentation & Application: Client<br>• Data Access & Data: Server | Offloads CPU load to client devices. | Hard to maintain across iOS/Android/Web; high bandwidth consumption; difficult to update algorithmic CAS scoring rules securely. |
| **Three-Tier Client-Server** (Thin Client) | • Presentation: Thin Client (Browser/Mobile)<br>• Application: Dedicated App Server<br>• Data Access & Data: DB Server | Clean separation of concerns; high security; client updates without database refactoring. | Solid foundation, but traditional 3-tier models struggle with real-time WebRTC media routing, edge caching, and AI vector similarity searches. |
| **N-Tier (Multi-Tier) Client-Server** | • Presentation: Edge CDN & Responsive Client<br>• API Gateway: Reverse Proxy & Auth<br>• App Services: Core Domain Services<br>• Real-Time Media: WebRTC SFU Media Tier<br>• Cache Tier: Redis In-Memory Cluster<br>• Persistent Data: Relational + Vector DB | Maximum modularity; horizontal auto-scaling; isolated failure domains; carrier-grade security. | Higher initial DevOps orchestration complexity (mitigated via containerized IaC deployment). |

---

### B. Analysis of Less Common & Emerging Architectural Paradigms

To ensure a forward-looking, enterprise-grade architecture, Systems Analysts evaluated advanced, less common, and cutting-edge architectural patterns:

#### 1. Peer-to-Peer (P2P) Architecture
* **Mechanism:** Clients communicate directly with one another without traversing an intermediary central server.
* **Evaluation for Consult Kenya:** Excellent for 1-on-1 audio/video consultation media streams (direct browser-to-browser WebRTC DTLS-SRTP encryption minimizes server bandwidth costs and delivers zero latency). However, totally unsuited for central search discovery, escrow ledger management, and moderation where centralized authority and audit trails are legally mandated.
* **Adoption Decision:** **Adopt as a Hybrid Subsystem:** Direct P2P WebRTC mesh for 1-on-1 consultations; centralized STUN/TURN fallback for NAT traversal.

#### 2. Event-Driven Architecture (EDA) & Reactive Streaming (CQRS / Event Sourcing)
* **Mechanism:** Decouples subsystems through an asynchronous message broker (e.g. Apache Kafka or RabbitMQ). Producers publish domain events (`MilestoneSubmitted`, `PaymentCaptured`), and independent consumer workers react asynchronously. Command Query Responsibility Segregation (CQRS) separates read models from write models.
* **Evaluation for Consult Kenya:** Crucial for financial and fintech operations. Safaricom M-Pesa STK callbacks and KRA eTIMS submissions arrive unpredictably. If the payment gateway spikes, an event queue absorbs the shock without dropping transactions.
* **Adoption Decision:** **Adopt for Financial, Telemetry & Notification Subsystems:** Redis Pub/Sub and Celery event queues power asynchronous fintech reconciliation and CAS telemetry.

#### 3. Edge Computing & Serverless Fluid Topology
* **Mechanism:** Code execution and static assets are distributed across globally decentralized edge locations (e.g. Cloudflare Workers or AWS CloudFront Edge Lambdas) situated within milliseconds of the end user.
* **Evaluation for Consult Kenya:** Kenyan mobile networks (Safaricom, Airtel) experience variable international transit latency to European or US cloud datacenters (150–250ms). Serving pre-rendered case study previews, cached Bento grids, and SVG bundles from local edge points of presence (PoP) in Nairobi and Mombasa drops initial page load to **under 80ms**.
* **Adoption Decision:** **Adopt for Presentation & Caching Layer:** Edge CDN caching with stale-while-revalidate policies for all case studies and Bento profile assets.

#### 4. Microservices vs. Modular Monolith Architecture
* **Evaluation:** While hyper-scale enterprises use hundreds of microservices, early-stage distributed microservices introduce catastrophic network latency, distributed transaction complexity (two-phase commit headaches), and massive DevOps overhead.
* **Adoption Decision:** **Adopt a High-Performance Modular Monolith (Cloud-Native Hexagonal / Clean Architecture):** Built with strictly decoupled internal domain modules (Identity, CaseStudies, Booking, Escrow, Discovery) communicating via in-process domain interfaces, deployed within unified containerized clusters with Redis and PostgreSQL/pgvector. Individual heavy workers (video transcoding, batch CAS calculation) run as decoupled background container tasks.

---

## 3. Selected Physical Architecture & Deployment Topology

The selected architecture is an **Edge-Accelerated, Multi-Tier Composable Cloud-Native Architecture**:

```mermaid
flowchart TD
    subgraph Client Tier (Form Factors)
        MClient["Mobile PWA / Native App\n(iOS & Android Viewport)"]
        DClient["Desktop Web Client\n(Chrome, Safari, Edge, Firefox)"]
    end

    subgraph Edge Delivery & Security Tier (Cloudflare Global Network)
        EdgeCDN["Cloudflare Edge PoP (Nairobi / Mombasa / JNB)"]
        WAF["Web Application Firewall & DDoS Shield"]
        SSL["TLS 1.3 Termination & Certs"]
        StaticEdge[("Edge Static Asset Cache\nSVGs, CSS, JS, Avatars")]
    end

    subgraph Ingress & Gateway Tier (AWS eu-west-1 / af-south-1)
        ALB["Application Load Balancer (AWS ALB)"]
        APIGateway["Reverse Proxy & Rate Limiter\n(FastAPI / Nginx Ingress)"]
    end

    subgraph Core Application Tier (ECS Fargate Containers)
        AppCore["Consult Kenya Core Modular Monolith\n• Identity & Auth Module\n• Creation Studio & Markdown Parser\n• Escrow & Ledger State Machine\n• Booking & Scheduling Engine"]
        WorkerPool["Background Asynchronous Worker Pool (Celery)\n• Daraja Callback Worker\n• KRA eTIMS Batch Syncer\n• SHA-256 Deliverable Hasher\n• 72-Hr Inspection Timer"]
        CASEngine["AI Two-Pass Recommendation & CAS Daemon\n• Pass 1 Vector Retriever\n• Pass 2 CAS Multiplier Re-Ranker"]
    end

    subgraph Real-Time Media Tier
        LiveKit["LiveKit Cloud / WebRTC SFU Cluster\n(Johannesburg & Nairobi Media Relays)"]
    end

    subgraph Managed Data & Persistence Tier
        DBPrimary[("Primary Relational & Vector DB\nAmazon RDS PostgreSQL 16 + pgvector\n(Multi-AZ Automated Standby)")]
        DBReplica[("Read-Replica DB\n(High-Throughput Analytics & Search)")]
        RedisCluster[("Redis In-Memory Cluster 7.2\n• Active Slot Locks (15-min)\n• CAS Ranking Multipliers\n• Celery Broker & Session Cache")]
        S3Bucket[("Amazon S3 Encrypted Object Store\n• Case Study Media Decks\n• Milestone Deliverable Vault (AES-256)\n• Tamper-Proof Audit Archive")]
    end

    subgraph External Managed APIs
        Daraja["Safaricom Daraja API\n(STK Push & B2C Rails)"]
        Paystack["Paystack / Card Rails\n(PCI-DSS 3DS Gateway)"]
        KRA["KRA eTIMS API\n(Statutory Invoicing)"]
        Registries["Statutory Registries\n(IPRS, KRA, LSK, EBK)"]
        Calendar["Google & Outlook APIs"]
    end

    %% Client Connections
    MClient & DClient -->|HTTPS / WSS / TLS 1.3| EdgeCDN
    EdgeCDN --> WAF --> SSL
    SSL -->|Cached Assets| StaticEdge
    SSL -->|Dynamic REST / GraphQL / WS| ALB
    ALB --> APIGateway
    APIGateway --> AppCore

    %% Internal Services
    AppCore <-->|Pub/Sub & Cache| RedisCluster
    AppCore -->|Write / Transact| DBPrimary
    AppCore -->|Read Feeds / Profiles| DBReplica
    DBPrimary -.->|Async Replication| DBReplica
    AppCore -->|Store Deliverables / Assets| S3Bucket

    AppCore -->|Enqueue Heavy Jobs| WorkerPool
    WorkerPool <--> DBPrimary
    WorkerPool <--> RedisCluster
    WorkerPool --> S3Bucket

    CASEngine <--> RedisCluster
    CASEngine <--> DBReplica

    %% Real-time Video
    MClient & DClient <-->|DTLS-SRTP Encrypted Audio/Video| LiveKit
    AppCore -->|Generate JWT Tokens & Webhooks| LiveKit

    %% External Connections
    WorkerPool <-->|STK Push & Callbacks| Daraja
    WorkerPool <-->|Card Tokens & Webhooks| Paystack
    WorkerPool <-->|Tax Submissions & QR Codes| KRA
    WorkerPool <-->|Identity & Board Verification| Registries
    AppCore <-->|Free/Busy Sync| Calendar
```

---

## 4. Evaluation Against 10 Non-Functional Architectural Requirements

A world-class Systems Architecture must explicitly address operational, performance, security, and socio-political constraints. Below is our formal compliance analysis:

```
+------------------------------------+---------------------------------------------------------------------------------+
|       ARCHITECTURAL REQUIREMENT    |              CONCRETE ARCHITECTURAL IMPLEMENTATION & MITIGATION                 |
+------------------------------------+---------------------------------------------------------------------------------+
| 1. Operational: Availability       | Multi-AZ Hot Standby architecture across independent Availability Zones in      |
|    & Fault Tolerance (99.95%)      | AWS. PostgreSQL automated failover in <60 seconds; stateless containerized     |
|                                    | ECS Fargate auto-healing upon container crash; zero-downtime rolling deploys.   |
+------------------------------------+---------------------------------------------------------------------------------+
| 2. Operational: Multi-Device       | Unified Responsive Progressive Web App (PWA) built with Next.js & Tailwind CSS. |
|    Portability & Responsiveness    | Identical visual fidelity across mobile screens (360px), tablets (768px), and   |
|                                    | desktop displays (1440px+). PWA service workers enable home-screen app launch.  |
+------------------------------------+---------------------------------------------------------------------------------+
| 3. Performance: Sub-Second Page    | Cloudflare Edge CDN PoP in Nairobi caches static assets and pre-rendered        |
|    Load & Feed Latency (<800ms)    | Bento grids. Pass-1 vector retrieval and pre-computed Redis CAS scores serve     |
|                                    | personalized feed streams in <180ms total server response time.                 |
+------------------------------------+---------------------------------------------------------------------------------+
| 4. Performance: High-Throughput    | Asynchronous queue architecture (Celery + Redis) processes up to 1,000 M-Pesa   |
|    Fintech Concurrency             | callbacks per second. Redis slot locking prevents double-booking race conditions.|
+------------------------------------+---------------------------------------------------------------------------------+
| 5. Security: Data Protection       | Server-Side Encryption (SSE-KMS) with AES-256 for all S3 documents and database |
|    & Encryption at Rest / Transit  | volumes. TLS 1.3 for all data in transit. Automated field-level encryption for  |
|                                    | PII (National ID, Tax PIN) meeting Kenya Data Protection Act (KDPA) 2019 rules. |
+------------------------------------+---------------------------------------------------------------------------------+
| 6. Security: Zero-Trust Identity   | Role-Based Access Control (RBAC) enforced via cryptographically signed JWT tokens|
|    & Audit Immutability            | with 15-minute expiration and rotating refresh tokens. Immutable write-only     |
|                                    | audit logs in S3 Object Lock vault for financial settlements and dispute cases. |
+------------------------------------+---------------------------------------------------------------------------------+
| 7. Cultural: Mobile-First Visual   | Designed natively for Kenya's visual-first digital culture. Eliminates dense    |
|    Ergonomics (TikTok / Instagram) | text CVs in favor of swipeable carousels, color-coded Bento tags, and split-screen|
|                                    | interactive architecture previews optimized for vertical mobile thumb reach.   |
+------------------------------------+---------------------------------------------------------------------------------+
| 8. Political & Legal: Kenyan Tax   | Direct integration with KRA eTIMS API for instant electronic tax invoicing with |
|    & eTIMS Compliance              | verifiable QR codes. Automatic withholding tax reporting prevents regulatory    |
|                                    | fines for both platform and corporate enterprise buyers.                       |
+------------------------------------+---------------------------------------------------------------------------------+
| 9. Cultural / Economic: Low-Data   | Adaptive bandwidth optimization: client detects network speed and switches from |
|    Offline Resilience (Rural 3G)   | rich video snippets to lightweight SQLite/IndexedDB cached vector cards without |
|                                    | breaking the UI. Mermaid charts compile client-side using tiny text payloads.   |
+------------------------------------+---------------------------------------------------------------------------------+
| 10. Maintainability & Modularity:  | Hexagonal modular monolith architecture ensures strict domain boundaries. Third-|
|     Decoupled Adapter Extensibility| party APIs (Daraja, LiveKit, KRA) sit behind abstract interfaces, allowing 100% |
|                                    | vendor replacement without altering core domain business logic.                |
+------------------------------------+---------------------------------------------------------------------------------+
```

---

## 5. Hardware, Software & Network Specifications

### A. Software Runtime & Technology Stack Specification

| Subsystem Layer | Technology / Runtime Component | Version / Specification | Architectural Purpose & Rationale |
| :--- | :--- | :--- | :--- |
| **Client Frontend** | **Next.js (React) + TypeScript** | Next.js 14.x / React 18+ | High-performance hybrid SSR & Client-side rendering; seamless responsive PWA capabilities. |
| **Styling & UI Components** | **Tailwind CSS + Radix UI + Lucide** | Tailwind v3.4+ | Utility-first CSS compiling to $<50\text{KB}$ production bundles; high-contrast modern Bento aesthetic. |
| **Diagram Engine** | **Mermaid.js (SVG Renderer)** | Mermaid v10.9+ | Client-side zero-latency vector rendering of flowcharts, architectures, and state machines. |
| **Backend Core Runtime** | **Python (FastAPI + Pydantic v2)** | Python 3.12 / FastAPI 0.111+ | Asynchronous high-throughput web framework; native typing; industry standard for AI vector operations. |
| **Async Task Broker** | **Celery + Redis** | Celery 5.4+ / Redis 7.2 | Reliable distributed background task execution for fintech webhooks, timers, and tax invoices. |
| **Primary Relational DB** | **PostgreSQL + pgvector** | PostgreSQL 16.3 + pgvector 0.7 | ACID-compliant transactional persistence; hybrid relational + vector cosine embedding indexing. |
| **In-Memory Cache & Locks**| **Redis Cluster** | Redis 7.2.4 | Sub-millisecond slot coordinator (15-min locks), session cache, and pre-computed CAS weights. |
| **Object / Blob Storage** | **Amazon S3 + CloudFront** | S3 Standard / Glacier Vault | Encrypted document storage, SHA-256 deliverable archives, immutable legal dispute dossiers. |
| **Containerization & CI/CD**| **Docker + GitHub Actions** | Docker Engine 26.x | Immutable container packaging; automated linting, security scanning, and blue/green deploys. |

---

### B. Hardware & Compute Sizing Specifications (Phase 1 & Phase 2 Sizing)

Based on our projected concurrency of **5,000 daily active users (DAU)**, **500 concurrent visual streams**, and **50 simultaneous WebRTC consultations** during initial rollout:

| Architectural Tier | Host Type / Sizing | Instances / Sizing | vCPU | RAM | Storage / Disk | Sizing Rationale & Workload |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Application Ingress (ALB)**| AWS Application Load Balancer | 1 Multi-AZ | — | — | — | Handles up to 25,000 active TCP connections; SSL termination; DDoS mitigation. |
| **Core Web / API Containers**| AWS ECS Fargate Task | 2 min – 8 max (Auto-scaled) | 2 vCPU per task | 4 GB per task | 20 GB Ephemeral | Handles stateless HTTP/REST requests, Markdown/Mermaid parsing, and session tokens. |
| **Async Worker Containers** | AWS ECS Fargate Task | 2 min – 6 max (Auto-scaled) | 2 vCPU per task | 4 GB per task | 20 GB Ephemeral | Handles Daraja callbacks, eTIMS tax sync, SHA-256 deliverable hashing, and email/SMS. |
| **Primary Relational DB** | Amazon RDS for PostgreSQL (Multi-AZ)| 1 Primary + 1 Standby (`db.m6g.xlarge`)| 4 vCPU | 16 GB | 250 GB gp3 SSD (3,000 IOPS)| Holds 12 relational entities, 3NF schemas, and pgvector embeddings. Multi-AZ hot standby. |
| **Read-Replica DB** | Amazon RDS for PostgreSQL (`db.m6g.large`)| 1 Read-Replica | 2 vCPU | 8 GB | 250 GB gp3 SSD | Dedicated offload for intensive discovery feed queries and administrative analytics. |
| **In-Memory Cache Cluster** | Amazon ElastiCache for Redis | 2 Nodes (`cache.m6g.large` Multi-AZ)| 2 vCPU per node| 6.4 GB per node| Memory-only (AOF enabled)| Redis cluster managing 15-minute slot locks, session states, and CAS telemetry weights. |
| **Encrypted Object Storage** | Amazon S3 Standard (SSE-KMS)| Scalable Bucket Tier | — | — | 1 TB initial (Auto-expanding)| Encrypted storage for deliverable archives, PDFs, video snippets, and audit snapshots. |

---

### C. Network Bandwidth, Topology & Edge Specifications

```
+------------------------------------+---------------------------------------------------------------------------------+
|          NETWORK PARAMETER         |                              TECHNICAL SPECIFICATION                           |
+------------------------------------+---------------------------------------------------------------------------------+
| 1. Virtual Private Cloud (VPC)     | Dedicated AWS VPC configured across 3 Availability Zones (eu-west-1a, b, c).    |
|    Segmentation                    | Subnets partitioned into:                                                       |
|                                    | • Public Subnet (ALB, NAT Gateways only)                                        |
|                                    | • Private Application Subnet (ECS Fargate containers)                           |
|                                    | • Isolated Database Subnet (RDS PostgreSQL, Redis; zero direct Internet routing)|
+------------------------------------+---------------------------------------------------------------------------------+
| 2. Edge CDN & PoP Routing          | Cloudflare Enterprise / Pro Edge with Anycast routing to Nairobi (NBO) and      |
|                                    | Mombasa (MBA) internet exchange points (KIXP), terminating TLS in <15ms.        |
+------------------------------------+---------------------------------------------------------------------------------+
| 3. Bandwidth Budget & Sizing       | • Average case study card payload: 120 KB (compressed SVGs + metadata)         |
|                                    | • Peak egress bandwidth: ~150 Mbps under 2,000 concurrent browsing users.       |
|                                    | • Media bandwidth (WebRTC): Offloaded to LiveKit Cloud with adaptive simulcast   |
|                                    |   (150 kbps audio-only up to 1.2 Mbps 720p video).                              |
+------------------------------------+---------------------------------------------------------------------------------+
| 4. Ingress Security & Firewalls    | Security Groups enforce strict zero-trust ingress:                              |
|                                    | • ALB accepts ports 80/443 from Cloudflare IP ranges only.                      |
|                                    | • ECS Containers accept port 8000 only from ALB Security Group.                 |
|                                    | • RDS accepts port 5432 only from ECS Application Security Group.               |
|                                    | • Redis accepts port 6379 only from ECS Application Security Group.             |
+------------------------------------+---------------------------------------------------------------------------------+
```

---

### D. Cloud Infrastructure Bill of Materials (BOM) — Monthly Cost Budget

Based on standard AWS and SaaS managed rates for the East Africa / Europe deployment:

| Infrastructure Resource Item | Sizing / Specification | Provider | Estimated Monthly Cost (USD) | Estimated Monthly Cost (KES)* |
| :--- | :--- | :---: | :---: | :---: |
| **AWS ECS Fargate Compute** (4 tasks avg) | 8 vCPU, 16 GB RAM aggregate | AWS | $145.00 | KES 18,850 |
| **Amazon RDS PostgreSQL (Multi-AZ)** | `db.m6g.xlarge` + 250 GB gp3 | AWS | $290.00 | KES 37,700 |
| **Amazon RDS Read-Replica** | `db.m6g.large` + 250 GB gp3 | AWS | $145.00 | KES 18,850 |
| **Amazon ElastiCache Redis (Multi-AZ)** | `cache.m6g.large` (2 nodes) | AWS | $110.00 | KES 14,300 |
| **Amazon ALB & NAT Gateway Data** | 1 ALB + 1 NAT Gateway | AWS | $65.00 | KES 8,450 |
| **Amazon S3 Storage & Bandwidth** | 1 TB S3 Standard + KMS | AWS | $35.00 | KES 4,550 |
| **Cloudflare Pro Plan + CDN** | Global Edge + Nairobi PoP | Cloudflare | $25.00 | KES 3,250 |
| **LiveKit Cloud (WebRTC Video)** | 10,000 participant minutes/mo | LiveKit | $60.00 | KES 7,800 |
| **Domain, SSL & Monitoring (Datadog/Sentry)**| APM, Tracing, Error Alerting | SaaS | $50.00 | KES 6,500 |
| **TOTAL ESTIMATED MONTHLY HOSTING BOM** | — | — | **$925.00 / mo** | **~KES 120,250 / mo** |

*\*Assumed exchange rate: 1 USD = 130 KES. Sizing is right-sized for initial pilot with auto-scaling headroom to 50,000 active users.*

---

## 6. Architecture Sign-Off & Verification

This architecture design fully bridges the logical models of Phase 2 into physical runtime specifications:
* **DFD Datastores (`D1`–`D10`)** $\to$ Physically mapped to PostgreSQL 16 multi-AZ tables, S3 object vaults, and Redis clusters.
* **Use Cases (`UC-01`–`UC-22`)** $\to$ Backed by scalable containerized services with sub-second response times.
* **System Acquisition Strategy** $\to$ Faithfully implements the **Hybrid / Composable API-Led Integration** model.

**Status:** Architecture Design, Topology & Hardware/Software Specifications Complete. Ready for Interface & Program Design.
