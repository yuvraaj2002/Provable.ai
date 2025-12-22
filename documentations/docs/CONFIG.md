# Configuration Management

This document describes the centralized configuration system using `pydantic-settings`.

## Overview

All environment variables are now managed through `app/core/config.py` using `pydantic-settings`. This provides:
- Type safety and validation
- Centralized configuration
- Automatic loading from `.env` file
- Default values where appropriate
- Cached settings instance for performance

## Configuration File

The main configuration is in `app/core/config.py`:

```python
from app.core.config import settings

# Access any setting
database_url = settings.DATABASE_URL
secret_key = settings.SECRET_KEY
```

## Environment Variables

### Required Variables

- `DATABASE_URL` - PostgreSQL database connection string
- `SECRET_KEY` - Secret key for JWT token signing (must not be default value)

### Optional Variables (with defaults)

- `ALGORITHM` - JWT algorithm (default: `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time (default: `30`)
- `REDIS_URL` - Redis connection URL
- `MAX_REDIS_CONNECTIONS` - Max Redis connections (default: `10`)
- `CONTEXT_WINDOW_LENGTH` - Context window size (default: `20`)
- `OPENAI_API_KEY` - OpenAI API key
- `DEFAULT_AGENT_MODEL` - Default LLM model (default: `gpt-4o-mini`)
- `MAX_MESSAGES` - Max messages in history (default: `20`)
- `GEMINI_KEYS` - Comma-separated Gemini API keys
- `LLM_MODEL` - LLM model name
- `MCP_SERVER_URL` - MCP server URL (default: `http://localhost:8001/mcp`)
- `GOOGLE_CLIENT_ID` - Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth Client Secret
- `GOOGLE_SCOPES` - Google OAuth scopes (space-separated, default: `openid email profile`)
- `GOOGLE_REDIRECT_URI` - Google OAuth redirect URI
- `GOOGLE_AUTH_URL` - Google OAuth authorization URL (default: `https://accounts.google.com/o/oauth2/v2/auth`)
- `GOOGLE_TOKEN_URL` - Google OAuth token URL (default: `https://oauth2.googleapis.com/token`)
- `GOOGLE_USERINFO_URL` - Google userinfo URL (default: `https://www.googleapis.com/oauth2/v2/userinfo`)
- `MAX_AGENT_ITERATIONS` - Max agent handoffs (default: `3`)
- `BACKEND_CORS_ORIGINS` - CORS origins (comma-separated)
- `DB_ECHO` - SQL query logging (default: `True`)

## Usage Examples

### In Your Code

```python
from app.core.config import settings

# Database
database_url = settings.DATABASE_URL

# Security
secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM

# Redis
redis_url = settings.REDIS_URL
max_connections = settings.MAX_REDIS_CONNECTIONS

# OpenAI
openai_key = settings.OPENAI_API_KEY
model = settings.DEFAULT_AGENT_MODEL

# Gemini (parsed list)
gemini_keys = settings.gemini_keys_list  # Returns List[str]

# Google OAuth
google_client_id = settings.GOOGLE_CLIENT_ID
google_scopes = settings.google_scopes_list  # Returns List[str]
redirect_uri = settings.GOOGLE_REDIRECT_URI
auth_url = settings.GOOGLE_AUTH_URL
```

### Property Methods

The config includes helper properties:

- `settings.gemini_keys_list` - Parses comma-separated `GEMINI_KEYS` into a list
- `settings.google_scopes_list` - Parses space-separated `GOOGLE_SCOPES` into a list

### Validation

The config automatically validates:
- `SECRET_KEY` must be set and not the default value
- `DATABASE_URL` must be set

## Files Updated

All files have been updated to use the centralized config:

- ✅ `app/core/security.py` - JWT settings
- ✅ `app/services/redis_service.py` - Redis settings
- ✅ `app/db/session.py` - Database settings
- ✅ `app/main.py` - CORS settings
- ✅ `app/legacy_agent/llm_inference.py` - Gemini/LLM settings
- ✅ `app/legacy_agent/mcp_client.py` - MCP settings
- ✅ `app/agents/factory.py` - Already using settings
- ✅ `migrations/env.py` - Database URL (with fallback)

## Migration from Old Code

### Before:
```python
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "default")
```

### After:
```python
from app.core.config import settings

database_url = settings.DATABASE_URL
secret_key = settings.SECRET_KEY
```

## Benefits

1. **Type Safety**: Pydantic validates types automatically
2. **Centralized**: All config in one place
3. **Validation**: Automatic validation on startup
4. **Performance**: Cached settings instance
5. **Documentation**: Self-documenting with type hints
6. **Default Values**: Sensible defaults where appropriate

## Environment File

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/neuralist
SECRET_KEY=your-secret-key-here
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your-openai-key
# ... etc
```

The config automatically loads from `.env` file.

