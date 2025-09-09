from flask import Flask, request, jsonify, render_template, redirect
import os
import requests

app = Flask(__name__, template_folder="templates")

# === Environment Variables ===
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
REDIRECT_URI = "https://paytm-auth-site.vercel.app/callback"

# === Routes ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/test-env")
def test_env():
    if CLIENT_ID and CLIENT_SECRET:
        return "✅ Environment variables are working!"
    else:
        return "❌ Environment variables NOT found!"

@app.route("/login")
def login():
    if not CLIENT_ID:
        return "❌ Missing CLIENT_ID!", 500
    state_key = "test_state"
    auth_url = f"https://login.paytmmoney.com/merchant-login?apiKey={CLIENT_ID}&state={state_key}"
    return redirect(auth_url)

# 🔍 Debugging version of callback
@app.route("/callback")
def callback():
    request_token = request.args.get("requestToken")
    if not request_token:
        return "❌ Missing request_token in callback URL", 400

    payload = {
        "api_key": CLIENT_ID,
        "api_secret_key": CLIENT_SECRET,
        "request_token": request_token
    }

    try:
        resp = requests.post(
            TOKEN_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        resp.raise_for_status()
        tokens = resp.json()
        return jsonify(tokens)  # shows access_token, public_access_token, read_access_token
    except requests.exceptions.RequestException as e:
        return f"❌ Token request failed: {e}", 500

