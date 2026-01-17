# NaviBlu Travel Assistant

AI enabled chatbot to provide flight and hotel options as well as general travel information.

Available here: https://itcs-6112-group-5.github.io/NaviBlu_Travel_Assistant/

Powered by Meta's Llama 3.3 70B model and realtime flight / hotel APIs.

The Streamlit app is hosted on a Hugging Face Space and embedded in a custom website.

<img src="images/For_Readme_1.png" alt="Logo" style="width: 80%;"/>
<img src="images/For_Readme_2.png" alt="Logo" style="width: 80%;"/>

<br>


## Features

**Flight Search** - Real-time flight pricing from 400+ airlines  
**Hotel Search** - 150,000+ hotels across 190 countries  
**Location Info** - Tourist attractions and activity recommendations  
**Natural Conversation** - Talk naturally, no complex forms  
**AI-Powered** - Built on Meta's Llama 3.3 70B model  

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

**UNC Charlotte - ITCS 6112 - Summer 2025**

**Software System Design and Implementation**

**Group 5**

Cameron Detig • Juan Rojas • Evelyn Hosana • Varsha Chintalapati


## Architecture

- **Chatbot Module** (`chatbot/`):
  - `core.py`: Agent-based system for flights, hotels, locations, and general info
  - `streamlit_app.py`: Frontend streamlit chat interface.
- **Static Website** (root files): Landing page with embedded Streamlit app via iframe
  - `index.html`, `styles.css`, `scripts.js`, `images/`

<br>

## Installation

### Prerequisites

Requires Python 3.12 +

### API Keys Required

Get your API keys:
- **GROQ_API_KEY**: For LLM calls → https://console.groq.com/
- **AMADEUS_API_KEY** and **AMADEUS_API_SECRET**: For hotel data → https://developers.amadeus.com/

Create a `.env` file in the project root with:

```
GROQ_API_KEY=your_key_here
AMADEUS_API_KEY=your_key_here
AMADEUS_API_SECRET=your_secret_here
```



### Install Dependencies

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r chatbot/requirements.txt
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



## Deployment

### Streamlit App (Hugging Face Spaces)
The chatbot is deployed on **Hugging Face Spaces** using Docker.

All deployment files are in the `chatbot/` folder, including the Dockerfile.

See [`chatbot/DEPLOYMENT.md`](chatbot/DEPLOYMENT.md) for detailed deployment instructions.

**Quick Summary**: 
1. Create a new Space with **Docker SDK**
2. Add your API keys as Secrets in Settings
3. Push to the github repo and an automated action will upload the chatbot files to the Hugging Face space.

### Website (GitHub Pages)

**To Deploy:**

1. **Push to GitHub**:

2. **Enable GitHub Pages**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under **Source**, select:
     - Branch: `main` (or your default branch)
     - Folder: `/ (root)`
   - Click **Save**

3. **Wait for deployment** 

4. **Your site will be live at**:
   ```
   https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
   ```
