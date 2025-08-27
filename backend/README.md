# Backend - FastAPI Proxy Server

FastAPI proxy server สำหรับ New Jira Client ที่ทำหน้าที่เป็นตัวกลางระหว่าง Frontend กับ Jira API 
รวมถึงรองรับ Webhook จาก Jira สำหรับการอัปเดตแบบ real-time

## ✨ ฟีเจอร์หลัก

- **Jira API Proxy**: ซ่อนและรวม logic ที่ซับซ้อน (batch updates, field mapping)
- **OAuth 2.0 3LO**: จัดการ authentication กับ Jira
- **Webhook Handler**: รับและประมวลผล Jira webhooks สำหรับการอัปเดตแบบ real-time
- **Data Transformation**: แปลงข้อมูลจาก Jira ให้เหมาะกับ Frontend
- **Optimistic Updates**: รองรับการอัปเดตแบบ optimistic ของ drag & drop

## 🏗️ โครงสร้างโปรเจกต์

```
backend/
├─ app/
│  ├─ main.py           # FastAPI app และ routes หลัก
│  ├─ deps.py           # Dependencies และ middleware
│  ├─ jira_proxy.py     # Jira API proxy logic
│  ├─ models.py         # Pydantic models
│  ├─ auth/
│  │  ├─ oauth.py       # Jira OAuth 2.0 3LO
│  │  └─ middleware.py  # Authentication middleware
│  ├─ webhooks/
│  │  ├─ handlers.py    # Webhook event handlers
│  │  └─ validators.py  # Webhook payload validation
│  └─ utils/
│     ├─ jira_client.py # Jira API client
│     └─ transformers.py # Data transformation utilities
├─ requirements.txt     # Python dependencies
├─ .env.example        # Environment variables template
└─ railway.toml        # Railway deployment config
```

## 📦 Dependencies

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
httpx>=0.25.0
python-dotenv>=1.0.0
pydantic>=2.4.0
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.6
```

## 🚀 การติดตั้งและเริ่มต้น

### 1. ติดตั้ง Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. ตั้งค่า Environment Variables

```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env`:

```env
# Jira Configuration
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_CLIENT_ID=your_jira_client_id
JIRA_CLIENT_SECRET=your_jira_client_secret
JIRA_REDIRECT_URI=http://localhost:3000/auth/callback

# FastAPI Configuration
FRONTEND_URL=http://localhost:3000
SECRET_KEY=your_secret_key_for_jwt

# Database (optional, for caching/sessions)
DATABASE_URL=sqlite:///./app.db

# Development
DEBUG=true
```

### 3. เริ่มต้น Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

API จะพร้อมใช้งานที่: http://localhost:8000

## 🔗 API Endpoints

### Authentication
- `GET /auth/login` - เริ่มต้น Jira OAuth flow
- `POST /auth/callback` - Handle OAuth callback
- `GET /auth/me` - ดูข้อมูล user ปัจจุบัน
- `POST /auth/logout` - Logout

### Jira Proxy
- `GET /api/projects` - ดึงรายการ projects
- `POST /api/search` - ค้นหา issues ด้วย JQL
- `GET /api/issues/{issue_key}` - ดูรายละเอียด issue
- `PUT /api/issues/{issue_key}/transition` - เปลี่ยนสถานะ issue
- `PUT /api/issues/{issue_key}` - อัปเดต issue fields

### Webhooks
- `POST /webhooks/jira` - รับ Jira webhooks

## 🔧 การพัฒนา

### การเพิ่ม API Route ใหม่

1. สร้าง route ใน `app/main.py` หรือแยกไฟล์ router
2. เพิ่ม Pydantic models ใน `app/models.py`
3. เพิ่ม business logic ใน `app/jira_proxy.py`

### การจัดการ Webhooks

1. เพิ่ม handler ใน `app/webhooks/handlers.py`
2. อัปเดต validation ใน `app/webhooks/validators.py`
3. ลงทะเบียน webhook URL ใน Jira admin

## 🚢 การ Deploy บน Railway

### 1. เชื่อมต่อ GitHub Repository

1. สร้างบัญชี Railway.app
2. เชื่อมต่อ GitHub repository
3. เลือก `backend` directory

### 2. ตั้งค่า Environment Variables

ใน Railway dashboard, เพิ่ม environment variables:

```
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_CLIENT_ID=your_jira_client_id
JIRA_CLIENT_SECRET=your_jira_client_secret
JIRA_REDIRECT_URI=https://your-frontend-domain.vercel.app/auth/callback
FRONTEND_URL=https://your-frontend-domain.vercel.app
SECRET_KEY=your_production_secret_key
DEBUG=false
```

### 3. การ Deploy

Railway จะ deploy อัตโนมัติเมื่อ push code ใหม่

## 🔍 การ Debug

### ดู Logs
```bash
# Development
uvicorn app.main:app --reload --log-level debug

# Production (Railway)
railway logs
```

### ทดสอบ API
```bash
# Health check
curl http://localhost:8000/health

# ทดสอบ Jira connection (ต้อง authenticate ก่อน)
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/projects
```

## 📚 เอกสารเพิ่มเติม

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Jira OAuth 2.0 3LO](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/)
- [Railway Documentation](https://docs.railway.app/)