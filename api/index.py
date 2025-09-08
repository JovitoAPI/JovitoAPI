from flask import Flask, request, jsonify

# Create the Flask app first
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask app is running on Vercel!"

@app.route("/callback")
def callback():
    # Later: handle Paytm request_token here
    return "Callback route hit!"
