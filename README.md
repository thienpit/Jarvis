# Jarvis AI Assistant

Ứng dụng AI trợ lý voice interaction, deploy trên Vercel (frontend) + Render (backend).

## Cấu trúc

```
jarvis/
├── frontend/          # Vercel deploy
│   ├── index.html
│   ├── app.js
│   └── style.css
├── backend/           # Render deploy
│   ├── app/
│   │   ├── main.py    # FastAPI
│   │   └── services/
│   │       ├── hermes_client.py
│   │       └── tts_service.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

## Deploy

### Frontend (Vercel)
1. Push code lên GitHub
2. Vercel → New Project → Import repo `thienpit/Jarvis`
3. Root Directory: `frontend`
4. Framework: Other
5. Deploy

### Backend (Render)
1. Push code lên GitHub
2. Render → New Web Service → Connect repo `thienpit/Jarvis`
3. Root Directory: `backend`
4. Build Command: `bash run.sh`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Environment Variables:
   - `HERMES_CLI_PATH`: `/app/hermes_agent/hermes_cli/main.py`
   - `HERMES_CLI_TIMEOUT`: `30`
   - `TTS_VOICE`: `vi-VN-NamMinhNeural`
7. Plan: Free
8. Deploy

### Test API trực tiếp
```bash
curl -X POST https://jarvis-backend.onrender.com/api/process \
  -H "Content-Type: application/json" \
  -d '{"text":"Xin chào Jarvis"}'
```

## Cập nhật

### Backend
```bash
git add .
git commit -m "Update backend"
git push
# Render tự động redeploy
```

### Frontend
```bash
git add .
git commit -m "Update frontend"
git push
# Vercel tự động redeploy
```

## Tác giả
Thiện Phan (thienpit)
