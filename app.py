import flask
from flask import request
import requests
import schedule
import time
import threading
import os

# Henter API-nøkler fra miljøvariabler
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID_FREE, TELEGRAM_CHAT_ID_VIP

# Flask-app
app = flask.Flask(__name__)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    print(f"📩 Mottatt data: {data}")  # LOGG INNOMMENDE MELDINGER

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text == "/sendtips":
            send_telegram_melding("✅ Her er dagens tips!", chat_id)

    return "OK", 200

# Funksjon for å sende meldinger
def send_telegram_melding(melding, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": melding, "parse_mode": "Markdown"}
    requests.post(url, json=data)

# Automatisk planlegging av meldinger
def send_daglige_tips():
    send_telegram_melding("🚀 Gratis tips!", TELEGRAM_CHAT_ID_FREE)
    send_telegram_melding("🔥 VIP tips!", TELEGRAM_CHAT_ID_VIP)

# Kjør meldinger hver dag kl. 12:00
schedule.every().day.at("12:00").do(send_daglige_tips)

# Start planlegging i en egen tråd
def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=start_scheduler, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
