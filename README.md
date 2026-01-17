# NaviBlu Travel Assistant

AI chatbot to provide flight and hotel options as well as general travel information.

Built on top of Meta's llama-3.3-70b.

The Streamlit app is hosted on Streamlit Community Cloud and embedded in a custom website.

<img src="website/images/For_Readme_1.png" alt="Logo" style="width: 80%;"/>
<img src="website/images/For_Readme_2.png" alt="Logo" style="width: 80%;"/>

<br>

## Architecture

- **Chatbot Module** (`chatbot/`): Core logic and Streamlit UI
  - `core.py`: Agent-based system for flights, hotels, locations, and general info
  - `streamlit_app.py`: Chat interface deployed on Streamlit Community Cloud
- **Static Website** (root files): Marketing site with embedded Streamlit app via iframe
  - `index.html`, `styles.css`, `scripts.js`, `images/`

<br>

## Installation

### Prerequisites

Requires Python 3.13.2 (or compatible version)

### API Keys Required

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_key_here
AMADEUS_API_KEY=your_key_here
AMADEUS_API_SECRET=your_secret_here
```

Get your API keys:
- **GROQ_API_KEY**: For LLM calls → https://console.groq.com/
- **AMADEUS_API_KEY** and **AMADEUS_API_SECRET**: For hotel data → https://developers.amadeus.com/

### Install Dependencies

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

<br>

## Running Locally

### Option 1: Quick Start with `local_testing.py`

```bash
python local_testing.py
```

Choose:
1. **Streamlit App** - Test the chatbot directly (runs on http://localhost:8501)
2. **Static Website** - View the full website with embedded Streamlit (runs on http://localhost:8000)

### Option 2: Run Streamlit Directly

```bash
streamlit run chatbot/streamlit_app.py
```

Visit http://localhost:8501

### Option 3: Serve Static Website

```bash
python -m http.server 8000
```

Visit http://localhost:8000

> **Note**: The website embeds the Streamlit app from Streamlit Community Cloud. If you want to test locally with the local Streamlit instance, update the iframe src in `index.html` to `http://localhost:8501`.

<br>

## Deployment

### Streamlit App
The chatbot is deployed on **Streamlit Community Cloud**. Any updates to files in the `chatbot/` folder will automatically redeploy.

### Static Website (GitHub Pages)

**To Deploy:**

1. **Push to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Prepare for GitHub Pages deployment"
   git push origin main
   ```

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under **Source**, select:
     - Branch: `main` (or your default branch)
     - Folder: `/ (root)`
   - Click **Save**

3. **Wait 1-2 minutes** for deployment

4. **Your site will be live at**:
   ```
   https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
   ```

The embedded Streamlit app will load automatically from Streamlit Community Cloud.

**Alternative Deployment Options:**
- **Netlify** (free) - drag and drop the entire repo or connect via Git
- **Vercel** (free) - connect your repo via Git

<br>

## Project Structure

```
NaviBlu_Travel_Assistant/
├── chatbot/                  # Chatbot module
│   ├── __init__.py          # Module initialization
│   ├── core.py              # Core chatbot logic with agent system
│   └── streamlit_app.py     # Streamlit UI (deployed to cloud)
├── images/                   # Website images (logo and travel photos)
├── index.html                # Main website page with embedded Streamlit
├── styles.css                # Website styling
├── scripts.js                # Slideshow and animations
├── local_testing.py          # Local testing launcher
├── requirements.txt          # Python dependencies
├── .env                      # API keys (create this)
└── testing_files/           # Jupyter notebooks for development
```

<br>

## Features

✈️ **Flight Search** - Real-time flight pricing from 400+ airlines  
🏨 **Hotel Search** - 150,000+ hotels across 190 countries  
📍 **Location Info** - Tourist attractions and activity recommendations  
💬 **Natural Conversation** - Talk naturally, no complex forms  
🤖 **AI-Powered** - Built on Meta's Llama 3.3 70B model  

<br>

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript (static website)
- **Chatbot UI**: Streamlit
- **Backend Logic**: Python
- **LLM**: Groq API (Meta Llama 3.3 70B)
- **Flight Data**: fast_flights API
- **Hotel Data**: Amadeus API

<br>

## Team

**ITCS 6112 - Group 5**

Cameron Detig • Juan Rojas • Evelyn Hosana • Varsha Chintalapati

© 2025 NaviBlu Project
