import os
import sys
import subprocess
import http.server
import socketserver

def check_streamlit_installed():
    """Check if streamlit is installed."""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("\nNaviBlu Travel Assistant - Local Testing")
    print("=" * 50)
    print("1. Run Streamlit App (for testing chatbot)")
    print("2. Serve Static Website (with embedded HF Space)")
    print()
    
    choice = input("Which option? (1 or 2): ").strip()
    
    if choice == "1":
        # Check if dependencies are installed
        if not check_streamlit_installed():
            print("\n⚠️  Streamlit is not installed!")
            print("Install dependencies first:")
            print(f"  pip install -r chatbot/requirements.txt")
            print("\nThen run this script again.")
            return
        
        print("\n🚀 Starting Streamlit App...")
        print("📍 URL: http://localhost:8501")
        print("⚠️  Press Ctrl+C to stop\n")
        
        # Use python -m streamlit for better compatibility
        os.system(f'{sys.executable} -m streamlit run chatbot/app.py')
        
    elif choice == "2":
        print("\n🌐 Starting Static Website Server...")
        print("📍 URL: http://localhost:8000")
        print("💡 The embedded Streamlit app will load from Hugging Face Space")
        print("⚠️  Press Ctrl+C to stop\n")
        
        PORT = 8000
        
        Handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}\n")
            httpd.serve_forever()
            
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
