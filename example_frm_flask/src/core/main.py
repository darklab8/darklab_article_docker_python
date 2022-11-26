from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return dict(msg="Hello, World!")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8000")