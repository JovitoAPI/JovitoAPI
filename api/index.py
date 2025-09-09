import os
import requests
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__, template_folder="templates")

# === Environment Variables ===
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET", "")
REDIRECT_URI = "https://paytm-auth-site.vercel.app/callback"

# === Paytm URLs ===
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
    else:
        return "❌ Environment variables NOT found!"

@app.route("/login")
def login():
    if not CLIENT_ID:
        return "❌ Missing CLIENT_ID!", 500
    state_key = "test_state"
    auth_url = f"{AUTH_BASE}?apiKey={CLIENT_ID}&state={state_key}"
    return redirect(auth_url)

# === Callback route: exchange requestToken for access tokens ===
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

        # Debug output if not OK
        if resp.status_code != 200:
            return (
                f"❌ Token request failed\n"
                f"Status: {resp.status_code}\n"
                f"Body: {resp.text}"
            ), 500

        # Try parsing JSON
        try:
            return jsonify(resp.json())
        except Exception:
            return f"❌ Response not JSON:\n{resp.text}", 500

    except Exception as e:
        return f"❌ Unexpected error: {str(e)}", 500
