# Chat Application - Docker Setup

This repository contains a full-stack chat application with Django backend (using Django Channels for WebSockets) and React frontend.

## Docker Configuration

The application includes several Docker configurations:

### Files Created:
- `backend/Dockerfile` - Production Django backend with Daphne server
- `frontend/Dockerfile` - Production React frontend with Nginx
- `frontend/nginx.conf` - Nginx configuration with API and WebSocket proxying
- `docker-compose.yml` - Production environment
- `.dockerignore` files for both frontend and backend

## Quick Start

### Production Environment
```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# Redis: localhost:6379
```

## Architecture

### Services:
1. **Backend** (Django + Channels)
   - Runs on port 8000
   - Uses Daphne ASGI server for WebSocket support
   - Includes Redis for WebSocket message passing
   - Auto-runs migrations and seed data

2. **Frontend** (React + Vite)
   - Production: Nginx on port 80
   - Includes API and WebSocket proxying

3. **Redis**
   - Used by Django Channels for WebSocket communication
   - Runs on port 6379

## Commands

### Build specific service:
```bash
docker-compose build backend
docker-compose build frontend
```

### Run in background:
```bash
docker-compose up -d
```

### View logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop services:
```bash
docker-compose down
```

### Reset everything:
```bash
docker-compose down -v --remove-orphans
docker system prune -a
```

## Environment Variables

You can customize the setup by creating a `.env` file in the root directory:

```env
# Backend
DEBUG=0
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://redis:6379/0

# Frontend
VITE_API_URL=http://localhost:8000
```

## Features

- **Production-ready**: Multi-stage builds, optimized images
- **WebSocket support**: Proper proxying for real-time chat
- **Static file serving**: Nginx handles frontend assets
- **Health checks**: Auto-restart on failures
- **Data persistence**: Redis data volume for chat history
