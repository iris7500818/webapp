from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    login_user_name = "Sari"
    return render_template("top.html", login_user_name=login_user_name)


@app.route("/write")
def write():
    return render_template("write.html")


if __name__ == "__main__":
    app.run(debug=True)