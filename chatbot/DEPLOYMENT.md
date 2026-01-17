# Deploying NaviBlu Chatbot to Hugging Face Spaces

This guide explains how to deploy the NaviBlu chatbot to Hugging Face Spaces.


## Prerequisites

1. **Hugging Face Account**: Sign up at https://huggingface.co/
2. **API Keys**: You'll need to add these as Secrets in your Space:
   - `GROQ_API_KEY`
   - `AMADEUS_API_KEY`
   - `AMADEUS_API_SECRET`

## Deployment Steps

### Step 1: Create a New Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Configure:
   - **Space name**: `naviblu-travel-assistant` (or your choice)
   - **SDK**: Select **Docker** - **Streamlit**
   - **Hardware**: **CPU basic** (free tier is sufficient)
3. **Create Space**



### Step 2: Add API Keys as Secrets

1. In your Space, go to **Settings** → **Repository secrets**
2. Add the following secrets:
   - **Name**: `GROQ_API_KEY`, **Value**: Your Groq API key
   - **Name**: `AMADEUS_API_KEY`, **Value**: Your Amadeus API key
   - **Name**: `AMADEUS_API_SECRET`, **Value**: Your Amadeus API secret

### Step 3: Wait for Build

The Space will build the Docker image and start. 

### Step 4: Test Your Space

Your chatbot will be live at:
```
https://huggingface.co/spaces/YOUR-USERNAME/naviblu-travel-assistant
```


**Note**: The embed URL format for Docker Spaces is `https://USERNAME-SPACENAME.hf.space`


## Updating the Space via GitHub Actions

The project includes a GitHub Actions workflow (`.github/workflows/deploy-huggingface.yml`) that **automatically deploys** the chatbot to Hugging Face whenever you push changes to the `chatbot/` folder.

#### How It Works

**Trigger Conditions:**
```yaml
on:
  push:
    branches: [main]
    paths: ['chatbot/**']  # Only triggers on chatbot folder changes
  workflow_dispatch:        # Can also trigger manually
```

**What Happens During Deployment:**

1. **GitHub Actions detects** a push to `main` that modified files in `chatbot/`
2. **Checks out** your repository code
3. **Authenticates** with Hugging Face using your `HF_TOKEN`
4. **Clones** your Hugging Face Space repository
5. **Removes** old files (keeps `.git` folder)
6. **Copies** all files from `chatbot/` folder (including hidden files like `.streamlit/`)
7. **Commits** changes with message: `"Auto-deploy from GitHub: [commit-sha]"`
8. **Pushes** to Hugging Face, triggering a Space rebuild

**Files Copied:**
- `app.py`, `core.py`, `__init__.py`
- `Dockerfile`, `README.md`, `requirements.txt`
- `.streamlit/config.toml` (hidden folder included!)

#### One-Time Setup

**Step 1: Get Your Hugging Face Token**
1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Name: `GitHub Actions Deploy`
4. Type: **Write** (needs write access to push to Space)
5. Copy the token (you won't see it again!)

**Step 2: Add GitHub Secrets**
1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add **two secrets**:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `HF_TOKEN` | Your Hugging Face token | `hf_xxxxxxxxxxxxx` |
| `HF_SPACE_NAME` | Your Space path | `cameron-d/NaviBlu_Travel_Assistant` |

**Step 3: Test the Workflow**

Make a change to any file in `chatbot/`, commit, and push:
```bash
# Example: Update a comment in chatbot/app.py
git add chatbot/
git commit -m "Test auto-deploy"
git push origin main
```

Watch the deployment:
- GitHub: **Actions** tab → See workflow run
- Hugging Face: Your Space → **Settings** → See new commit appear

#### Manual Trigger

You can also trigger deployment manually (without pushing code):

1. Go to GitHub → **Actions** tab
2. Select **Deploy to Hugging Face Spaces** workflow
3. Click **Run workflow** → Choose branch → **Run**

This is useful for re-deploying without code changes.


#### What Gets Deployed

✅ **Included:**
- All Python files (`*.py`)
- Docker configuration (`Dockerfile`)
- Requirements (`requirements.txt`)
- Space metadata (`README.md`)
- Hidden folders (`.streamlit/`)
- All subdirectories

❌ **Excluded:**
- Git history (only `.git` folder from HF Space is kept)
- Files outside `chatbot/` folder

#### Viewing Deployment Status

**In GitHub:**
1. Go to **Actions** tab
2. Click on the latest workflow run
3. Expand steps to see:
   - ✅ Checkout code
   - ✅ Push to HF Space
   - ⏱️ Deployment logs

**In Hugging Face:**
1. Go to your Space
2. Check **Settings** → Recent commits
3. Look for: `Auto-deploy from GitHub: [sha]`
4. **App** tab → Monitor rebuild progress
