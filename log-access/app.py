from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "This is the base route. Try /logs to see the recent history."

@app.route("/logs")
def get_logs():
    try:
        with open("/app/logs/log") as f:
            logs = f.read()
    except FileNotFoundError:
        return "No logs here"
    
    return logs