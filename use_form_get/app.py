from flask import Flask, render_template, request


class Message:
    def __init__(self, id, user_name, contents):
        self.id=id
        self.user_name=user_name
        self.contents=contents


app=Flask(__name__)
login_user_name="osamu"
message_list=[
    Message("202509190127", "osamu", "( ^^) _U~~"),
    Message("202509190228", "noriko", "( ^)o(^ )"),
    Message("202509190255", "osamu", "( ´∀｀ )")
]


@app.route("/")
def index():
    search_word=request.args.get("search_word")
    if search_word is None:
        return render_template(
            "top.html", login_user_name=login_user_name, message_list=message_list
        )
    else:
        filtered_message_list=[
            message for message in message_list if search_word in message.contents
        ]
        return render_template(
            "top.html",
            login_user_name=login_user_name,
            message_list=filtered_message_list,
            search_word=search_word
        )


@app.route("/write", methods=["GET", "POST"])
def write():
    return render_template("write.html")


if __name__=="__main__":
    app.run(debug=True)