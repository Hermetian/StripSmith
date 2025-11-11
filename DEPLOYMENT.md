# StripSmith Web Deployment Guide

This guide will help you deploy StripSmith with a **Vercel frontend + Railway backend** architecture.

## Architecture Overview

```
User Browser
    ↓
Vercel (React Frontend) - FREE
    ↓
Railway (FastAPI Backend) - FREE (500hrs/month)
    ↓
User's API Keys (stored in memory)
    ↓
OpenAI & Anthropic APIs
```

---

## Prerequisites

1. GitHub account
2. [Railway.app](https://railway.app) account (sign up with GitHub)
3. [Vercel](https://vercel.com) account (sign up with GitHub)
4. Push this code to a GitHub repository

---

## Step 1: Deploy Backend to Railway

### 1.1. Push Code to GitHub

```bash
git add .
git commit -m "Add web deployment"
git push origin main
```

### 1.2. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your `StripSmith` repository
5. Railway will auto-detect Python and deploy

### 1.3. Configure Railway

1. In your Railway project, click on the service
2. Go to **Settings** tab
3. Under **"Root Directory"**, set it to: `backend`
4. Click **"Generate Domain"** to get a public URL
5. Copy the URL (e.g., `https://stripsmith-production.up.railway.app`)

**Note:** Railway free tier gives you 500 hours/month (~16 hours/day), which is plenty for a hobby project.

---

## Step 2: Deploy Frontend to Vercel

### 2.1. Update API URL

1. Edit `frontend/vercel.json` and replace the placeholder URL:

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://YOUR-RAILWAY-URL.railway.app/api/:path*"
    }
  ]
}
```

2. Create `frontend/.env.production`:

```bash
VITE_API_URL=https://YOUR-RAILWAY-URL.railway.app
```

3. Commit changes:

```bash
git add frontend/vercel.json frontend/.env.production
git commit -m "Configure production API URL"
git push
```

### 2.2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Add environment variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://YOUR-RAILWAY-URL.railway.app`
6. Click **"Deploy"**

Your frontend will be live at `https://your-project.vercel.app`

---

## Step 3: Test the Deployment

1. Visit your Vercel URL
2. Enter your OpenAI and Anthropic API keys
3. Upload a short story (test with ~500 words first)
4. Watch the progress and verify it works!

---

## Cost Breakdown

### Hosting (FREE)
- **Vercel Frontend:** Free forever
- **Railway Backend:** Free (500 hrs/month)

### API Usage (User Pays)
Users provide their own API keys, so **you pay $0**:
- OpenAI DALL-E 3: $0.04 per image (standard quality)
- Anthropic Claude: ~$0.05 per story analysis

Typical 30-panel chapter: ~$1.50-2.00 (paid by user)

---

## Security Notes

✅ **API Keys are secure:**
- Stored in server memory only (never on disk)
- Session expires after 2 hours
- Never logged or persisted
- Each user uses their own keys

✅ **No abuse risk:**
- Users can only use their own API credits
- No shared API keys
- No way for users to exhaust your credits

---

## Optional: Add Custom Domain

### Vercel (Frontend)
1. Go to your project settings
2. Click **"Domains"**
3. Add your domain and follow DNS instructions

### Railway (Backend)
1. Go to your service settings
2. Under **"Networking"** → **"Public Networking"**
3. Add custom domain

---

## Monitoring & Logs

### Railway Backend
- View logs in Railway dashboard
- Monitor memory/CPU usage
- Check for errors in real-time

### Vercel Frontend
- View deployment logs
- Monitor function invocations (none for this static site)
- Check analytics

---

## Troubleshooting

### Backend won't start
- Check Railway logs for errors
- Verify `backend/requirements.txt` is complete
- Ensure Python 3.11 is specified in `runtime.txt`

### Frontend can't reach backend
- Verify CORS settings in `backend/main.py`
- Check the API URL in `frontend/.env.production`
- Verify Railway domain is correct in `vercel.json`

### "CORS error" in browser console
The backend allows all origins for now. If you want to restrict:

Edit `backend/main.py`:
```python
allow_origins=[
    "https://your-project.vercel.app",  # Your Vercel URL
]
```

### Generation fails
- Check Railway logs for Python errors
- Verify user provided valid API keys
- Check if Railway ran out of free hours (500/month)

---

## Scaling Beyond Free Tier

If you exceed Railway's 500 hours/month:

### Option 1: Upgrade Railway
- **Hobby Plan:** $5/month (unlimited hours)

### Option 2: Switch Backend Provider
- **Render.com:** Free tier with auto-sleep
- **fly.io:** Free tier with 3 shared VMs
- **Modal.com:** Serverless Python with generous free tier

---

## Development Workflow

### Run locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000`

### Deploy updates

```bash
git add .
git commit -m "Update description"
git push
```

Both Railway and Vercel will auto-deploy on push!

---

## Next Steps

- [ ] Test with a short story (500 words)
- [ ] Share with friends to get feedback
- [ ] Monitor Railway hours usage
- [ ] Consider adding analytics
- [ ] Add user authentication (if needed later)
- [ ] Implement job cleanup (auto-delete old files)

---

## Support

If you run into issues:
1. Check Railway and Vercel logs
2. Verify environment variables
3. Test API keys work directly
4. Check GitHub Issues for similar problems

Happy comic generating! 📚✨
