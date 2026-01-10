 #import the app adn run the server 

from app import create_app

app = create_app()

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    
    # Clear output so you always know where the server is running
    print("\n" + "="*60)
    print(f"🚀 OneTimeShare Server Starting...")
    print(f"🌐 Local:    http://localhost:{port}")
    print(f"🌐 Network:  http://0.0.0.0:{port}")
    print(f"🔧 Debug:    {debug}")
    print(f"⚡ Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug)
