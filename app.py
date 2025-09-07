import os
import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Pull credentials from Vercel environment variables
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET")
REDIRECT_URI = "https://paytm-auth-site.vercel.app/callback"
TOKEN_URL = "https://developer.paytmmoney.com/accounts/oauth/token"

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
