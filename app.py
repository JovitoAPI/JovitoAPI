import os
from urllib.parse import quote
from flask import Flask, request

app = Flask(__name__)

CLIENT_ID = os.getenv("PAYTM_CLIENT_ID", "")
REDIRECT_URI = os.getenv("PAYTM_REDIRECT_URI", "https://paytm-auth-site.vercel.app/callback")

AUTH_BASE = "https://developer.paytmmoney.com/oauth2/authorize"

@app.route("/")
def index():
    # URL-encode the redirect URI for safety
    enc_redirect = quote(REDIRECT_URI, safe="")
    auth_url = f"{AUTH_BASE}?client_id={CLIENT_ID}&response_type=code&scope=openid&redirect_uri={enc_redirect}"
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="UTF-8"><title>🚀 Paytm Money Authentication</title></head>
    <body style="font-family:Arial; text-align:center; margin-top:80px;">
      <h1>🚀 Welcome to Your Trading Bot Site</h1>
      <p>Click below to log in with Paytm Money:</p>
      <p><a href="{auth_url}">
        <button style="padding:12px 24px; font-size:16px; cursor:pointer;">Authorize with Paytm Money</button>
      </a></p>
    </body></html>
    """

@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")
    if code:
        return f"""
        <!DOCTYPE html>
        <html><head><meta charset="UTF-8"><title>Callback</title></head>
        <body style="font-family:Arial; margin:40px;">
          <h2>✅ Authorization Code Received</h2>
          <p>Copy this code into your notebook/app:</p>
          <pre style="background:#f6f8fa; padding:12px; border:1px solid #ddd;">{code}</pre>
        </body></html>
        """
    return f"""
    <!DOCTYPE html>
    <html><head><meta charset="UTF-8"><title>Callback</title></head>
    <body style="font-family:Arial; margin:40px;">
      <h2>⚠️ No code in URL</h2>
      <p>{'Error: ' + error if error else 'Try authorizing again from the home page.'}</p>
    </body></html>
    """

if __name__ == "__main__":
    # Local run for testing
    app.run(host="0.0.0.0", port=5000)
