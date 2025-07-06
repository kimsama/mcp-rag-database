# Docker Network Setup for MCP Services

This document provides instructions for connecting the mcp-database and mcp-crawl4ai-rag Docker containers using Docker networks.

## Overview

The mcp-database container provides Supabase (PostgreSQL + API) and Neo4j services that the mcp-crawl4ai-rag container needs to access. This guide shows how to connect them using Docker networking.

## Current Services

**mcp-database container provides:**
- Supabase API: `supabase-kong` container on port 8000
- PostgreSQL: `supabase-db` container on port 5432  
- Neo4j: `neo4j` container on ports 7687 (bolt) and 7474 (browser)

**mcp-crawl4ai-rag container needs:**
- Access to Supabase API for vector storage
- Access to Neo4j for knowledge graph functionality

## Solution 1: Shared Docker Network (Recommended)

### Step 1: Create Shared Network

```bash
docker network create mcp-network
```

### Step 2: Update mcp-database Configuration

Add network configuration to the root `docker-compose.yml`:

```yaml
# Add to the end of /mnt/d/dev/my-github/mcp-database/docker-compose.yml
networks:
  default:
    name: mcp-network
    external: true
```

### Step 3: Start mcp-database Services

```bash
cd /mnt/d/dev/my-github/mcp-database
docker compose down  # Stop existing services
docker compose up -d  # Start with new network
```

### Step 4: Update Environment Variables

In your mcp-crawl4ai-rag `.env` file, use container names instead of localhost:

```env
# Database connections using container names
SUPABASE_URL=http://supabase-kong:8000
SUPABASE_SERVICE_KEY=your_service_key

# Neo4j connection using container name
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Other required variables
OPENAI_API_KEY=your_openai_key
MODEL_CHOICE=gpt-4-turbo
USE_KNOWLEDGE_GRAPH=true
# ... etc
```

### Step 5: Run mcp-crawl4ai-rag with Network

```bash
cd /mnt/d/dev/my-github/mcp-crawl4ai-rag
docker run --network mcp-network --env-file .env -p 8051:8051 mcp/crawl4ai-rag
```

## Solution 2: Docker Compose Integration

Create a docker-compose override in the mcp-crawl4ai-rag directory:

```yaml
# Create: /mnt/d/dev/my-github/mcp-crawl4ai-rag/docker-compose.override.yml
services:
  crawl4ai-mcp:
    build: .
    container_name: mcp-crawl4ai-rag
    ports:
      - "8051:8051"
    depends_on:
      - supabase-kong
      - neo4j
    environment:
      SUPABASE_URL: http://supabase-kong:8000
      NEO4J_URI: bolt://neo4j:7687
    networks:
      - mcp-network
    env_file:
      - .env

networks:
  mcp-network:
    external: true
```

Then run:
```bash
cd /mnt/d/dev/my-github/mcp-crawl4ai-rag
docker compose up -d
```

## Solution 3: Host Network Mode (Alternative)

If you prefer to use host networking:

```bash
cd /mnt/d/dev/my-github/mcp-crawl4ai-rag
docker run --network host --env-file .env mcp/crawl4ai-rag
```

With host networking, use localhost addresses:
```env
SUPABASE_URL=http://localhost:8000
NEO4J_URI=bolt://localhost:7687
```

## Verification

### Check Network Connectivity

1. **Verify network exists:**
   ```bash
   docker network ls | grep mcp-network
   ```

2. **Check containers on network:**
   ```bash
   docker network inspect mcp-network
   ```

3. **Test connectivity from crawl4ai container:**
   ```bash
   # Get into the crawl4ai container
   docker exec -it mcp-crawl4ai-rag /bin/bash
   
   # Test Supabase connection
   curl http://supabase-kong:8000/health
   
   # Test Neo4j connection (if nc is available)
   nc -zv neo4j 7687
   ```

### Service Health Checks

Monitor service health:
```bash
# Check all containers
docker ps

# Check logs for connectivity issues
docker logs mcp-crawl4ai-rag
docker logs supabase-kong
docker logs neo4j
```

## Container Service Names

When using Docker networks, reference services by their container names:

| Service | Container Name | Internal Port | External Port |
|---------|---------------|---------------|---------------|
| Supabase API | `supabase-kong` | 8000 | 8000 |
| PostgreSQL | `supabase-db` | 5432 | 5432 |
| Neo4j Bolt | `neo4j` | 7687 | 7687 |
| Neo4j Browser | `neo4j` | 7474 | 7474 |
| Supabase Studio | `supabase-studio` | 3000 | 8000 (via kong) |

## Troubleshooting

### Common Issues

1. **Connection refused errors:**
   - Ensure both containers are on the same network
   - Check that services are healthy: `docker ps`
   - Verify container names match environment variables

2. **DNS resolution errors:**
   - Confirm network exists: `docker network ls`
   - Check containers are attached: `docker network inspect mcp-network`

3. **Environment variable issues:**
   - Use container names (not localhost) when containers are networked
   - Verify .env file is properly loaded

### Reset Network

If you need to start fresh:
```bash
# Stop all services
cd /mnt/d/dev/my-github/mcp-database
docker compose down

cd /mnt/d/dev/my-github/mcp-crawl4ai-rag
docker stop mcp-crawl4ai-rag

# Remove and recreate network
docker network rm mcp-network
docker network create mcp-network

# Restart services
cd /mnt/d/dev/my-github/mcp-database
docker compose up -d
```

## Security Considerations

- The shared network isolates MCP services from other Docker containers
- Services are only accessible within the network unless ports are explicitly exposed
- Use proper authentication credentials for database connections
- Consider using Docker secrets for sensitive environment variables in production

## Next Steps

Once networking is configured:
1. Test basic connectivity between containers
2. Verify Supabase vector operations work
3. Test Neo4j knowledge graph functionality
4. Run end-to-end crawling and RAG operations