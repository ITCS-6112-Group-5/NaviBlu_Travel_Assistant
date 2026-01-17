import os
import http.server
import socketserver

def main():
    print("\nNaviBlu Travel Assistant - Local Testing")
    print("=" * 50)
    print("1. Run Streamlit App (for testing chatbot)")
    print("2. Serve Static Website (with embedded Streamlit)")
    print()
    
    choice = input("Which option? (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Streamlit App...")
        print("📍 URL: http://localhost:8501")
        print("⚠️  Press Ctrl+C to stop\n")
        os.system('streamlit run chatbot/streamlit_app.py')
        
    elif choice == "2":
        print("\n🌐 Starting Static Website Server...")
        print("📍 URL: http://localhost:8000")
        print("💡 The embedded Streamlit app will load from Streamlit Cloud")
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
