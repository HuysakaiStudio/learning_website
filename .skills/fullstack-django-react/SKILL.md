---
name: fullstack-django-react
description: Expert skill for developing full-stack applications using Django backend with React frontend, including database design, API development, and deployment best practices
license: MIT
metadata:
  author: learning-web-project
  version: "1.0.0"
allowed-tools: Read Write Search ListFiles
---

# Full-Stack Django-React Developer Skill

## Overview
This skill provides comprehensive guidance for developing full-stack web applications using Django as the backend and React as the frontend. It covers best practices for API design, database modeling, authentication, deployment, and integration patterns between Django and React.

## Technology Stack
- **Backend**: Django 5.x with Django REST Framework
- **Frontend**: React 18+ with modern patterns
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Django sessions/JWT tokens
- **Deployment**: Docker, Heroku, Vercel, or similar platforms

## Core Capabilities

### 1. Project Setup and Configuration

#### Django Backend Setup
- Configure settings for both development and production
- Set up CORS for React frontend communication
- Configure static and media file handling
- Database configuration and optimization

#### React Frontend Setup
- Create React App or Next.js project
- Configure proxy for development
- Set up API client utilities
- Authentication and state management

### 2. API Development Best Practices

#### Django REST Framework Patterns
```python
# Use serializers for data transformation
from rest_framework import serializers

class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = YourModel
        fields = '__all__'

# Use ViewSets for standard CRUD operations
from rest_framework import viewsets

class ExampleViewSet(viewsets.ModelViewSet):
    queryset = YourModel.objects.all()
    serializer_class = ExampleSerializer
```

#### API Endpoint Design
- Follow RESTful conventions
- Use consistent naming patterns
- Implement proper HTTP status codes
- Handle errors gracefully

### 3. Database Modeling
- Design efficient database schemas
- Implement proper relationships
- Optimize queries with select_related/prefetch_related
- Handle migrations properly

### 4. Authentication and Authorization
- Implement secure authentication flows
- Handle JWT tokens if required
- Implement role-based permissions
- Secure API endpoints

### 5. Frontend-Backend Integration
- Set up proper CORS configuration
- Handle API calls efficiently
- Implement loading states and error handling
- Manage state synchronization

## Django Settings Configuration

### CORS Configuration
```python
# Add to requirements.txt
django-cors-headers>=4.0.0

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
    'rest_framework',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    # ... other middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# For production, be more specific with origins
# CORS_ALLOWED_ORIGINS = [
#     "https://yourdomain.com",
# ]

# Allow credentials to be sent with requests
CORS_ALLOW_CREDENTIALS = True
```

### REST Framework Configuration
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

## React Integration Patterns

### API Client Setup
```javascript
// api/client.js
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com/api/' 
  : 'http://localhost:8000/api/';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        ...options.headers,
      },
      credentials: 'include', // Important for Django sessions
      ...options,
    };

    // Add CSRF token for mutations
    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(options.method)) {
      const csrfToken = this.getCsrfToken();
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken;
      }
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
  }

  getCsrfToken() {
    return document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
  }
}

export default new ApiClient();
```

### Authentication Hook
```javascript
// hooks/useAuth.js
import { useState, useEffect } from 'react';
import apiClient from '../api/client';

export const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await apiClient.request('auth/me/');
        setUser(data.user);
      } catch (error) {
        console.error('Failed to fetch user:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const login = async (credentials) => {
    const data = await apiClient.request('auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    if (data.success) {
      setUser(data.user);
    }
    
    return data;
  };

  const logout = async () => {
    await apiClient.request('auth/logout/', { method: 'POST' });
    setUser(null);
  };

  return { user, loading, login, logout };
};
```

## Deployment Strategies

### Backend Deployment
- Use environment variables for configuration
- Configure static file serving (WhiteNoise or CDN)
- Set up proper logging
- Implement health checks

### Frontend Deployment
- Build optimization and code splitting
- Environment-specific configurations
- Asset optimization
- Cache management

## Common Patterns and Solutions

### Handling CSRF Tokens
- Django's CSRF protection requires special handling with AJAX requests
- Include CSRF tokens in POST/PUT/PATCH/DELETE requests
- Use Django's CSRF cookie mechanism

### File Uploads
- Handle multipart form data properly
- Implement progress indicators
- Validate file types and sizes
- Secure file storage

### Real-time Features
- Consider Django Channels for WebSocket support
- Use Server-Sent Events for simpler cases
- Implement polling strategies when needed

## Troubleshooting

### Common Issues
- CORS errors: Verify origin configuration
- CSRF errors: Check token inclusion in requests
- Authentication: Ensure session cookies are handled properly
- Static files: Verify serving configuration in production

### Debugging Tips
- Use browser developer tools to inspect network requests
- Check Django logs for backend errors
- Enable Django debug toolbar for development
- Use React DevTools for frontend debugging