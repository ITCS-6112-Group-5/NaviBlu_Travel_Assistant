# Deploying NaviBlu Chatbot to Hugging Face Spaces

This guide explains how to deploy the NaviBlu chatbot to Hugging Face Spaces.

> ⚠️ **Note**: As of April 2025, Hugging Face deprecated the built-in Streamlit SDK. Streamlit apps now require Docker. This folder is already configured for Docker deployment.

## Prerequisites

1. **Hugging Face Account**: Sign up at https://huggingface.co/
2. **API Keys**: You'll need these as Secrets in your Space:
   - `GROQ_API_KEY`
   - `AMADEUS_API_KEY`
   - `AMADEUS_API_SECRET`

## Files in This Folder

All files needed for Hugging Face Spaces deployment:

```
chatbot/
├── app.py               # Streamlit entry point
├── core.py              # Core chatbot logic
├── __init__.py          # Module initialization
├── Dockerfile           # Docker configuration (required)
├── README.md            # HF Space metadata (YAML frontmatter)
├── requirements.txt     # Python dependencies
├── packages.txt         # System dependencies (apt-get)
├── DEPLOYMENT.md        # This guide
└── .streamlit/
    └── config.toml      # Streamlit configuration
```

## Deployment Steps

### Step 1: Create a New Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Configure:
   - **Space name**: `naviblu-travel-assistant` (or your choice)
   - **License**: MIT (or your preference)
   - **SDK**: Select **Docker**
   - **Hardware**: **CPU basic** (free tier is sufficient)
3. Click **Create Space**

### Step 2: Deploy the Chatbot Folder

**Option A: Upload via Web Interface (Easiest)**

1. In your new Space, click **Files** tab
2. Click **Add file** → **Upload files**
3. Upload ALL files from this `chatbot/` folder:
   - `app.py`
   - `core.py`
   - `__init__.py`
   - `Dockerfile`
   - `README.md`
   - `requirements.txt`
   - `packages.txt`
   - `.streamlit/config.toml` (create the folder structure)
4. Commit the files

**Option B: Git Push**

1. Clone your new Space:
   ```bash
   git clone https://huggingface.co/spaces/YOUR-USERNAME/naviblu-travel-assistant
   cd naviblu-travel-assistant
   ```

2. Copy files from the chatbot folder:
   ```bash
   cp -r /path/to/NaviBlu_Travel_Assistant/chatbot/* .
   ```

3. Push to Hugging Face:
   ```bash
   git add .
   git commit -m "Deploy NaviBlu chatbot"
   git push
   ```

### Step 3: Add API Keys as Secrets

1. In your Space, go to **Settings** → **Repository secrets**
2. Add the following secrets:
   - **Name**: `GROQ_API_KEY`, **Value**: Your Groq API key
   - **Name**: `AMADEUS_API_KEY`, **Value**: Your Amadeus API key
   - **Name**: `AMADEUS_API_SECRET`, **Value**: Your Amadeus API secret

### Step 4: Wait for Build

The Space will build the Docker image and start (typically 3-7 minutes for first build). Monitor progress in the **App** tab or **Logs**.

### Step 5: Test Your Space

Your chatbot will be live at:
```
https://huggingface.co/spaces/YOUR-USERNAME/naviblu-travel-assistant
```

## Embedding in Website

To embed in your website (`index.html`), update the iframe URL:

```html
<iframe src="https://YOUR-USERNAME-naviblu-travel-assistant.hf.space" 
        class="streamlit-iframe" 
        title="NaviBlu Travel Assistant">
</iframe>
```

**Note**: The embed URL format for Docker Spaces is `https://USERNAME-SPACENAME.hf.space`

## Understanding the Docker Setup

### Dockerfile Explained

```dockerfile
FROM python:3.11-slim          # Base Python image
WORKDIR /app                   # Set working directory
COPY requirements.txt .        # Copy dependencies
RUN pip install ...            # Install Python packages
COPY . .                       # Copy all app files
RUN useradd -m -u 1000 user   # Create non-root user (HF requirement)
USER user                      # Switch to non-root user
EXPOSE 8501                    # Expose Streamlit port
CMD ["streamlit", "run", ...]  # Start command
```

### README.md YAML Frontmatter

```yaml
---
title: NaviBlu Travel Assistant
sdk: docker              # Required for Streamlit now
app_port: 8501           # Streamlit's default port
---
```

## Troubleshooting

### Build Fails

- Check **Logs** in the App tab for error messages
- Verify Dockerfile syntax is correct
- Ensure all files are uploaded (especially `requirements.txt`)

### App Stuck on "Starting"

- Make sure `app_port: 8501` is in README.md frontmatter
- Verify Streamlit is configured to run on `0.0.0.0:8501`
- Check that Dockerfile exposes port 8501

### Import Errors

- Ensure `core.py` and `__init__.py` are uploaded
- Check that `app.py` imports use `from core import Chatbot` (not relative)

### API Errors

- Verify secrets are named exactly as expected (case-sensitive)
- Test API keys independently to ensure they're valid

### Permission Errors

- The Dockerfile creates a non-root user - this is required by HF
- Make sure you're not trying to write to system directories

## Updating the Space

### Option A: Automatic via GitHub Actions (Recommended)

If you set up the GitHub Actions workflow, simply push changes to the `chatbot/` folder on GitHub - it will automatically deploy to Hugging Face!

**One-time setup:**
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Add these secrets:
   - `HF_TOKEN`: Your Hugging Face access token (from https://huggingface.co/settings/tokens)
   - `HF_SPACE_NAME`: Your Space path (e.g., `your-username/naviblu-travel-assistant`)

Then every push to `chatbot/` will auto-deploy!

### Option B: Manual Push

```bash
# After making changes locally
cd your-space-clone
cp -r /path/to/chatbot/* .
git add .
git commit -m "Update chatbot"
git push
```

### Option C: Web Upload

Upload updated files through the Hugging Face web interface.

## Cost

- **CPU basic**: Free (sufficient for this chatbot)
- **CPU upgrade**: ~$0.50/hour
- **GPU**: Starting at ~$0.60/hour (not needed)

## Why Hugging Face Spaces?

✅ **Free tier** with good resources  
✅ **Automatic HTTPS** and domain  
✅ **Easy secrets management** for API keys  
✅ **Git-based deployment**  
✅ **Docker support** for full control  
✅ **Good uptime** and reliability  
✅ **Embed-friendly** for websites  

## Next Steps

1. ✅ Deploy chatbot to Hugging Face Spaces
2. ✅ Test the Space URL directly
3. ✅ Update `index.html` with new embed URL
4. ✅ Deploy website to GitHub Pages
5. ✅ Test the fully integrated experience
