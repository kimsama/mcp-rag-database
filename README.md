# MCP Database Setup

A minimal Docker Compose setup providing both Supabase and Neo4j for MCP (Model Context Protocol) database needs.

## Services Included

- **Supabase**: Complete PostgreSQL database with auth, real-time, and API stack
- **Neo4j**: Graph database with Graph Data Science plugin

## Quick Start

1. Copy environment file and configure:
   ```bash
   cp .env.example .env
   # Edit .env with your secure passwords and keys
   ```

2. Run setup script (first time only):
   ```bash
   python setup.py
   ```
   This will:
   - Clone the Supabase repository with sparse checkout
   - Copy your .env file to the Supabase docker directory
   - Verify everything is ready

3. Start services:
   ```bash
   docker compose up -d
   ```

## Service URLs

- **Supabase Studio**: http://localhost:8000
- **Neo4j Browser**: http://localhost:7474
- **PostgreSQL**: localhost:5432
- **Neo4j Bolt**: localhost:7687

## Environment Configuration

Key variables to update in `.env`:

- `POSTGRES_PASSWORD`: PostgreSQL database password
- `NEO4J_AUTH`: Neo4j username/password (format: `username/password`)
- `JWT_SECRET`: JWT secret for Supabase auth
- Supabase API keys (`ANON_KEY`, `SERVICE_ROLE_KEY`)

## Data Persistence

All data is stored in Docker volumes:
- `neo4j_data`: Neo4j database files
- `neo4j_logs`: Neo4j logs
- Supabase volumes: Managed by included Supabase compose file

## Commands

```bash
# Initial setup (first time only)
python setup.py

# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Pull latest images
docker compose pull

# Update Supabase (if needed)
cd supabase && git pull && cd ..
```

## Important Notes

- **First time setup**: You MUST run `python setup.py` before starting services
- **Supabase dependency**: The docker-compose.yml includes Supabase via the cloned repository
- **Environment sync**: Your .env file is automatically copied to supabase/docker/.env
- **Project name**: All services use the "mcp-database" project name for unified management