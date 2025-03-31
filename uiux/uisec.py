import webbrowser
import ssl
import os
import time
from flask import Flask, jsonify, request, abort
from functools import wraps
from flask_talisman import Talisman


app = Flask(__name__)

Talisman(app)

API_KEY = "secureapikey123"

ALLOWED_URLS = {"http://localhost/frmp6/uiux/pages/index.php"}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.args.get("api_key") != API_KEY:
            abort(403, description="Unauthorized access")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/secure_ui")
@require_api_key
def secure_ui():
    return jsonify({"status": "UI secured with HTTPS, Access Control, and API Authentication"})

def open_secure_browser(url):
    if url in ALLOWED_URLS:
        webbrowser.open(url)
        print(f"Opening {url} in your default web browser...")
    else:
        print("Blocked unauthorized URL access attempt.")

if __name__ == "__main__":
    if not os.environ.get("WERKZEUG_RUN_MAIN"):  
        open_secure_browser("http://localhost/frmp6/uiux/pages/index.php")

    app.run(ssl_context=("cert.pem", "key.pem"), debug=True)



