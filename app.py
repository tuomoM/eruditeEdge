from flask import Flask, Blueprint, session
from flask import render_template
import db
from views import register



def create_app():
    app = Flask(__name__)

    app.register_blueprint(register.register_bp)

    return app


"""
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")
"""