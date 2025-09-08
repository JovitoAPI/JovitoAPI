# api/index.py
import os
import requests
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__, template_folder="templates")

# Environment variables (set these in Vercel Project Settings)
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

# Paytm URLs
AUTH_BASE = "https://login.paytmmoney.com/merchant-login"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/v2/gettoken"

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Test environment variables
@app.route("/test-env")
def test_env():
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    return "❌ Environment variables NOT found!"

# Login route: redirect to Paytm login
@app.route("/login")
def login():
    enc_redirect = quote_plus(REDIRECT_URI)
    login_url = f"{AUTH_BASE}?apiKey={CLIENT_ID}&state={enc_redirect}"
    return redirect(login_url)

# Callback route: exchange request_token for access_token
@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")
    if not request_token:
        return "Missing request_token", 400

    payload = {
        "api_key": CLIENT_ID,
        "api_secret_key": CLIENT_SECRET,
        "request_token": request_token
    }

    try:
        resp = requests.post(TOKEN_URL, json=payload, timeout=10)
        resp.raise_for_status()
        tokens = resp.json()
        return jsonify(tokens)
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
