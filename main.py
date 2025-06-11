from flask import Flask, jsonify
from monitor import Monitor

app = Flask(__name__)

monitor = Monitor()

@app.route("/api/stats")
def all_stats():
    return jsonify(monitor.get_all())

@app.route("/api/stats/cpu")
def cpu_stats():
    return jsonify(monitor.cpu_stat())

@app.route("/api/stats/ram")
def ram_stats():
    return jsonify(monitor.ram_stat())

@app.route("/api/stats/disk")
def disk_stats():
    return jsonify(monitor.disk_stat())





if __name__ == "__main__":
    app.run(debug=True)
