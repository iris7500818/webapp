from flask import Flask


app: Flask = Flask(__name__)


@app.route("/")
def index():
    return "<h1>これは掲示板のトップページです。</h1>"


@app.route("/write", methods=["GET"])
def write_by_get_method():
    return """
        <html>
        <body>
        <h1>これは掲示板書き込みページです。</h1>
        <h3>書き込み内容：</h3>
        <form action="/write" method="POST">
            <textarea name="msg" rows="5" cols="70"></textarea><br></br>
            <input type="submit" value="書き込み">
        </form>
        </body>
        </html>
    """


@app.route("/write", methods=["POST"])
def write_by_post_method():
    return "<h1>書き込みを受け付けました。</h1>"


@app.route("/edit/<int:message_id>")
def edit(message_id):
    return f"<h1>これはID={message_id}の編集ページです。</h1>"


if __name__ == "__main__":
    app.run(debug=True)