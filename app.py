from flask import Flask, redirect, request
import os

app = Flask(__name__)

# Load environment variables
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID")
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI")

@app.route("/")
def home():
    return """
    <h1>🚀 Welcome to Your Trading Bot Site</h1>
    <p>Click below to log in with Paytm Money:</p>
    <a href="/login"><button>Login with Paytm Money</button></a>
    """

@app.route("/login")
def login():
    auth_url = (
        "https://developer.paytmmoney.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&scope=read"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    return f"<h2>Authorization Code: {code}</h2>"
