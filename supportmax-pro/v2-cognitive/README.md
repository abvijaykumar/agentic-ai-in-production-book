# SupportMax Pro v2 - Cognitive Enhancement

## Overview

Version 2 adds production-grade memory, context management, and framework-based orchestration for complex multi-step problem solving. This version introduces sophisticated cognitive capabilities enabling complex customer issues requiring coordinated specialist agents.

## Key New Features

### Cognitive Capabilities
- **Distributed Memory**: Redis Cluster + Mem0 for production-scale memory management
- **LangGraph Orchestration**: State machine-based workflows for complex reasoning
- **CrewAI Multi-Agent**: Coordinated specialist agents (billing, technical, account)
- **Knowledge Graph**: Neo4j for entity relationships and contextual reasoning
- **Advanced RAG**: Hybrid search with reranking and query decomposition
- **Dynamic Context**: Intelligent context pruning and summarization
- **LangSmith Observability**: Comprehensive tracing and debugging

### Enhanced from v1
- All v1 features (persistent storage, multi-turn chat, integrations)
- 10x throughput: 1,000-5,000 tickets/day
- 80% automation rate (vs 70% in v1)
- Sub-5-second response times
- Complex multi-step issue resolution

## Technology Stack

**Frameworks**: LangGraph, CrewAI, Mem0  
**Memory**: Redis Cluster, Neo4j, Pinecone/Weaviate  
**LLMs**: GPT-4, Claude Sonnet  
**Observability**: LangSmith, Prometheus, Grafana  
**Infrastructure**: Kubernetes, Helm

## Architecture

```
LangGraph Orchestrator (State Machines)
    ↓
CrewAI Coordinator (Multi-Agent)
    ↓
Specialist Agents (Billing, Technical, Account)
    ↓
Memory Layer (Mem0)
    ├── Episodic (Redis Cluster)
    ├── Semantic (Pinecone/Weaviate)
    └── Knowledge Graph (Neo4j)
```

## Quick Start

### Docker Compose
```bash
cd implementation/src/v2-cognitive
cp .env.example .env
docker-compose up --build
```

### Kubernetes
```bash
helm install supportmax-v2 ./deployment/helm/supportmax-v2 \
  --namespace supportmax --create-namespace
```

### Local Development (with uv)

```bash
# 1. Setup environment and install dependencies
uv sync
source .venv/bin/activate

# 2. Run Application
python src/api/endpoints.py
```

## Core Concepts

### 1. Three-Tier Memory
- **Episodic**: Short-term conversations (Redis, < 10ms)
- **Semantic**: Long-term knowledge (Vector DB, < 100ms)
- **Procedural**: Workflows and skills (PostgreSQL + cache)

### 2. LangGraph State Machines
Complex workflows orchestrated as state machines with conditional branching.

### 3. Specialist Agents
Domain experts (billing, technical, account) collaborate via CrewAI.

### 4. Knowledge Graph
Neo4j stores entity relationships for contextual reasoning.

## Configuration

See `.env.example` for:
- Memory configuration (Redis Cluster, Mem0)
- Agent settings (LangGraph, CrewAI)
- Vector store (Pinecone/Weaviate)
- Knowledge graph (Neo4j)
- Observability (LangSmith)

## API Endpoints

- `POST /v2/chat/stream` - Stream responses with state updates
- `GET /v2/memory/{user_id}` - User memory context
- `POST /v2/workflow/execute` - Execute custom workflows
- `GET /v2/agents/status` - Specialist agent status

## Capabilities

- **Throughput**: 1,000-5,000 tickets/day
- **Automation**: 80% resolution rate
- **Response Time**: < 5 seconds average
- **Complex Issues**: Multi-step, multi-agent coordination
- **Memory**: 50+ message conversation history
- **Context**: Dynamic optimization up to 8K tokens

## Deployment

**Kubernetes Resources**:
- 3+ orchestrator pods
- 3-node Redis Cluster
- 3-node Neo4j cluster
- Managed vector store
- HPA for auto-scaling

## Migration from v1

1. Migrate conversations to episodic memory
2. Rebuild knowledge graph with relationships
3. Configure specialist agents
4. Deploy memory infrastructure

All v1 endpoints remain compatible.

## Performance vs Previous Versions

| Metric         | v0.5 | v1      | v2          |
| -------------- | ---- | ------- | ----------- |
| Daily Capacity | 50   | 500     | 5,000       |
| Automation     | 60%  | 70%     | 80%         |
| Response Time  | 2s   | 30s     | 5s          |
| Complex Issues | ❌    | Limited | ✅           |
| Memory         | None | Session | Distributed |
| Multi-Agent    | ❌    | ❌       | ✅           |

## Documentation

- [Implementation Guide](IMPLEMENTATION_GUIDE.md)
- [Memory Architecture](docs/memory_architecture.md)
- [Agent Configuration](docs/agent_configuration.md)
- [Deployment Guide](docs/deployment_guide.md)

## Next Steps

To v3 (Enterprise Integration):
- MCP gateway
- Multi-platform agents (OpenAI, Anthropic, Microsoft, Google)
- Enterprise SSO
- Service mesh

## License

MIT License