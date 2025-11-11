# StripSmith Web - AI Comic Generator

**Transform stories into AI-generated comics using your own API keys.**

Live Demo: [Deploy your own!](#deployment)

---

## What is This?

StripSmith Web is a browser-based comic generation tool that:

1. **Analyzes your story** using Claude AI
2. **Generates character reference sheets** with DALL-E 3
3. **Breaks the story into comic panels** with AI
4. **Creates panel artwork** using consistent character designs
5. **Composes final pages** with layouts and speech bubbles
6. **Exports** to PDF, PNG, or CBZ format

**🔐 Privacy First:** You provide your own API keys. They're stored in memory only (never on disk) and expire after 2 hours.

---

## Quick Start (5 minutes)

### 1. Deploy Backend (Railway - Free)

```bash
# 1. Push to GitHub
git add .
git commit -m "Initial web version"
git push origin main

# 2. Go to railway.app, click "New Project"
# 3. Deploy from GitHub, select this repo
# 4. Set root directory to "backend"
# 5. Generate a public domain
```

### 2. Deploy Frontend (Vercel - Free)

```bash
# 1. Update frontend/vercel.json with your Railway URL
# 2. Go to vercel.com, click "New Project"
# 3. Import from GitHub
# 4. Set root directory to "frontend"
# 5. Add env var: VITE_API_URL=https://your-railway-url
# 6. Deploy!
```

**Done!** You now have a live comic generator at `your-project.vercel.app`

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

## How It Works

### Architecture

```
┌─────────────────┐
│  User Browser   │
│  (Vercel)       │  ← React frontend (free hosting)
└────────┬────────┘
         │ API calls
         ↓
┌─────────────────┐
│  FastAPI Server │
│  (Railway)      │  ← Python backend (free 500hrs/month)
└────────┬────────┘
         │
         ├→ User's OpenAI Key → DALL-E 3
         └→ User's Anthropic Key → Claude
```

### Security Model

✅ **You pay $0 for API usage** - users provide their own keys
✅ **Keys never touch disk** - stored in memory only
✅ **Session expires** - keys auto-delete after 2 hours
✅ **No abuse risk** - users can't exhaust your credits

---

## Features

- ✨ **User-provided API keys** (no shared costs)
- 📊 **Real-time progress tracking**
- 🎨 **Customizable art styles**
- 📖 **Multi-chapter support**
- 💾 **Multiple export formats** (PDF, PNG, CBZ)
- 🔒 **Secure session management**
- 🚀 **Free hosting** (Vercel + Railway)

---

## Usage Costs (Paid by User)

Users need:
- **OpenAI API key** (for DALL-E 3 image generation)
- **Anthropic API key** (for Claude story analysis)

### Cost per comic:
- **30-panel chapter:** ~$1.50-2.00
  - Character sheets: ~$0.36
  - Panel images: ~$1.20
  - Claude analysis: ~$0.05

**You pay:** $0 (users use their own keys!)

---

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11** - Core language
- **OpenAI SDK** - DALL-E 3 integration
- **Anthropic SDK** - Claude integration
- **Pillow & OpenCV** - Image processing
- **ReportLab** - PDF generation

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Vanilla CSS** - Styling (no frameworks!)

### Hosting
- **Railway** - Backend (500 hrs/month free)
- **Vercel** - Frontend (unlimited free)

---

## Project Structure

```
StripSmith/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── jobs.py          # Job/session management
│   ├── api_wrapper.py   # Pipeline wrapper
│   ├── requirements.txt
│   └── railway.json
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.jsx     # Main component
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── vercel.json
├── src/                 # Original Python pipeline
│   ├── analysis/       # Story analysis
│   ├── assets/         # Character generation
│   ├── panels/         # Panel breakdown
│   ├── compositor/     # Page composition
│   └── utils/
└── DEPLOYMENT.md       # Detailed deployment guide
```

---

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:3000`

---

## API Endpoints

### `POST /api/session/set-keys`
Store API keys in session (memory only)

**Request:**
```json
{
  "openai_api_key": "sk-...",
  "anthropic_api_key": "sk-ant-..."
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "expires_in": 7200
}
```

### `POST /api/generate`
Start comic generation job

**Form Data:**
- `session_id` - Session ID from set-keys
- `story_file` - Text file upload
- `style` - Art style (optional)
- `chapters` - "all", "1-3", or "1"
- `output_format` - "pdf", "png", or "cbz"

**Response:**
```json
{
  "job_id": "uuid",
  "status": "started"
}
```

### `GET /api/status/{job_id}`
Check job progress

**Response:**
```json
{
  "status": "processing",
  "progress": 45,
  "stage": "Generating panel 15/30..."
}
```

### `GET /api/download/{job_id}`
Download completed comic

---

## Environment Variables

### Backend (Railway)
No API keys needed! Users provide their own.

### Frontend (Vercel)
```bash
VITE_API_URL=https://your-backend.railway.app
```

---

## Limitations

### Railway Free Tier
- 500 hours/month (~16 hrs/day)
- Shared CPU
- 512MB RAM

**For hobby use, this is plenty!**

If you exceed:
- Upgrade to Hobby plan ($5/month)
- Or switch to Render/fly.io

---

## Roadmap

- [ ] Add sample stories for testing
- [ ] Implement file cleanup (auto-delete old jobs)
- [ ] Add cost estimation before generation
- [ ] Support for custom character uploads
- [ ] Gallery of generated comics
- [ ] User accounts (optional)
- [ ] Webhook notifications
- [ ] Progressive image loading

---

## Contributing

This is a hobby/demo project. Feel free to:
- Open issues for bugs
- Submit PRs for features
- Fork and customize for your needs

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Credits

- **OpenAI DALL-E 3** - Image generation
- **Anthropic Claude** - Story analysis
- **FastAPI** - Backend framework
- **React + Vite** - Frontend

---

## Getting Help

1. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment issues
2. See [Troubleshooting](#troubleshooting) below
3. Open a GitHub issue

### Troubleshooting

**"CORS error"**
- Check API URL in frontend/.env.production
- Verify Railway domain is correct

**"Invalid API key"**
- OpenAI keys start with `sk-`
- Anthropic keys start with `sk-ant-`
- Test keys at platform.openai.com or console.anthropic.com

**"Generation failed"**
- Check Railway logs for Python errors
- Verify story is valid UTF-8 text
- Try a shorter story first (~500 words)

**"Backend won't start"**
- Check Railway build logs
- Verify requirements.txt is complete
- Check Python version (3.11)

---

**Ready to generate comics?** Deploy now and start creating! 📚✨
