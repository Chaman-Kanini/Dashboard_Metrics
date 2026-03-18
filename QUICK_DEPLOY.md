# Quick Deploy Guide

Fast-track deployment instructions for Dashboard_Metrics.

## Prerequisites

- GitHub account (repository already created)
- Supabase account (free tier)
- Render account (free tier)
- Vercel account (free tier)

---

## Step 1: Deploy Database (5 minutes)

1. **Create Supabase Project**
   - Go to [supabase.com](https://supabase.com) → New Project
   - Name: `dashboard-metrics`
   - Set a strong database password (save it!)
   - Choose region closest to you
   - Wait for provisioning (~2 minutes)

2. **Run Database Schema**
   - In Supabase dashboard → SQL Editor → New Query
   - Copy entire contents of `database/schema.sql`
   - Paste and click **Run**
   - Verify tables created: Go to Table Editor

3. **Get Connection String**
   - Project Settings → Database → Connection string
   - Copy **Connection pooling** URI (Transaction mode)
   - Format: `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`
   - **Save this** - you'll need it for Render

---

## Step 2: Deploy Backend (10 minutes)

1. **Push Code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Add deployment configurations"
   git push origin main
   ```

2. **Create Render Web Service**
   - Go to [render.com](https://render.com) → New → Web Service
   - Connect GitHub repository: `Chaman-Kanini/Dashboard_Metrics`
   - Configure:
     - **Name**: `dashboard-metrics-api`
     - **Region**: Oregon (or closest)
     - **Branch**: `main`
     - **Root Directory**: `backend/IdeLogsApi`
     - **Runtime**: Docker
     - **Dockerfile Path**: `./Dockerfile`
     - **Plan**: Free

3. **Add Environment Variables**
   Click "Advanced" → Add Environment Variables:
   
   | Key | Value |
   |-----|-------|
   | `ASPNETCORE_ENVIRONMENT` | `Production` |
   | `ConnectionStrings__DefaultConnection` | Paste your Supabase connection string from Step 1.3 |
   | `ALLOWED_ORIGINS` | Leave empty for now (will update after Vercel) |

4. **Deploy**
   - Click **Create Web Service**
   - Wait for build (~5-8 minutes)
   - Copy your backend URL: `https://dashboard-metrics-api.onrender.com`
   - Test health endpoint: `https://dashboard-metrics-api.onrender.com/api/health`

---

## Step 3: Deploy Frontend (5 minutes)

1. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com) → Add New → Project
   - Import `Chaman-Kanini/Dashboard_Metrics`
   - Configure:
     - **Framework**: Vite (auto-detected)
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `dist`

2. **Add Environment Variable**
   - Click "Environment Variables"
   - Add:
     - **Name**: `VITE_API_URL`
     - **Value**: `https://dashboard-metrics-api.onrender.com/api`
     - (Use your actual Render URL from Step 2.4)

3. **Deploy**
   - Click **Deploy**
   - Wait for build (~2-3 minutes)
   - Copy your frontend URL: `https://dashboard-metrics-xxx.vercel.app`

---

## Step 4: Update Backend CORS (2 minutes)

1. **Update Render Environment Variables**
   - Go to Render dashboard → Your service
   - Environment → Add Variable:
     - **Key**: `ALLOWED_ORIGINS`
     - **Value**: `https://dashboard-metrics-xxx.vercel.app`
     - (Use your actual Vercel URL from Step 3.3)

2. **Redeploy Backend**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait ~3 minutes

---

## Step 5: Test Deployment (2 minutes)

1. **Visit Your Dashboard**
   - Open your Vercel URL: `https://dashboard-metrics-xxx.vercel.app`
   - Dashboard should load (may show empty data initially)

2. **Verify API Connection**
   - Open browser DevTools (F12) → Network tab
   - Refresh page
   - Check for API calls to your Render backend
   - Should see 200 OK responses

3. **Test Data Ingestion** (Optional)
   - Update local `.env` with Supabase connection string
   - Run: `python windsurf_to_langfuse.py`
   - Refresh dashboard to see data

---

## Troubleshooting

### Frontend shows "Network Error"
- Check CORS: Verify `ALLOWED_ORIGINS` in Render includes your Vercel URL
- Check backend is running: Visit `https://your-backend.onrender.com/api/health`
- Check browser console for specific errors

### Backend won't start
- Check Render logs for errors
- Verify Supabase connection string is correct
- Ensure no extra spaces in environment variables

### Database connection fails
- Verify connection string format
- Check password is correct (no special characters causing issues)
- Try connection pooling URL instead of direct connection

---

## URLs Summary

After deployment, save these URLs:

- **Frontend**: `https://dashboard-metrics-xxx.vercel.app`
- **Backend**: `https://dashboard-metrics-api.onrender.com`
- **Backend Health**: `https://dashboard-metrics-api.onrender.com/api/health`
- **Supabase Dashboard**: `https://supabase.com/dashboard/project/[PROJECT-REF]`

---

## Next Steps

- [ ] Set up custom domain (optional)
- [ ] Configure Supabase backups
- [ ] Set up monitoring/alerts
- [ ] Review Render logs periodically
- [ ] Consider upgrading to paid tiers for production use

---

## Cost Summary

**Free Tier Limits:**
- Supabase: 500MB database, 2GB bandwidth/month
- Render: 750 hours/month, sleeps after 15min inactivity
- Vercel: 100GB bandwidth/month

**Total Monthly Cost**: $0 (within free tier limits)

For production with no sleep time and better performance, consider:
- Render Starter: $7/month
- Supabase Pro: $25/month
- Vercel Pro: $20/month
