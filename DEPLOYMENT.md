# Free Deployment Guide for TRAVENZA

Travenza is completely configured and ready for **100% Free Cloud Deployment**.

---

## Option 1: 1-Click Full-Stack Deploy on Render.com (Easiest)
Render allows hosting both your FastAPI backend and React frontend for free from a single GitHub repository.

### Step 1: Push to GitHub
1. Create a new repository on [GitHub](https://github.com/new) named `travenza`.
2. In your local terminal inside `travenza`:
   ```bash
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/travenza.git
   git push -u origin main
   ```

### Step 2: Deploy Blueprint on Render
1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** → **Blueprint**.
3. Connect your `travenza` GitHub repository.
4. Render will automatically read the included [render.yaml](file:///C:/Users/ASUS/.gemini/antigravity-ide/scratch/travenza/render.yaml) file:
   - Sets up **travenza-backend** (Python/FastAPI web service)
   - Sets up **travenza-frontend** (Static site)
   - Automatically connects your frontend to your backend URL!
5. Click **Apply**. Both services will build and deploy with free public HTTPS URLs!

---

## Option 2: Vercel (Frontend) + Render / Railway (Backend)

### Deploy Backend (Render or Railway):
1. On [Render](https://render.com) or [Railway](https://railway.app):
   - Choose **New Web Service** from your GitHub repo.
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
2. Copy your live backend URL (e.g. `https://travenza-backend.onrender.com`).

### Deploy Frontend (Vercel):
1. Go to [Vercel](https://vercel.com) and click **Add New Project**.
2. Select your `travenza` repo.
3. Set **Root Directory** to `frontend`.
4. In **Environment Variables**, add:
   - `VITE_API_URL` = `https://travenza-backend.onrender.com/api`
5. Click **Deploy**. Vercel will deploy your React app globally with instant CDN speeds.

---

## Option 3: Local Container Deployment (Docker Compose)
If you want to run the full production build locally in Docker containers:
```bash
docker compose up --build
```
- Frontend will be live on `http://localhost:80`
- Backend API will be live on `http://localhost:8000`
