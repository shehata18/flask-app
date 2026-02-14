from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Flaskkkkk 🚀</h1><p>Deployed on Ubuntu VM</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
