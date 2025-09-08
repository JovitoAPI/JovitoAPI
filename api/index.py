import os
import requests
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template, jsonify

app = Flask(__name__, template_folder="templates")

# === Environment Variables ===
# Make sure these are set in Vercel
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
    else:
        return "❌ Environment variables NOT found!"


@app.route("/login")
def login():
    # Paytm login URL with api_key and a state key
    state_key = "mystate123"  # any string you want; will be returned by Paytm
    enc_redirect = quote_plus(REDIRECT_URI)
    login_url = f"{AUTH_BASE}?apiKey={CLIENT_ID}&state={state_key}&redirect_uri={enc_redirect}"
    return redirect(login_url)


@app.route("/callback")
def callback():
    # Paytm redirects to this with ?request_token=xxx
    request_token = request.args.get("request_token")
    if not request_token:
        return "❌ Missing request_token in callback URL", 400

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


# === Only for local testing; Vercel ignores this ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
