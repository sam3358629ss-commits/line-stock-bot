from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "LINE Bot Running!"

@app.route("/callback")
def callback():
    return "OK"

if __name__ == "__main__":
    app.run()
