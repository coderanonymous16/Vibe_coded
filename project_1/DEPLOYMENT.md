# ExamRAG Public Deployment Guide

This project is ready to be deployed in a public setup with:

- Render for the FastAPI backend
- Vercel for the static frontend
- Supabase/Postgres for production persistence
- OpenAI-compatible LLM key for live generation
- Resend for email-related account flows

## 1. Backend on Render

1. Connect this repository to Render.
2. Create a new Web Service.
3. Set the root directory to `backend`.
4. Use the included `render.yaml` or configure manually:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Add environment variables using the values from `.env` or your own production config.
6. Replace the placeholder database URL with your real PostgreSQL/Supabase connection string before launch.
7. After the first successful deployment, copy the actual Render URL shown on the service overview page and set `APP_BASE_URL` to that URL.

## 2. Frontend on Vercel

1. Import the `frontend/` folder as a static site project.
2. After the backend is deployed, edit `frontend/config.js` and set `window.EXAMRAG_API_BASE` to the actual Render URL with `/api/v1` appended. This static frontend does not read Vercel environment variables at runtime.
3. Commit and push that change, then deploy/redeploy the frontend.
4. Set Render's `CORS_ORIGINS` to the exact Vercel production URL (and any preview URL you intend to use). A value such as `https://*.vercel.app` is not treated as a wildcard by the current CORS middleware.

Example only; replace the host with the URL Render actually assigned to your service:

```js
window.EXAMRAG_API_BASE = 'https://<actual-render-service>.onrender.com/api/v1';
```

## 3. Core environment variables

Required:

- `DATABASE_URL`
- `SECRET_KEY`
- `OPENAI_API_KEY`
- `EMBEDDING_API_KEY`
- `RESEND_API_KEY`
- `RESEND_FROM_EMAIL`
- `APP_BASE_URL`
- `FRONTEND_URL`

## 4. Production notes

- Use a real PostgreSQL connection string in production.
- Keep the app defaulting to SQLite only for local dev.
- Keep `.env` local and never commit it to source control.
- Replace the placeholder Supabase host with the real DB password before public launch.
