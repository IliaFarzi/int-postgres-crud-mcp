
# Task Management Application

## Overview

This project provides a **FastAPI application** for managing tasks, integrated with a **(MCP) server**. The system is containerized with PostgreSQL and designed with clear separation between domain logic, service abstraction, and API layers.

The architecture ensures:

- **Consistent type and data schema** between interfaces.
- **Service abstraction** over PostgreSQL queries using `psycopg`.
- Clear API lifecycle management using singleton pattern and dependency injection.
- Standalone MCP server capability.

---

## Tech Stack

- **Python 3.12**
- **FastAPI** (REST API server)
- **FastMCP** (mcp server)
- **dotenv** (environment variables)
- **psycopg** (PostgreSQL client)
- **pydantic** (data validation)
- **langchain[openai]** (agent integration)
- **langchain_mcp_adapters** (adapter for MCP tools)
- **PostgreSQL** (containerized database)

---

## Setup Instructions

### 1. Create a `.env` file

Create a `.env` in the project root. Example:

```env
POSTGRES_DB=task_mcp
POSTGRES_USER=root
POSTGRES_PASSWORD=123qwe123QWE
DATABASE_URL=postgresql://root:123qwe123QWE@postgres:5432/task_mcp
OPENAI_API_KEY=<your_openai_api_key_here>
PHOENIX_COLLECTOR_ENDPOINT=http://phoenix:6006
PHOENIX_ENABLE_TRACING=true
````

> **Hint:** The `DATABASE_URL` uses the Docker network hostname (`postgres`) instead of `localhost` because containers are connected over a Docker network.

---

### 2. Start the application

Build and run the containers:

```bash
docker-compose up -d --build
```

* `-d` runs containers in the background.
* `--build` rebuilds images in case of changes.

Check the REST API documentation at:

```
http://127.0.0.1:8000/docs
```

To inspect the MCP server:

```bash
npx @modelcontextprotocol/inspector python task_mcp_server.py
```

---

## Architecture

### Directory Overview

* **`domain/`** – Defines type and data schema, shared consistently between interfaces.
* **`service/`** – Contains library-dependent logic, e.g., `task_service.py` provides an abstraction over PostgreSQL queries using `psycopg`. Used by both tools and endpoints.
* **`app/`** – API layer:

  * `routes/` – Endpoint definitions.
  * `life_span.py` – Ensures singleton pattern for service dependencies, proper setup/teardown for API.
* **`main.py`** – Entry point for the FastAPI app, starts:

  * Task CRUD API
  * MCP server
  * Agent endpoints using MCP
* **`task_mcp_server.py`** – Can run as a standalone MCP server without `main.py`.

---

### Design Considerations

* **Service Abstraction:** Logic is centralized in `service` to avoid duplication between API and MCP server.
* **Singleton & Lifecycle Management:** FastAPI app uses `life_span.py` to ensure services are initialized once and properly cleaned up.
* **Containerized DB:** Postgres runs in a Docker container, connected to the app via a Docker network.

---

### Limitations

* Current tools are basic and may be extended with:

  * Text search
  * Semantic search for task fields
* Some duplication is expected between `task_router` and `task_mcp_server` logic due to:

  * Different error handling (`HTTPException` vs `ToolError`)
  * Different decorators for FastAPI vs FastMCP
* MCP server cannot benefit from singleton or dependency injection used in the API server because it runs in a separate process.

---

## Usage Notes

* Ensure `.env` credentials match between `POSTGRES_PASSWORD` and `DATABASE_URL`. Mismatch will cause authentication errors.
* Use `docker-compose down -v` to reset containers and database volumes if needed.

---
<p float="left">
  <img src="./imgs/1.png" width="400" />
  <img src="./imgs/2.png" width="400" />
</p>
<p float="left">
  <img src="./imgs/3.png" width="400" />
  <img src="./imgs/4.png" width="400" />
</p>
