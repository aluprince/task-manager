from flask import Flask
from routes.user_routes import auth_bp
from routes.task_routes import task_bp
from config import db

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome home still under Development"


# blueprints
app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(task_bp, url_prefix="/")


if __name__ == "__main__":
    app.run(debug=True)



















