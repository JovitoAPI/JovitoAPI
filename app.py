# trigger redeploy for /test-env
import os
import requests
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__, template_folder="templates")

# Read secrets from environment (Vercel env vars or local .env if you use)
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
# Ensure REDIRECT_URI matches what you registered on Paytm dev console
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

AUTH_BASE = "https://developer.paytmmoney.com/oauth2/authorize"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/oauth/token"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    # Build safe, URL-encoded redirect URI
    enc_redirect = quote_plus(REDIRECT_URI)
    auth_url = f"{AUTH_BASE}?client_id={CLIENT_ID}&response_type=code&scope=read&redirect_uri={enc_redirect}"
    return redirect(auth_url)

# ✅ Temporary route to check environment variables
@app.route("/test-env")
def test_env():
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    else:
        return "❌ Environment variables NOT found!"

# ✅ Callback route: exchange code for tokens
@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Missing code", 400

    # Exchange code for tokens
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
        return jsonify(tokens)  # shows access_token + refresh_token
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
