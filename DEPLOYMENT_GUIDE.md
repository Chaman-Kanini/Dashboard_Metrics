# Deployment Guide

Complete guide to deploy Dashboard_Metrics across three platforms:
- **Database**: Supabase (PostgreSQL)
- **Backend**: Render (.NET 8 API)
- **Frontend**: Vercel (React + Vite)

---

## 1. Database Deployment (Supabase)

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign in
2. Click **New Project**
3. Fill in project details:
   - **Name**: `dashboard-metrics` (or your preferred name)
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Select closest to your users
4. Click **Create new project** and wait for provisioning

### Step 2: Run Database Schema

1. In Supabase dashboard, go to **SQL Editor**
2. Click **New Query**
3. Copy the entire contents of `database/schema.sql`
4. Paste into the SQL editor
5. Click **Run** to execute the schema

### Step 3: Get Connection Details

1. Go to **Project Settings** → **Database**
2. Scroll to **Connection string** section
3. Copy the **Connection pooling** URI (recommended for serverless)
4. Format: `postgresql://postgres.[PROJECT-REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres`
5. Save this connection string - you'll need it for backend deployment

### Step 4: Configure Row Level Security (Optional but Recommended)

Since this is an internal dashboard, you may want to disable RLS or configure policies:

```sql
-- Disable RLS for internal use (run in SQL Editor)
ALTER TABLE sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE events DISABLE ROW LEVEL SECURITY;
ALTER TABLE metrics DISABLE ROW LEVEL SECURITY;
```

---

## 2. Backend Deployment (Render)

### Step 1: Prepare Backend for Deployment

The backend needs a few configuration files for Render.

### Step 2: Create Render Account and Service

1. Go to [render.com](https://render.com) and sign in
2. Click **New +** → **Web Service**
3. Connect your GitHub repository: `Chaman-Kanini/Dashboard_Metrics`
4. Configure the service:
   - **Name**: `dashboard-metrics-api`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `backend/IdeLogsApi`
   - **Runtime**: `.NET`
   - **Build Command**: `dotnet publish -c Release -o out`
   - **Start Command**: `dotnet out/IdeLogsApi.dll`
   - **Instance Type**: Free (or paid for better performance)

### Step 3: Configure Environment Variables

In Render service settings, add these environment variables:

| Key | Value |
|-----|-------|
| `ASPNETCORE_ENVIRONMENT` | `Production` |
| `ConnectionStrings__DefaultConnection` | Your Supabase connection string from Step 1.3 |
| `ASPNETCORE_URLS` | `http://0.0.0.0:8080` |

**Important**: Render expects your app to listen on port 8080 by default.

### Step 4: Update CORS Configuration

After deployment, you'll get a Render URL like `https://dashboard-metrics-api.onrender.com`

You'll need to update the frontend URL in CORS after deploying to Vercel.

### Step 5: Deploy

1. Click **Create Web Service**
2. Render will automatically build and deploy
3. Wait for deployment to complete (5-10 minutes)
4. Note your backend URL: `https://dashboard-metrics-api.onrender.com`

---

## 3. Frontend Deployment (Vercel)

### Step 1: Prepare Frontend Configuration

The frontend needs environment variables configured.

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **Add New** → **Project**
3. Import your GitHub repository: `Chaman-Kanini/Dashboard_Metrics`
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)

### Step 3: Configure Environment Variables

Add this environment variable in Vercel project settings:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://dashboard-metrics-api.onrender.com/api` |

Replace with your actual Render backend URL from Step 2.5.

### Step 4: Deploy

1. Click **Deploy**
2. Vercel will build and deploy automatically (2-3 minutes)
3. You'll get a URL like: `https://dashboard-metrics.vercel.app`

---

## 4. Final Configuration

### Update Backend CORS

After getting your Vercel URL, update the backend CORS configuration:

1. Go to Render dashboard → Your service → Environment
2. Add new environment variable:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://dashboard-metrics.vercel.app`
3. Update `Program.cs` to use this variable (see code below)
4. Redeploy the backend

### Test the Deployment

1. Visit your Vercel URL: `https://dashboard-metrics.vercel.app`
2. The dashboard should load and connect to the backend
3. Check browser console for any errors
4. Verify API calls are successful

---

## 5. Post-Deployment Checklist

- [ ] Database schema deployed to Supabase
- [ ] Backend deployed to Render and running
- [ ] Frontend deployed to Vercel and loading
- [ ] CORS configured correctly (frontend can call backend)
- [ ] Environment variables set correctly on all platforms
- [ ] Test data ingestion (run `windsurf_to_langfuse.py` with updated connection string)
- [ ] Monitor logs on Render for any errors
- [ ] Set up custom domain (optional)

---

## 6. Monitoring and Maintenance

### Supabase
- Monitor database size in Supabase dashboard
- Set up backups (automatic on paid plans)
- Review query performance in **Database** → **Query Performance**

### Render
- Check logs: Service → **Logs** tab
- Monitor resource usage
- Free tier sleeps after 15 min inactivity (first request will be slow)

### Vercel
- Check deployment logs in project dashboard
- Monitor bandwidth usage
- Review analytics (if enabled)

---

## 7. Troubleshooting

### Backend won't start on Render
- Check logs for connection string errors
- Verify Supabase connection string is correct
- Ensure port 8080 is configured

### Frontend can't connect to backend
- Check CORS configuration
- Verify `VITE_API_URL` is set correctly
- Check browser console for CORS errors
- Ensure backend is running (not sleeping)

### Database connection errors
- Verify Supabase connection string format
- Check if IP is whitelisted (Supabase allows all by default)
- Use connection pooling URL for serverless environments

---

## 8. Cost Estimates

- **Supabase**: Free tier (500MB database, 2GB bandwidth)
- **Render**: Free tier (750 hours/month, sleeps after inactivity)
- **Vercel**: Free tier (100GB bandwidth, unlimited deployments)

**Total**: $0/month on free tiers (sufficient for development/testing)

For production, consider paid tiers for better performance and no sleep time.
