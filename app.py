import os
from flask import Flask, redirect, request

app = Flask(__name__)

# 🔐 Read secrets from Vercel Environment Variables
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYTM_CLIENT_SECRET")
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI")

@app.route("/")
def index():
    # Build the Paytm OAuth2 URL
    auth_url = (
        f"https://developer.paytmmoney.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}&response_type=code&scope=read&redirect_uri={REDIRECT_URI}"
    )
    return f"""
        <h1>🚀 Paytm Money Authentication</h1>
        <p>Click below to authorize with Paytm Money:</p>
        <a href="{auth_url}">
            <button style="padding:12px 24px; font-size:16px; cursor:pointer;">
                Authorize with Paytm Money
            </button>
        </a>
    """

@app.route("/callback")
def callback():
    # Paytm Money will send ?code=XYZ here
    code = request.args.get("code")
    return f"<h1>Authorization Code:</h1><p>{code}</p>"
