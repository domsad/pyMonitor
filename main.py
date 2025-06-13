from flask import Flask, jsonify, render_template
from flasgger import Swagger
from monitor import Monitor

# tworzymy instancję aplikacji Flask i Swagger api doc
app = Flask(__name__)
swagger = Swagger(app)

monitor = Monitor()

# Endpoint zwracający wszystkie statystyki systemowe w formacie JSON
@app.route("/api/stats")
def all_stats():
    """Zwraca wszystkie statystyki systemowe
    ---
    responses:
      200:
        description: Wszystkie statystyki systemowe
    """
    return jsonify(monitor.get_all())


# Pojedyncze endpointy API – przydatne, gdy chcesz jakieś konkretne dane
@app.route("/api/stats/cpu")
def cpu_stats():
    """Zwraca statystyki CPU
    ---
    responses:
      200:
        description: Statystyki procesora
    """
    return jsonify(monitor.cpu_stat())

@app.route("/api/stats/ram")
def ram_stats():
    """Zwraca statystyki RAM
    ---
    responses:
      200:
        description: Statystyki pamięci RAM
    """
    return jsonify(monitor.ram_stat())

@app.route("/api/stats/disk")
def disk_stats():
    """Zwraca statystyki dysku
    ---
    responses:
      200:
        description: Statystyki dysku
    """
    return jsonify(monitor.disk_stat())


# Główna strona projektu renderuje plik html z danymi z api
@app.route("/")
def index():
    return render_template("index.html", stats=monitor.get_all())

if __name__ == "__main__":
    app.run()
