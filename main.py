import config.db
from flask import Flask, render_template, request, jsonify
from routes.user_routes import auth_bp
from routes.task_routes import task_bp
from dotenv import load_dotenv, find_dotenv
from routes.task_routes import token_required

load_dotenv(find_dotenv())

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
@token_required
def dashboard():
    return render_template("dashboard.html")


# blueprints
app.register_blueprint(auth_bp, url_prefix="/")
app.register_blueprint(task_bp, url_prefix="/")


if __name__ == "__main__":
    app.run(debug=True)



















