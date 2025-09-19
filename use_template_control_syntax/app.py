from flask import Flask, render_template


app = Flask(__name__)


class Message:
    def __init__(self, id, user_name, contents):
        self.id = id
        self.user_name = user_name
        self.contents = contents


@app.route("/")
def index():
    login_user_name = None
    message_list = [
        Message("202400502102310", "Sari", "朝からビールですか！楽しみです。"),
        Message("202400502100223", "Nox", "こちらこそ！次回はABコースで！"),
        Message("202400502092101", "Sari", "昨日はABコース楽しかったです！"),
    ]
    return render_template(
        "top.html", login_user_name=login_user_name, message_list=message_list
    )


@app.route("/write")
def write():
    return render_template("write.html")


if __name__ == "__main__":
    app.run(debug=True)