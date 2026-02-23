* Atlas — Multi-Service Conversational AI System
Overview

Atlas is a modular conversational AI system built using LangChain, OpenAI, ChromaDB, and Gradio. The system integrates three distinct services behind a unified chat interface, demonstrating API integration, semantic retrieval, and function calling.

The architecture emphasizes modularity, testability, guardrails, and memory management.

* System Architecture

Atlas is structured into independent services that are routed through a central ChatEngine.

User (Gradio Chat UI)
        ↓
     Guardrails
        ↓
     Router
        ↓
 ┌───────────────┬────────────────┬──────────────────┐
 │ Service 1     │ Service 2      │ Service 3        │
 │ API Backend   │ Semantic Query │ Function Calling │
 └───────────────┴────────────────┴──────────────────┘
        ↓
     Response
Implemented Services
* Service 1 — API-Based Service

Backend: REST Countries API
Purpose: Provide structured country information

This service:

Calls a public API

Extracts structured data

Uses the LLM to transform the raw JSON into natural language

Never returns API output verbatim

Example:

Tell me about Germany
* Service 2 — Semantic Query Service

Backend: ChromaDB (persistent vector database)

This service:

Uses OpenAI embeddings

Stores embeddings in a persistent Chroma instance

Retrieves top-k relevant documents

Generates answers using retrieved context

Dataset:

A lightweight AI knowledge base (< 40MB)

Stored locally

Embeddings generated once and persisted

Example:

What are embeddings?
* Service 3 — Function Calling Service

Backend: OpenAI Function Calling

This service:

Uses tool binding in LangChain

Extracts structured arguments

Executes deterministic Python functions

Returns computed results

Supported operations:

Mean

Sum

Median

Standard Deviation

Example:

Compute the mean of 4, 8, 15, 16, 23, 42
* Conversational Interface

Built with Gradio ChatInterface.

Features:

Maintains short-term conversation memory

Distinct assistant personality ("Atlas")

Clean routing logic

Clear separation between UI and backend logic

* Guardrails

The system enforces:

Restricted Topics

The assistant will refuse to respond to:

Cats

Dogs

Horoscopes

Zodiac Signs

Taylor Swift

Prompt Injection Protection

The assistant refuses:

Attempts to reveal system prompts

Attempts to override instructions

Attempts to modify system behavior

Guardrails are enforced before LLM invocation for deterministic safety.

* Memory Management

Atlas implements short-term memory with:

Message history tracking

Automatic trimming to avoid context overflow

Independent memory inside the ChatEngine

The system does not rely on UI-level memory for LLM context.

* Project Structure
ATLAS_AI_agent (Run this, Jupyter Notebook)
AIAgent (source code)
chat_system/
│
├── app.py
├── knowledge_base.txt
│
└── src/
    ├── config.py
    ├── prompting.py
    ├── memory.py
    ├── guardrails.py
    ├── chat_engine.py
    ├── logging_utils.py
    │
    └── services/
        ├── api_service.py
        ├── semantic_service.py
        ├── function_service.py
        ├── build_vector_store.py