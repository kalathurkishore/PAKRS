# Personal AI Knowledge Retrieval System (PAKRS)

> **Version:** 1.0\
> **Status:** Planning\
> **Goal:** Build a free, AI-powered personal knowledge platform that
> indexes Google Keep notes containing Instagram reels, YouTube videos,
> articles, and personal notes, enabling fast keyword and semantic
> search.

------------------------------------------------------------------------

# 1. Vision

Traditional note applications are optimized for storage, not retrieval.
Over time, users accumulate hundreds or thousands of saved links and
notes that become difficult to rediscover.

This project transforms those notes into an AI-powered searchable
knowledge base.

## Objectives

-   Index all Google Keep notes.
-   Extract rich metadata from links.
-   Generate AI summaries and keywords.
-   Support keyword and semantic search.
-   Provide analytics and learning insights.
-   Host entirely using free/open-source tools.

------------------------------------------------------------------------

# 2. Functional Requirements

## Input Sources

-   Google Keep export
-   YouTube URLs
-   Instagram Reel URLs
-   Generic web links
-   Plain text notes

## Core Features

-   Automatic ingestion
-   Link extraction
-   Metadata enrichment
-   Transcript extraction
-   OCR
-   AI summarization
-   Keyword extraction
-   Topic classification
-   Embedding generation
-   Hybrid search
-   Analytics dashboard

------------------------------------------------------------------------

# 3. High-Level Architecture

``` text
Google Keep Export
        │
        ▼
Keep Parser
        │
        ▼
URL Extractor
        │
        ▼
Metadata Collector
        │
        ▼
Transcript / OCR
        │
        ▼
AI Processing
        │
 ┌──────┴─────────┐
 ▼                ▼
SQLite         FAISS
 └──────┬─────────┘
        ▼
 Search Engine
        ▼
 Streamlit UI
```

------------------------------------------------------------------------

# 4. Recommended Technology Stack

  Layer            Technology
  ---------------- -------------------------------------------------
  Language         Python 3.11
  Database         SQLite + FTS5
  Vector Search    FAISS
  Embeddings       BAAI/bge-small-en-v1.5
  OCR              EasyOCR
  Speech           Whisper
  UI               Streamlit
  Hosting          Streamlit Community Cloud / Hugging Face Spaces
  Source Control   GitHub

------------------------------------------------------------------------

# 5. Repository Structure

``` text
pakrs/
├── app/
├── ingestion/
├── ai/
├── retrieval/
├── analytics/
├── database/
├── vector_db/
├── config/
├── scripts/
├── tests/
├── docs/
├── data/
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# 6. Module Design

## 6.1 Keep Parser

Responsibilities

-   Parse exported JSON/HTML
-   Extract metadata
-   Normalize notes
-   Detect duplicate notes

Outputs

-   Structured note objects

------------------------------------------------------------------------

## 6.2 Link Extractor

Responsibilities

-   Detect URLs
-   Identify platform
-   Validate links

Platforms

-   YouTube
-   Instagram
-   Generic websites

------------------------------------------------------------------------

## 6.3 Metadata Collector

Collect

-   Title
-   Description
-   Creator
-   Thumbnail
-   Duration
-   Publish date

Fallback gracefully when metadata cannot be fetched.

------------------------------------------------------------------------

## 6.4 Transcript Pipeline

Sources

-   YouTube transcripts
-   Whisper transcription
-   OCR extracted text

------------------------------------------------------------------------

## 6.5 AI Pipeline

Generate

-   Summary
-   Keywords
-   Topic
-   Difficulty
-   Named entities
-   Embeddings

------------------------------------------------------------------------

# 7. Database Design

## notes

-   id
-   title
-   body
-   created_at
-   updated_at
-   labels

## links

-   id
-   note_id
-   platform
-   url

## media

-   id
-   title
-   creator
-   summary
-   transcript
-   keywords
-   topic

## embeddings

-   media_id
-   embedding_reference

------------------------------------------------------------------------

# 8. Search Design

## Keyword Search

SQLite FTS5

## Semantic Search

FAISS

## Hybrid Ranking

Score = 0.45 \* FTS + 0.45 \* Vector + 0.10 \* Recency

------------------------------------------------------------------------

# 9. Streamlit Pages

-   Dashboard
-   Search
-   Collections
-   Analytics
-   Settings

------------------------------------------------------------------------

# 10. Analytics

Metrics

-   Total notes
-   Total links
-   Topics
-   Creators
-   Monthly activity
-   Frequently searched keywords

------------------------------------------------------------------------

# 11. Deployment

Development

-   Local Python

Production

-   GitHub
-   Streamlit Community Cloud

------------------------------------------------------------------------

# 12. Testing

Unit

-   Parsers
-   Database
-   Search

Integration

-   End-to-end ingestion

Manual

-   Retrieval quality
-   Duplicate detection

------------------------------------------------------------------------

# 13. Risks

  Risk                    Mitigation
  ----------------------- ----------------------------------------------
  Instagram limitations   OCR + local transcription + stored note text
  Large dataset           Incremental indexing
  Embedding updates       Version embeddings

------------------------------------------------------------------------

# 14. Future Enhancements

-   Chat assistant over saved knowledge
-   Knowledge graph
-   Browser extension
-   Mobile app
-   Duplicate clustering
-   Personalized recommendations
-   Calendar timeline
-   Voice search
-   PDF indexing
-   Notion/Obsidian integration

------------------------------------------------------------------------

# 15. Implementation Roadmap

## Phase 1

Repository setup

## Phase 2

Google Keep ingestion

## Phase 3

Metadata extraction

## Phase 4

Transcript/OCR

## Phase 5

Summarization

## Phase 6

Embeddings

## Phase 7

Hybrid retrieval

## Phase 8

UI

## Phase 9

Analytics

## Phase 10

Deployment

------------------------------------------------------------------------

# 16. Success Criteria

-   Keyword retrieval accuracy \>95%
-   Semantic retrieval of related concepts
-   Search latency \<2 seconds
-   Fully automated indexing
-   Zero-cost hosting
-   Modular architecture
