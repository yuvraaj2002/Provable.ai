# Google OAuth Implementation

This document describes the Google OAuth implementation using Authlib and session middleware.

## Overview

The application uses **Authlib** library for OAuth integration with **Starlette Session Middleware** for session management. This provides a secure, industry-standard OAuth flow.

## Architecture

### Components

1. **Session Middleware** (`app/main.py`)
   - Manages user sessions using encrypted cookies
   - Stores OAuth state tokens securely
   - Configured with `SECRET_KEY` for encryption

2. **OAuth Service** (`app/services/oauth_service.py`)
   - Initializes Authlib OAuth client
   - Registers Google OAuth provider
   - Uses OpenID Connect discovery endpoint

3. **Auth Endpoints** (`app/api/v1/endpoints/auth.py`)
   - `/auth/google/login` - Initiates OAuth flow
   - `/auth/google/callback` - Handles OAuth callback

## Flow

### 1. User Initiates Login

```
GET /api/v1/auth/google/login
```

- User clicks "Login with Google"
- Backend redirects to Google's authorization page
- State token is automatically managed by Authlib

### 2. Google Callback

```
GET /api/v1/auth/google/callback?code=...&state=...
```

- Google redirects back with authorization code
- Backend exchanges code for access/refresh tokens
- Fetches user info from Google
- Creates/updates user in database
- Stores OAuth tokens in `oauth_info` table
- Generates JWT token for API access
- Redirects to frontend with token

## Database Schema

### Users Table
- `id` - Primary key
- `name` - User's name
- `email` - User's email (unique)
- `profile_picture` - Profile picture URL
- `created_at`, `updated_at` - Timestamps

### OAuthInfo Table
- `id` - Primary key
- `user_id` - Foreign key to Users
- `provider_name` - "google" or "password"
- `provider_token_id` - Google user ID
- `access_token` - OAuth access token
- `refresh_token` - OAuth refresh token
- `expiry_at` - Token expiration time
- `created_at`, `updated_at` - Timestamps

## Configuration

### Environment Variables

```env
# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_SCOPES=openid email profile
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# Session (uses SECRET_KEY from main config)
SECRET_KEY=your-secret-key-for-sessions
```

### Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8000/api/v1/auth/google/callback`
6. Copy Client ID and Client Secret

## Usage

### Frontend Integration

```javascript
// Redirect user to Google login
window.location.href = 'http://localhost:8000/api/v1/auth/google/login';

// Handle callback (after redirect)
// Extract token from URL query params
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const userId = urlParams.get('user_id');

// Store token and redirect to app
localStorage.setItem('access_token', token);
window.location.href = '/dashboard';
```

### API Usage

After OAuth login, use the JWT token for API requests:

```javascript
fetch('http://localhost:8000/api/v1/auth/profile', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

## Security Features

1. **State Token Validation**
   - Authlib automatically validates state tokens
   - Prevents CSRF attacks

2. **Secure Session Storage**
   - Sessions encrypted with `SECRET_KEY`
   - HttpOnly cookies (via session middleware)
   - SameSite protection

3. **Token Storage**
   - OAuth tokens stored securely in database
   - Refresh tokens for long-term access
   - Token expiration handling

4. **JWT Tokens**
   - Short-lived access tokens
   - Stateless authentication
   - Secure token signing

## Error Handling

The implementation handles:
- Missing Google credentials
- Invalid authorization codes
- Network errors during token exchange
- Missing user email from Google
- Database errors

All errors are logged and return appropriate HTTP status codes.

## Testing

### Manual Testing

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Navigate to:
```
http://localhost:8000/api/v1/auth/google/login
```

3. Complete Google OAuth flow
4. Verify redirect with token
5. Use token for authenticated requests

### Test Endpoints

```bash
# Initiate login
curl http://localhost:8000/api/v1/auth/google/login

# Get profile (after login)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/v1/auth/profile
```

## Troubleshooting

### Common Issues

1. **"Google OAuth is not configured"**
   - Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`

2. **Redirect URI mismatch**
   - Ensure redirect URI in Google Console matches `GOOGLE_REDIRECT_URI`

3. **Session not persisting**
   - Check `SECRET_KEY` is set
   - Verify session middleware is added before CORS middleware

4. **Token exchange fails**
   - Check Google credentials are correct
   - Verify redirect URI matches exactly

## Future Enhancements

- [ ] Support for other OAuth providers (GitHub, Facebook)
- [ ] Token refresh endpoint
- [ ] OAuth token revocation
- [ ] Multi-provider account linking
- [ ] OAuth token encryption at rest

