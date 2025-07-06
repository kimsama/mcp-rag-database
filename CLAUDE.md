# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) database stack that provides a complete multi-database development environment using Docker Compose. The project combines Supabase (PostgreSQL with auth, real-time, and API stack) with Neo4j (graph database) for comprehensive database needs.

## Architecture

The project uses a hybrid approach:

1. **Supabase Integration**: Rather than defining all services locally, the project includes the official Supabase docker-compose.yml file and adds Neo4j as an additional service
2. **Environment Synchronization**: The setup script manages environment file synchronization between the root and Supabase directories
3. **Sparse Git Checkout**: Only the `/docker` directory from the Supabase repository is cloned to minimize disk usage

## Key Files

- `setup.py`: Bootstrap script that clones Supabase repo and prepares environment
- `docker-compose.yml`: Main compose file that includes Supabase services and adds Neo4j
- `.env.example`: Template with all required environment variables
- `supabase/docker/`: Contains the official Supabase Docker configuration (auto-cloned)

## Common Commands

### Initial Setup (Required First Time)
```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with secure passwords and keys

# Run setup script to clone Supabase and prepare environment
python setup.py
```

### Service Management
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f neo4j
docker compose logs -f supabase-studio

# Pull latest images
docker compose pull

# Full reset (destroys all data)
docker compose down -v --remove-orphans
```

### Development and Debugging
```bash
# Check service status
docker compose ps

# Access Neo4j browser
# http://localhost:7474

# Access Supabase Studio
# http://localhost:8000

# Connect to PostgreSQL directly
# Host: localhost, Port: 5432, Password: from .env

# Connect to Neo4j directly
# Bolt URL: bolt://localhost:7687, Auth: from NEO4J_AUTH in .env
```

## Service URLs and Ports

- **Supabase Studio**: http://localhost:8000 (main dashboard)
- **Neo4j Browser**: http://localhost:7474 (graph database UI)
- **PostgreSQL**: localhost:5432 (direct database connection)
- **Neo4j Bolt**: localhost:7687 (direct graph database connection)
- **Neo4j HTTPS**: localhost:7473 (secure web interface)

## Environment Configuration

Critical environment variables that must be configured:

- `POSTGRES_PASSWORD`: Main PostgreSQL database password
- `JWT_SECRET`: JWT signing secret (minimum 32 characters)
- `NEO4J_AUTH`: Neo4j credentials in format `username/password`
- `ANON_KEY` / `SERVICE_ROLE_KEY`: Supabase API keys
- `DASHBOARD_USERNAME` / `DASHBOARD_PASSWORD`: Supabase dashboard credentials

## Data Persistence

All data is stored in Docker volumes:
- `neo4j_data`: Neo4j database files
- `neo4j_logs`: Neo4j application logs
- `neo4j_conf`: Neo4j configuration
- `neo4j_plugins`: Neo4j plugins (includes Graph Data Science)
- Supabase volumes: Managed by included Supabase compose file

## Important Setup Notes

1. **First-time setup is mandatory**: You must run `python setup.py` before starting services
2. **Environment file sync**: The setup script automatically copies `.env` to `supabase/docker/.env`
3. **Neo4j plugins**: Graph Data Science plugin is pre-configured and enabled
4. **Supabase updates**: To update Supabase, run `cd supabase && git pull && cd ..`

## Troubleshooting

- If services fail to start, verify `.env` file exists and is properly configured
- For "repository not found" errors, delete the `supabase/` directory and re-run `python setup.py`
- For Neo4j connection issues, check that `NEO4J_AUTH` is in correct `username/password` format
- For Supabase issues, check that all required environment variables are set in `.env`