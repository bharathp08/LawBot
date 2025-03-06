from app import app
from pyngrok import ngrok
import atexit

# Kill any existing ngrok processes
ngrok.kill()

# Set your authtoken (if not already set)
ngrok.set_auth_token('YOUR_AUTHTOKEN_HERE')

# Open a HTTP tunnel on the default port 5000
public_url = ngrok.connect(5000)
print(f' * Public URL: {public_url}')

# Cleanup on exit
atexit.register(ngrok.kill)

if __name__ == '__main__':
    app.run()