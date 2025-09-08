import os
import json
import requests
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__, template_folder="templates")

# === Environment Variables ===
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv(
    "PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback"
)

# === Paytm OAuth URLs ===
AUTH_BASE = "https://login.paytmmoney.com/merchant-login"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/v2/gettoken"

# === Routes ===

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test-env")
def test_env():
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    return "❌ Environment variables NOT found!"


@app.route("/login")
def login():
    if not CLIENT_ID or not CLIENT_SECRET:
        return "❌ Missing environment variables!", 500
    # Build URL-encoded redirect
    state_key = "test_state"  # can be any string
    auth_url = f"{AUTH_BASE}?apiKey={CLIENT_ID}&state={state_key}"
    return redirect(auth_url)


@app.route("/callback")
def callback():
    request_token = request.args.get("request_token")
    if not request_token:
        return "❌ Missing request_token in callback URL", 400

    # Prepare payload
    payload = {
        "api_key": CLIENT_ID,
        "api_secret_key": CLIENT_SECRET,
        "request_token": request_token,
    }

    try:
        resp = requests.post(TOKEN_URL, json=payload, timeout=10)
        resp.raise_for_status()
        tokens = resp.json()
        return jsonify(tokens)  # will show access_token + public_access_token + read_access_token
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500


if __name__ == "__main__":
    # Local dev only
    app.run(host="0.0.0.0", port=5000, debug=True)
