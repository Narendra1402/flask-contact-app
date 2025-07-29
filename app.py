from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow CORS for requests from your frontend (e.g., GitHub Pages)

@app.route("/send", methods=["POST"])
def send_email():
    data = request.get_json()

    EMAIL_SENDER = os.environ.get("EMAIL_USER")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

    # Debug (optional) - logs to Render console
    print("Logging in as:", EMAIL_SENDER)
    print("Password present:", bool(EMAIL_PASSWORD))

    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return jsonify({"error": "Email credentials are not set"}), 500

    msg = EmailMessage()
    msg["Subject"] = f"Contact Form: {data.get('visit', 'No Subject')}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_SENDER  # Receive the form at your own email address

    body = f"""
    You received a new contact form submission:

    Name: {data.get('fullname')}
    Email: {data.get('email')}
    Visit Time: {data.get('meeting')}
    Message: {data.get('notes')}
    """

    msg.set_content(body)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


# Needed for Render to detect correct port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
