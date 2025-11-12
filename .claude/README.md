# Claude Code Web Instructions

This file contains instructions for Claude Code instances working on this repository.

## Git Workflow

### Branch Permissions

Claude Code instances can only push to branches matching the pattern:
- `claude/<session-id>` (automatically enforced)

### Pushing to Main Branch

**IMPORTANT:** To trigger a merge to the `main` branch, your commit message MUST include the phrase:

```
[READY]
```

Example commit messages:
- ✅ `[READY] Add new feature for comic generation`
- ✅ `Update API endpoints [READY]`
- ✅ `[READY] Railway configuration files added and ready for deployment`
- ❌ `Add new feature` (will not merge to main)
- ❌ `READY: Fix bug` (missing brackets)

### Workflow Summary

1. Make changes and commit to your `claude/*` branch
2. When work is complete and tested, create a commit with `[READY]` in the message
3. Push to your branch - automation will handle merging to main
4. Railway auto-deploys from main branch

## Deployment

### Railway Backend

- **Service:** Backend API (FastAPI)
- **Branch:** `main` (auto-deploys)
- **URL:** Check Railway dashboard for deployment URL
- **Health check:** `GET /health`

### Vercel Frontend

- **Branch:** TBD
- **URL:** TBD

## Project Structure

- `/backend` - FastAPI backend service
- `/frontend` - Web frontend (planned)
- `/src` - Core comic generation pipeline
- `/scripts` - CLI tools

## Important Notes

- Backend uses serverless deployment on Railway free tier
- Comic generation runs as background jobs (handles long processing times)
- API keys are stored in session memory, never persisted to disk
