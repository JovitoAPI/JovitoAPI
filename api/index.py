import os
import requests
from flask import Flask, request, jsonify, redirect, render_template
from urllib.parse import quote_plus

app = Flask(__name__, template_folder="templates")

# Environment variables (Vercel or local .env)
API_KEY = os.getenv("PAYTM_CLIENT_ID", "")
API_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

AUTH_BASE = "https://login.paytmmoney.com/merchant-login"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/v2/gettoken"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    # Build safe, URL-encoded redirect URI
    enc_redirect = quote_plus(REDIRECT_URI)
    login_url = f"{AUTH_BASE}?apiKey={API_KEY}&state=123&redirect_uri={enc_redirect}"
    return redirect(login_url)

@app.route("/test-env")
def test_env():
    if API_KEY and API_SECRET:
        return "✅ Environment variables are working!"
    else:
        return "❌ Environment variables NOT found!"

@app.route("/callback")
def callback():
    # 1️⃣ Get request_token from query params
    request_token = request.args.get("request_token")
    if not request_token:
        return "Missing request_token in callback URL", 400

    # 2️⃣ Exchange request_token for access_token
    payload = {
        "api_key": API_KEY,
        "api_secret_key": API_SECRET,
        "request_token": request_token
    }

    try:
        resp = requests.post(TOKEN_URL, json=payload, timeout=10)
        resp.raise_for_status()
        tokens = resp.json()
        # 3️⃣ Return tokens (access_token + refresh_token)
        return jsonify(tokens)
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
