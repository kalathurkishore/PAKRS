# Personal Knowledge Retrieval System (PKRS) - Project Planner

## Vision

Build a **free, self-hosted AI-powered knowledge retrieval system** that
transforms exported Google Keep notes containing Instagram reels,
YouTube videos, articles, and personal notes into a searchable knowledge
base.

### Primary Goals

-   Exact keyword search
-   Semantic (AI) search
-   AI-generated summaries
-   Automatic tagging and categorization
-   Knowledge analytics dashboard
-   100% free using open-source software
-   Easy deployment using free hosting

------------------------------------------------------------------------

# Functional Requirements

## Data Sources

-   Google Keep export
-   YouTube links
-   Instagram reel links
-   Generic web URLs
-   Plain text notes

## Search Capabilities

-   Keyword search
-   Natural language search
-   Hybrid search (FTS + Vector Search)
-   Search by creator
-   Search by platform
-   Search by tags
-   Search by date
-   Similar content search

## AI Features

-   Automatic summaries
-   Keyword extraction
-   Topic classification
-   Embedding generation
-   Duplicate detection (future)
-   Learning timeline (future)

------------------------------------------------------------------------

# High-Level Architecture

    Google Keep Export
            │
            ▼
    Keep Parser
            │
            ▼
    Metadata Collection
            │
            ▼
    Transcript / OCR
            │
            ▼
    AI Processing
            │
            ├── SQLite
            └── FAISS
                    │
                    ▼
            Streamlit Search UI

------------------------------------------------------------------------

# Technology Stack

  Layer            Technology
  ---------------- -------------------------------------------------
  Language         Python 3.11
  Database         SQLite + FTS5
  Vector DB        FAISS
  Embeddings       BAAI/bge-small-en-v1.5
  OCR              EasyOCR
  Speech           Whisper
  UI               Streamlit
  Hosting          Streamlit Community Cloud / Hugging Face Spaces
  Source Control   GitHub

------------------------------------------------------------------------

# Repository Structure

    pkrs/
    │
    ├── app/
    ├── ingestion/
    ├── ai/
    ├── database/
    ├── vector_db/
    ├── data/
    ├── tests/
    ├── docs/
    ├── scripts/
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

# Milestones

## Phase 0 -- Planning (Week 1)

Deliverables - Requirements - Architecture - Repository setup - Initial
planner

Success Criteria - Repository initialized - Project skeleton committed

------------------------------------------------------------------------

## Phase 1 -- Google Keep Ingestion

Tasks - Parse exported Keep JSON/HTML - Extract metadata - Detect URLs -
Store notes

Deliverables - Parsed note objects - SQLite schema - Import pipeline

Success Criteria - 100% notes imported without duplication

------------------------------------------------------------------------

## Phase 2 -- Metadata Enrichment

Tasks - Fetch YouTube metadata - Capture Instagram metadata where
available - Download transcripts - OCR thumbnails if needed

Deliverables - Enriched metadata records

Risks - Instagram rate limits and restricted metadata.

Mitigation - Graceful fallback to stored note text and optional local
transcription.

------------------------------------------------------------------------

## Phase 3 -- AI Processing

Tasks - Generate summaries - Extract keywords - Classify topics -
Generate embeddings

Outputs - Summary - Tags - Topic - Embedding

------------------------------------------------------------------------

## Phase 4 -- Retrieval Engine

Components - SQLite FTS5 - FAISS index - Ranking layer

Ranking Strategy 1. Exact keyword score 2. Semantic similarity 3.
Recency boost (optional) 4. Combined weighted score

------------------------------------------------------------------------

## Phase 5 -- Streamlit UI

Pages - Home - Search - Filters - Item Details - Analytics - Settings

Features - Search box - Natural language search - Platform filters -
Topic filters - Open original link - Copy summary

------------------------------------------------------------------------

## Phase 6 -- Analytics Dashboard

Metrics - Total notes - Total videos - Topic distribution - Most
frequent creators - Most common keywords - Monthly saving trends

------------------------------------------------------------------------

## Phase 7 -- Deployment

Development - Local machine

Production - GitHub - Streamlit Community Cloud

Configuration - requirements.txt - secrets.toml (if needed)

------------------------------------------------------------------------

# Database Design

## Notes

-   id
-   title
-   body
-   created_at
-   updated_at
-   labels

## Links

-   id
-   note_id
-   platform
-   url

## Media

-   id
-   title
-   creator
-   summary
-   transcript
-   keywords
-   topic

## Embeddings

-   media_id
-   vector_reference

------------------------------------------------------------------------

# Non-Functional Requirements

-   Fast (\<2s typical search)
-   Offline indexing
-   Incremental updates
-   Modular code
-   Testable components
-   Extensible architecture

------------------------------------------------------------------------

# Testing Strategy

Unit Tests - Parsers - Database - Search - AI utilities

Integration Tests - Full ingestion - Search quality - UI smoke tests

Manual Tests - Random retrieval verification - Broken link handling

------------------------------------------------------------------------

# Risks

  Risk                        Mitigation
  --------------------------- ---------------------------------------
  Instagram API limitations   Fallback to note text/OCR/transcripts
  Large dataset               Incremental indexing
  Embedding model updates     Version embeddings
  Slow indexing               Batch processing

------------------------------------------------------------------------

# Stretch Goals

-   Chat interface (RAG)
-   Browser extension
-   Mobile-friendly UI
-   Calendar view
-   Knowledge graph
-   Personalized recommendations
-   LLM-generated study plans from saved content

------------------------------------------------------------------------

# Success Metrics

-   ≥95% retrieval accuracy for remembered concepts
-   \<2 second average search time
-   Automatic indexing of new exports
-   Zero manual tagging required for common workflows

------------------------------------------------------------------------

# Estimated Timeline

  Phase           Duration
  --------------- -----------
  Planning        1 week
  Ingestion       1 week
  Metadata        1 week
  AI Processing   2 weeks
  Retrieval       1 week
  UI              1 week
  Deployment      2--3 days
  Polish          1 week

**Estimated MVP:** 6--8 weeks

**Estimated Full Version:** 10--12 weeks
