# New Jira Client (Next.js + FastAPI)

UI ลื่นแบบ Trello/Linear + Login ผ่าน **Jira (OAuth 2.0 3LO)**  
Deploy แนะนำ: **Frontend = Vercel**, **Backend = Railway**

## ✨ Features

- 🔐 **Jira OAuth 2.0 3LO**: Secure authentication with Jira
- 📊 **Board View**: Personal board with Jira status columns
- 🎯 **Drag & Drop**: Update issue status with smooth animations
- 🔍 **JQL Search**: Search issues using Jira Query Language
- ⚡ **Optimistic Updates**: Instant UI feedback
- 🎨 **Modern UI**: Built with Next.js 15 and TailwindCSS 4
- 🚀 **FastAPI Backend**: High-performance proxy server

## Project Structure

```
new-jira-client/
├─ frontend/          # Next.js 15 application
│  ├─ app/           # Next.js app directory
│  ├─ public/        # Static assets
│  └─ package.json   # Frontend dependencies
└─ backend/          # FastAPI application
   ├─ app/
   │  ├─ auth/       # OAuth 2.0 implementation
   │  ├─ webhooks/   # Jira webhook handlers
   │  ├─ utils/      # Jira client and transformers
   │  ├─ main.py     # FastAPI application
   │  ├─ models.py   # Pydantic models
   │  ├─ deps.py     # Dependencies
   │  └─ jira_proxy.py # Jira API proxy logic
   ├─ requirements.txt
   ├─ .env.example
   └─ railway.toml
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** for frontend
- **Python 3.8+** for backend
- **Jira Cloud** account with OAuth app configured

### 1. Clone Repository

```bash
git clone https://github.com/OmTanakorn/new-jira-client.git
cd new-jira-client
```

### 2. Setup Jira OAuth App

1. Go to https://developer.atlassian.com/console/myapps/
2. Create a new OAuth 2.0 (3LO) app
3. Add callback URL: `http://localhost:3000/auth/callback` (for development)
4. Enable required scopes: `read:jira-work`, `write:jira-work`, `offline_access`
5. Save the **Client ID** and **Client Secret**

### 3. Setup Backend

```bash
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Jira credentials:
# - JIRA_BASE_URL=https://your-domain.atlassian.net
# - JIRA_CLIENT_ID=your_client_id
# - JIRA_CLIENT_SECRET=your_client_secret
# - JIRA_REDIRECT_URI=http://localhost:3000/auth/callback
# - SECRET_KEY=your_random_secret_key

# Start backend server
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: http://localhost:8000

### 4. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## 🔧 Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Run with debug logging
DEBUG=true uvicorn app.main:app --reload --port 8000
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Lint code
npm run lint
```

## 📦 Deployment

### Deploy Backend on Railway

1. Create account at [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select `backend` directory as root
4. Configure environment variables in Railway dashboard
5. Deploy automatically on push

### Deploy Frontend on Vercel

1. Create account at [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Configure environment variables
5. Deploy automatically on push

## 🔐 Environment Variables

### Backend (.env)

```bash
# Jira Configuration
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_CLIENT_ID=your_jira_client_id
JIRA_CLIENT_SECRET=your_jira_client_secret
JIRA_REDIRECT_URI=http://localhost:3000/auth/callback

# FastAPI Configuration
FRONTEND_URL=http://localhost:3000
SECRET_KEY=your_secret_key_for_jwt

# Development
DEBUG=true
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main Endpoints

**Authentication**
- `GET /auth/login` - Initiate OAuth flow
- `POST /auth/callback` - Handle OAuth callback
- `GET /auth/me` - Get current user info

**Jira Operations**
- `GET /api/projects` - List accessible projects
- `POST /api/search` - Search issues with JQL
- `GET /api/issues/{key}` - Get issue details
- `PUT /api/issues/{key}/transition` - Change issue status
- `PUT /api/issues/{key}` - Update issue fields

**Webhooks**
- `POST /webhooks/jira` - Receive Jira webhooks

## 🔒 Security

- ✅ OAuth 2.0 for secure authentication
- ✅ JWT tokens for session management
- ✅ CORS protection
- ✅ All dependencies patched against known vulnerabilities
- ✅ CodeQL security scanning passed

## 🛠️ Technologies

**Frontend**
- Next.js 15.5 with App Router
- React 19
- TailwindCSS 4
- @dnd-kit for drag & drop
- TanStack Query for data fetching
- NextAuth.js for authentication

**Backend**
- FastAPI 0.109.1+
- Python 3.8+
- HTTPX for async HTTP
- Pydantic for validation
- python-jose for JWT

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.