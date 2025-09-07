import os
import requests
from flask import Flask, request, render_template, jsonify
# trigger redeploy for /test-env
app = Flask(__name__)

# Pull credentials from Vercel environment variables (global scope)
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET")
REDIRECT_URI = "https://paytm-auth-site.vercel.app/callback"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/oauth/token"

# Temporary route to check environment variables
@app.route("/test-env")
def test_env():
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    else:
        return "❌ Environment variables NOT found!"

# Your normal callback route
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
