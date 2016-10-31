from flask import Flask

app = Flask(__name__)

# Error handling and automatic reload
app.config["DEBUG"] = True

@app.route("/")
@app.route("/hello")

def hello_world():
    return "Ola, Mundo!"
    
# Dynamic Route
@app.route("/test/<search_query>")
def search(search_query):
    return search_query
    
# Testing parameters converters
@app.route("/integer/<int:valor>")
def tipo_int(valor):
    print valor + 1
    return "Correcto!"

@app.route("/float/<float:valor>")
def tipo_float(valor):
    print valor + 1.6
    return "Correcto!"

@app.route("/path/<path:valor>")
def tipo_caminho(valor):
    print valor
    return "Caminho correcto!"
    
# Returning the status code explicitly
@app.route("/nome/<nome>")
def index(nome):
    if nome.lower() == "pedro":
        return "Ola, {}".format(nome), 200
    else:
        return "Nao encontrado", 404
    
if __name__ == "__main__":
    app.run("0.0.0.0",8080)