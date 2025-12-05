# SupportMax Pro v0.5 - Baseline Agent

## Overview

SupportMax Pro v0.5 is the baseline implementation of an AI-powered customer support system. It establishes the core agent architecture (Perception -> Reasoning -> Action) and enforces production constraints (latency, cost, tokens) from day one.

## Features

- **Core Agent Loop**: Perception, Reasoning, Action
- **Production Constraints**: Runtime checks for latency (<2s) and token usage
- **In-Memory Knowledge Base**: Keyword-based FAQ search
- **Basic Tooling**: Mock ticket creation
- **API**: FastAPI endpoints

## Prerequisites

- Python 3.10+
- `uv` package manager (recommended) or `pip`
- OpenAI or Anthropic API Key

## Quick Start (with uv)

We recommend using `uv` for fast, reliable dependency management.

### 1. Setup Environment

```bash
cd implementation/src/supportmax-pro/v0.5-baseline
cp .env.example .env
# Edit .env with your API keys
```

### 2. Install Dependencies

```bash
# Install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

### 3. Run the Application

Start the full system (API + Frontend) with a single command:
```bash
uv run python src/main.py
```

This commands will:
1. Start the FastAPI server on `http://localhost:8000`
2. Launch the Streamlit dashboard on `http://localhost:8501`

### 4. Test the API

You can also test directly via curl:

You can also test directly via curl:

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I reset my password?", "user_id": "user123"}'
```

## Docker Deployment

Alternatively, you can run with Docker:

```bash
docker-compose -f deployment/docker-compose.yml up --build
```

## Running Tests

```bash
pytest tests/ -v
```

## Directory Structure

- `src/agent`: Core agent logic
- `src/api`: FastAPI endpoints
- `src/config`: Configuration and constraints
- `src/knowledge`: FAQ data and retrieval
- `src/tools`: Ticket creation tools
