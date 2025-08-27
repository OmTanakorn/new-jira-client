# New Jira Client (Next.js + FastAPI)

UI ลื่นแบบ Trello/Linear + Login ผ่าน **Jira (OAuth 2.0 3LO)**  
Deploy แนะนำ: **Frontend = Vercel**, **Backend = Railway**

## Project Structure

```
new-jira-client/
├─ frontend/ # Next.js 
└─ backend/ # FastAPI proxy (optional logic), รับ Webhook ภายหลัง
```

## ขั้นเริ่มเร็ว
```bash
git init
git add .
git commit -m "chore: init new-jira-client"

# ตั้งค่า ENV (ดูใน frontend/README.md และ backend/README.md)
# Deploy: FE -> Vercel, BE -> Railway
```

- ฟีเจอร์ MVP
- บอร์ดส่วนตัว (คอลัมน์ = สถานะ Jira)
- Drag & Drop → เรียก Jira transitions (optimistic update)
- ค้นหา JQL และแสดงเฉพาะ fields ที่จำเป็น