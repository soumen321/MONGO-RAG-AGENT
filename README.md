# mongo-rag-agent

A production-ready retrieval-augmented generation (RAG) agent built on MongoDB, LangGraph, and LangChain.

## Project structure

- `src/mongo_rag_agent/`: Package source code
- `main.py`: Root entrypoint launcher for local execution
- `pyproject.toml`: Project metadata and package configuration
- `requirements.txt`: Development/runtime dependencies
- `tests/`: Unit tests and integration smoke tests

## Run locally

```bash
python main.py
```

## Package entrypoint

```bash
pip install -e .
mongo-rag-agent
```

## Notes

- Set `MONGODB_URI` and `OPENAI_API_KEY` in `.env`
- The agent uses MongoDB vector search and a documentation page lookup tool
- The graph workflow is managed through `langgraph`
