# Personal AI Knowledge Retrieval System (PAKRS)

## Holistic Vision, Architecture, Approach & Master Planner

**Version:** 1.0 (Master Planning Document)

------------------------------------------------------------------------

# 1. Vision

Build an AI-powered Personal Knowledge Retrieval System that transforms
exported Google Keep notes into a searchable, intelligent knowledge
base.

Instead of remembering where something was saved, users describe what
they remember:

> "Find the reel explaining TensorRT optimization."

The system retrieves the correct note using both keyword and semantic
understanding.

------------------------------------------------------------------------

# 2. Problem Statement

Over time Google Keep becomes a storage system instead of a retrieval
system.

Challenges include: - Hundreds/thousands of notes - Instagram reels -
YouTube videos - Articles - Personal notes - Duplicate ideas - No
semantic search - Difficult rediscovery

------------------------------------------------------------------------

# 3. Project Goals

## Functional Goals

-   Import Google Keep
-   Parse every note
-   Detect all links
-   Extract metadata
-   Generate summaries
-   Generate embeddings
-   Build hybrid search
-   Provide analytics
-   Support incremental indexing

## Non-functional Goals

-   Completely free
-   Open source
-   Offline indexing
-   Modular architecture
-   Easy deployment
-   Extensible

------------------------------------------------------------------------

# 4. End-to-End Workflow

``` text
Google Keep Export
      │
      ▼
Keep Parser
      │
      ▼
Normalize Notes
      │
      ▼
Extract Links
      │
      ▼
Metadata Collection
      │
      ▼
Speech Transcript
OCR
Captions
      │
      ▼
Cleaning
Chunking
      │
      ▼
AI Processing
 ├─ Summary
 ├─ Keywords
 ├─ Topics
 ├─ Named Entities
 └─ Embeddings
      │
      ▼
SQLite + FTS5
FAISS Index
      │
      ▼
Hybrid Search Engine
      │
      ▼
Streamlit Web UI
```

------------------------------------------------------------------------

# 5. Core Modules

1.  Google Keep Parser
2.  Note Normalizer
3.  URL Extractor
4.  Metadata Collector
5.  Transcript Pipeline
6.  OCR Pipeline
7.  AI Enrichment
8.  Embedding Generator
9.  SQLite Database
10. Vector Database
11. Hybrid Retrieval Engine
12. Analytics Engine
13. Streamlit Frontend

Each module should be independently testable.

------------------------------------------------------------------------

# 6. Recommended Technology

  Component         Choice
  ----------------- ------------------------------------------------
  Language          Python 3.11
  DB                SQLite + FTS5
  Vector Index      FAISS
  Embeddings        BGE Small or MiniLM
  OCR               EasyOCR
  Speech            Whisper
  UI                Streamlit
  Hosting           Streamlit Community Cloud / HuggingFace Spaces
  Version Control   GitHub

------------------------------------------------------------------------

# 7. Suggested Repository

``` text
pakrs/
├── app/
├── ingestion/
├── enrichment/
├── retrieval/
├── analytics/
├── database/
├── vector_db/
├── config/
├── scripts/
├── docs/
├── tests/
└── data/
```

------------------------------------------------------------------------

# 8. Database Concept

Main entities:

-   Notes
-   Links
-   Media
-   Creators
-   Tags
-   Topics
-   Embeddings
-   Search History

Relationships:

Note → Links

Link → Metadata

Metadata → Embedding

Embedding → Search Result

------------------------------------------------------------------------

# 9. AI Processing Pipeline

For every piece of content generate:

-   Summary
-   Keywords
-   Topic
-   Tags
-   Named entities
-   Difficulty
-   Embedding vector

Future:

-   Knowledge graph
-   Related content
-   Recommendations

------------------------------------------------------------------------

# 10. Retrieval Strategy

Use Hybrid Retrieval.

Stage 1 - SQLite FTS5 - Exact keyword search

Stage 2 - FAISS semantic retrieval

Stage 3 - Merge results

Stage 4 - Re-rank

Future: - BM25 - Cross Encoder reranking - Query expansion

------------------------------------------------------------------------

# 11. User Experience

Search examples:

-   Find CUDA optimization reel
-   Show everything about BEV
-   Videos related to TensorRT
-   Notes from last month about transformers

Filters:

-   Platform
-   Topic
-   Creator
-   Date
-   Tags

------------------------------------------------------------------------

# 12. Analytics

Dashboard should answer:

-   What topics do I save most?
-   Which creators do I follow?
-   Monthly learning trend
-   Most searched topics
-   Knowledge growth

------------------------------------------------------------------------

# 13. Deployment Plan

Development: - Local Python

Source: - GitHub

Hosting: - Streamlit Community Cloud

Indexes stored locally and regenerated when data changes.

------------------------------------------------------------------------

# 14. Risks

  Risk                     Mitigation
  ------------------------ --------------------------
  Metadata unavailable     Fallback to note text
  Instagram restrictions   OCR + Whisper
  Duplicate notes          Hash-based deduplication
  Large datasets           Incremental indexing

------------------------------------------------------------------------

# 15. Phased Roadmap

## Phase 1

Planning and repository setup

Deliverables: - Project structure - Documentation - Initial schema

## Phase 2

Google Keep ingestion

Deliverables: - Parser - URL extraction - SQLite storage

## Phase 3

Metadata enrichment

Deliverables: - Titles - Captions - Thumbnails - Transcripts

## Phase 4

AI enrichment

Deliverables: - Summaries - Keywords - Embeddings

## Phase 5

Search engine

Deliverables: - Keyword search - Semantic search - Hybrid ranking

## Phase 6

Frontend

Deliverables: - Streamlit UI - Filters - Search - Detail page

## Phase 7

Analytics

Deliverables: - Dashboards - Charts - Trends

## Phase 8

Deployment

Deliverables: - Public application - Documentation - User guide

------------------------------------------------------------------------

# 16. Future Vision

Expand beyond Google Keep:

-   PDFs
-   Browser bookmarks
-   Notion
-   Obsidian
-   GitHub stars
-   Research papers
-   Local documents
-   Images
-   Audio
-   Videos

Eventually evolve into a personal AI knowledge assistant with
conversational search.

------------------------------------------------------------------------

# 17. Success Metrics

-   Accurate retrieval (\>95% for known concepts)
-   Search latency under 2 seconds
-   Fully automated indexing
-   Minimal manual tagging
-   Modular, maintainable architecture
-   Zero-cost operation

------------------------------------------------------------------------

# 18. Guiding Principles

-   Local-first whenever possible
-   Open-source components
-   AI assists but never hides original data
-   Modular over monolithic
-   Incremental processing
-   Reproducible indexing
-   Clean documentation before implementation

------------------------------------------------------------------------

# 19. Next Immediate Tasks

1.  Initialize Git repository.
2.  Export Google Keep.
3.  Design SQLite schema.
4.  Build parser.
5.  Import notes.
6.  Build metadata collectors.
7.  Integrate Whisper and OCR.
8.  Generate embeddings.
9.  Build hybrid search.
10. Create Streamlit interface.
11. Add analytics.
12. Deploy MVP.

This document serves as the master planning blueprint for the MVP and
provides the foundation for detailed engineering documentation in later
phases.
