# NeuraList Project Structure

This document describes the reorganized project structure following industry best practices.

## Directory Structure

```
NeuraList/
├── app/                          # Main application package
│   ├── main.py                   # FastAPI application entry point
│   ├── api/                      # API endpoints
│   │   └── v1/                   # API version 1
│   │       ├── api.py            # API router aggregation
│   │       └── endpoints/        # Route handlers
│   │           ├── agent.py      # Agent/chatbot endpoints
│   │           ├── auth.py       # Authentication endpoints
│   │           └── tasks.py      # Task management endpoints
│   │
│   ├── agents/                   # Multi-agent system (new)
│   │   ├── README.md             # Agent documentation
│   │   ├── base/                 # Base agent classes
│   │   ├── definitions/          # Agent implementations
│   │   ├── factory.py            # Agent factory
│   │   ├── orchestrator/         # Agent orchestration
│   │   ├── registry/             # Agent registry
│   │   └── tools/                # Agent tools
│   │
│   ├── core/                     # Core application logic
│   │   ├── config.py             # Configuration settings
│   │   ├── logging_config.py     # Logging setup
│   │   └── security.py           # Security utilities (JWT, etc.)
│   │
│   ├── db/                       # Database layer
│   │   ├── base.py               # Database base configuration
│   │   └── session.py             # Database session management
│   │
│   ├── legacy_agent/             # Legacy agent system (deprecated)
│   │   ├── agent_memory.py
│   │   ├── agent_prompts.py
│   │   ├── chatbot.py
│   │   ├── llm_inference.py
│   │   └── mcp_client.py
│   │
│   ├── models/                   # Database models (SQLModel)
│   │   ├── agent_model.py
│   │   ├── auth_model.py         # User model
│   │   └── tasks_model.py        # Task model
│   │
│   ├── schemas/                  # API request/response schemas
│   │   ├── auth.py               # Auth schemas (SignUp, Login, etc.)
│   │   └── tasks.py              # Task schemas (AddTaskRequest, etc.)
│   │
│   ├── services/                 # Business logic services
│   │   ├── oauth_service.py      # OAuth operations service
│   │   ├── redis_service.py      # Redis operations service
│   │   └── user_service.py       # User operations service
│   │
│   └── utils/                    # Utility functions
│       └── password.py           # Password hashing utilities
│
├── docs/                         # Documentation
│   ├── AI Feature.md
│   ├── AI ratelimit.md
│   ├── Chatbot.md
│   ├── CONFIG.md
│   └── OAUTH.md
│
├── migrations/                   # Alembic database migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│
├── notebooks/                    # Jupyter notebooks for experimentation
│   ├── Agents.ipynb
│   ├── graphiti.ipynb
│   └── rabbit_mq.ipynb
│
├── scripts/                      # Utility scripts
│   ├── deploy.py
│   ├── rabbit_mq_consume.py
│   └── rabbit_mq_produce.py
│
├── tests/                        # Test files
│   ├── auth_api.http             # HTTP test files
│   └── unit/                     # Unit tests
│
├── alembic.ini                   # Alembic configuration
├── pyproject.toml                # Project dependencies
├── uv.lock                       # Dependency lock file
├── PRD.md                        # Product Requirements Document
├── PROJECT_STRUCTURE.md          # This file
└── README.md                     # Project documentation

```

## Key Changes Made

### 1. **Separation of Concerns**
   - **`app/models/`**: Contains only database models (SQLModel tables)
   - **`app/schemas/`**: Contains API request/response schemas (Pydantic models)
   - **`app/services/`**: Contains business logic services (OAuthService, RedisService, UserService)
   - **`app/utils/`**: Contains utility functions (password hashing)

### 2. **Legacy Code Organization**
   - Moved old `app/agent/` → `app/legacy_agent/` for backward compatibility
   - Kept for reference but marked as deprecated

### 3. **Test Organization**
   - Created `tests/unit/` for unit tests
   - Moved test scripts to `scripts/`
   - Moved notebooks to `notebooks/`

### 4. **Clean Structure**
   - Removed temporary files (`temp.py`)
   - Removed redundant code (`app/core/agent.py`)
   - Consolidated utilities into proper locations

## Import Patterns

### Models (Database)
```python
from app.models.auth_model import User
from app.models.tasks_model import Task
```

### Schemas (API)
```python
from app.schemas.auth import SignUpRequest, LoginRequest
from app.schemas.tasks import AddTaskRequest
```

### Services
```python
from app.services.oauth_service import OAuthService
from app.services.redis_service import RedisService
from app.services.user_service import UserService
```

### Utils
```python
from app.utils.password import hash_password, verify_password
```

## Best Practices Followed

1. ✅ **Separation of Models and Schemas**: Database models separate from API schemas
2. ✅ **Service Layer**: Business logic in services, not endpoints
3. ✅ **Utility Functions**: Reusable utilities in dedicated folder
4. ✅ **Legacy Code**: Old code preserved but clearly marked
5. ✅ **Test Structure**: Proper test organization
6. ✅ **Documentation**: Clear folder structure with purpose

## Next Steps

- Consider adding integration tests in `tests/integration/`
- Add service layer for task operations
- Consider adding repository pattern for database access
- Add proper error handling schemas

