# trigger redeploy for /test-env
import os
import requests
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__, template_folder="templates")

# 🔑 Read secrets from environment (Vercel env vars or local .env for testing)
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
# Ensure this matches what you registered on Paytm dev console
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

# 🔗 Paytm OAuth2 Endpoints
AUTH_BASE = "https://developer.paytmmoney.com/oauth2/authorize"
TOKEN_URL = "https://developer.paytmmoney.com/oauth2/token"  # ✅ Fixed endpoint

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    """Landing page with login button"""
    return render_template("index.html")

@app.route("/login")
def login():
    """Redirect user to Paytm OAuth login"""
    enc_redirect = quote_plus(REDIRECT_URI)
    auth_url = f"{AUTH_BASE}?client_id={CLIENT_ID}&response_type=code&scope=read&redirect_uri={enc_redirect}"
    return redirect(auth_url)

@app.route("/test-env")
def test_env():
    """Check if environment variables are loaded"""
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    return "❌ Environment variables NOT found!"

@app.route("/callback")
def callback():
    """Paytm redirects here with ?code=... → Exchange code for tokens"""
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    try:
        resp = requests.post(TOKEN_URL, data=payload, timeout=10)
        resp.raise_for_status()
        tokens = resp.json()
        return jsonify(tokens)  # Shows access_token + refresh_token
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
