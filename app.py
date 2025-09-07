import requests
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

CLIENT_ID = "b1928e80f02b43eea5551c257d238674"
CLIENT_SECRET = "911f98860ffe4404a37816e897187cb2"
REDIRECT_URI = "https://paytm-auth-site.vercel.app/callback"

TOKEN_URL = "https://developer.paytmmoney.com/accounts/oauth/token"

@app.route("/")
def index():
    return render_template("index.html")

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
