from flask import Flask

app: Flask = Flask(__name__)

@app.route("/")
def hello_world():
    age = 22
    return "<h1>I'm " + str(age) + " years old.</h1>"

if __name__ == "__main__":
    app.run(debug=True)