import os
from urllib.parse import quote_plus
from flask import Flask, redirect, request, render_template

app = Flask(__name__, template_folder="templates")

# Read secrets from environment (Vercel env vars or local .env if you use)
CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
# Ensure REDIRECT_URI matches what you registered on Paytm dev console
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

AUTH_BASE = "https://developer.paytmmoney.com/oauth2/authorize"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    # Build safe, URL-encoded redirect URI
    enc_redirect = quote_plus(REDIRECT_URI)
    auth_url = f"{AUTH_BASE}?client_id={CLIENT_ID}&response_type=code&scope=read&redirect_uri={enc_redirect}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if code:
        return f"""
        <!doctype html>
        <html><head><meta charset='utf-8'><title>Callback</title></head>
        <body style="font-family:Arial; margin:30px;">
          <h2>✅ Authorization Code Received</h2>
          <p>Copy this code and use it to exchange for an access token:</p>
          <pre style="background:#f6f8fa;padding:10px;border:1px solid #ddd;">{code}</pre>
        </body></html>
        """
    return f"""
    <!doctype html>
    <html><head><meta charset='utf-8'><title>Callback</title></head>
    <body style="font-family:Arial; margin:30px;">
      <h2>⚠️ No code in URL</h2>
      <p>{'Error: ' + error if error else 'Open the home page and click Authorize to start the login flow.'}</p>
    </body></html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
