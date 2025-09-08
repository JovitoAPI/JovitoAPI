import os
import requests
from flask import Flask, redirect, request, render_template, jsonify
from urllib.parse import quote_plus

app = Flask(__name__, template_folder="templates")

# Env vars from Vercel / local .env
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

# Paytm Money endpoints
AUTH_BASE = "https://login.paytmmoney.com/merchant-login"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/v2/gettoken"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    if not CLIENT_ID:
        return "❌ PAYTM_CLIENT_ID not set in environment", 500

    if not REDIRECT_URI:
        return "❌ PAYTM_REDIRECT_URI not set in environment", 500

    # Build safe, URL-encoded redirect URI
    enc_redirect = quote_plus(REDIRECT_URI)
    auth_url = f"https://login.paytmmoney.com/merchant-login?apiKey={CLIENT_ID}&state=xyz"

    return redirect(auth_url)


@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")
    if not request_token:
        return "Missing request_token", 400

    payload = {
        "api_key": CLIENT_ID,
        "api_secret_key": CLIENT_SECRET,
        "request_token": request_token,
    }

    try:
        resp = requests.post(TOKEN_URL, json=payload, timeout=10)
        resp.raise_for_status()
        tokens = resp.json()
        return jsonify(tokens)
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500

@app.route("/test-env")
def test_env():
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    return "❌ Environment variables missing!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
