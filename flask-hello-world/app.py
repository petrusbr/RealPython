from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/hello")

def hello_world():
    return "Ola, Mundo!"
    
if __name__ == "__main__":
    app.run("0.0.0.0",8080)