@app.route("/callback")
def callback():
    code = request.args.get("request_token")  # ✅ Paytm uses request_token, not code
    if not code:
        return "❌ Missing request_token in callback URL", 400

    payload = {
        "api_key": CLIENT_ID,
        "api_secret_key": CLIENT_SECRET,
        "request_token": code,
    }

    try:
        resp = requests.post(
            "https://developer.paytmmoney.com/accounts/v2/gettoken",
            json=payload,
            timeout=10
        )
        # Debug log
        return f"🔍 Paytm Response: {resp.status_code} {resp.text}", resp.status_code
    except requests.exceptions.RequestException as e:
        return f"Token request failed: {e}", 500
