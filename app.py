from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🚀 Welcome to Your Trading Bot Site</h1>
    <p>Click below to log in with Paytm Money:</p>
    <a href="https://developer.paytmmoney.com/oauth2/authorize?client_id=b1928e80f02b43eea5551c257d238674&response_type=code&scope=read&redirect_uri=https://paytm-auth-site.vercel.app/callback">
        <button>Authorize with Paytm Money</button>
    </a>
    """

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if code:
        return f"<h2>✅ Authorization Code:</h2><p>{code}</p>"
    else:
        return "<h2>⚠️ No code found in URL</h2>"
