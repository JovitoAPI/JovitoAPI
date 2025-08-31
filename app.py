from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>🚀 Paytm Money Auth Site</h1><p>Go to /authorize to start.</p>"

@app.route("/authorize")
def authorize():
    return render_template("index.html")  # loads templates/index.html

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if code:
        return f"<h1>✅ Authorization Code Received</h1><p>{code}</p>"
    else:
        return "<h1>❌ No authorization code found.</h1>"

# Required for local testing (Vercel will ignore this)
if __name__ == "__main__":
    app.run(debug=True)
