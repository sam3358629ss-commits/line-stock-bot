import os
from flask import Flask, request
from linebot import LineBotApi
from linebot.models import TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(
    os.getenv("CHANNEL_ACCESS_TOKEN")
)

@app.route("/")
def home():
    return "LINE Bot Running!"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()

    for event in body["events"]:
        if event["type"] == "message":
            if event["message"]["type"] == "text":

                user_text = event["message"]["text"]

                line_bot_api.reply_message(
                    event["replyToken"],
                    TextSendMessage(
                        text=f"收到股票代號：{user_text}"
                    )
                )

    return "OK"
