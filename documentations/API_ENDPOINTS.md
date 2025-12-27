# API Endpoints

## Users

| Endpoint | Method | Description | Input | Output |
|----------|--------|-------------|-------|--------|
| `/` | GET | Root endpoint | None | `{"message": "Welcome to the AI Safety Application!"}` |
| `/api/v1/users/google-login` | GET | Initiate Google OAuth login | None | Redirect to Google OAuth |
| `/api/v1/users/google-callback` | GET | Google OAuth callback | Query: OAuth code | `{"access_token": "string"}` |
| `/api/v1/users/login` | POST | User login with email/password | Body: `{"email": "string", "password": "string"}` | `{"access_token": "string"}` |
| `/api/v1/users/signup` | POST | Create new user account | Body: `{"email": "string", "password": "string", "username": "string"}` | `{"message": "Verification mail has been sent..."}` |
| `/api/v1/users/verify-mail` | GET | Verify email address | Query: `token` (string) | `{"message": "Email verified successfully..."}` |
| `/api/v1/users/me` | GET | Get current user info | Header: `Authorization: Bearer <token>` | User object |

## API Keys

| Endpoint | Method | Description | Input | Output |
|----------|--------|-------------|-------|--------|
| `/api/v1/api_keys` | POST | Create new API key | Header: `Authorization: Bearer <token>`<br>Body: `{"key_name": "string"}` | `{"api_key": "string", "message": "API key created successfully"}` |
| `/api/v1/api_keys` | GET | Get all user's API keys | Header: `Authorization: Bearer <token>` | `{"api_keys": [{"id": "string", "key_name": "string", "last_4_digit": "string", "created_at": "string"}]}` |
| `/api/v1/api_keys/{key_id}` | DELETE | Delete API key | Header: `Authorization: Bearer <token>`<br>Path: `key_id` (string) | `{"message": "API key deleted successfully"}` |

## Authentication

All protected endpoints require `Authorization: Bearer <token>` header. Token obtained from login endpoints.

