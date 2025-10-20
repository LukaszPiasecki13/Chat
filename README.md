# Real-Time Chat Application

A modern real-time chat application built with Django REST Framework backend and React TypeScript frontend. The application features WebSocket-based live messaging with role-based permissions system.

## Features

- **Real-time messaging** using WebSockets (Django Channels)
- **Role-based permissions** (Player/Official roles)
- **Contact management system**
- **Message history** with persistent storage
- **Modern UI** built with Material-UI
- **RESTful API** for chat operations
- **Authentication system** with custom permissions
- **Responsive design** for cross-platform compatibility

## Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API framework
- **Django Channels** - WebSocket support for real-time features
- **SQLite** - Database (development)
- **Python 3.12** - Programming language

### Frontend
- **React 19** with TypeScript - Frontend framework
- **Material-UI (MUI)** - Component library
- **Vite** - Build tool and development server
- **Axios** - HTTP client for API calls
- **React Toastify** - Notifications

## Project Structure

```
Chat/
├── backend/                 # Django backend application
│   ├── chat/               # Main chat application
│   │   ├── models.py       # Database models (User, Profile, Message, Contact)
│   │   ├── consumers.py    # WebSocket consumers
│   │   ├── views.py        # API views
│   │   ├── serializers.py  # DRF serializers
│   │   ├── permissions.py  # Custom permissions
│   │   ├── routing.py      # WebSocket routing
│   │   └── management/commands/seed.py  # Database seeding
│   └── core/               # Django project settings
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript type definitions
│   └── package.json
└── README.md
```

## Models

### Profile
- Links Django User with role (Player/Official)
- Defines user permissions in the chat system

### Contact
- Manages relationships between users
- Ensures unique contact pairs

### Message
- Stores chat messages between users
- Includes sender, receiver, content, and timestamp

## Installation & Setup

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install django djangorestframework django-cors-headers channels
```

4. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Seed the database with test data:
```bash
python manage.py seed
```

6. Start the Django development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## Usage

1. Access the application at `http://localhost:5173` (frontend)
2. The backend API runs at `http://localhost:8000`
3. Select a user from the dropdown to simulate different users
4. Choose a contact from the contact list to start chatting
5. Messages are sent in real-time using WebSockets

## API Endpoints

- `GET /api/users/` - List all users
- `GET /api/contacts/{user_id}/` - Get user's contacts
- `GET /api/conversation/{user1_id}/{user2_id}/` - Get conversation history
- `POST /api/messages/` - Send a message
- `WebSocket /ws/chat/{room_name}/` - Real-time chat connection

## Permission System

The application implements a role-based permission system:
- **Players** can communicate with Officials
- **Officials** can communicate with Players
- Same role users cannot message each other directly

## Development

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend linting
cd frontend
npm run lint
```

### Building for Production
```bash
# Frontend build
cd frontend
npm run build
```
