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
    params = request.args.to_dict()
    if not params:
        return "❌ No query parameters received from Paytm", 400
    return jsonify({"received_params": params})
