import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot Running!"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()

    print("收到訊息：")
    print(body)

    return "OK"

if __name__ == "__main__":
    app.run()
