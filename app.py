from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot Running!"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()

    event = body["events"][0]

    if event["type"] == "message":
        print("收到訊息")

    return "OK"

if __name__ == "__main__":
    app.run()
