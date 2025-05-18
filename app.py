from flask import Flask, Blueprint, session
from flask import render_template
import db
from views import register, main, login, logout
import config



def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key
    app.register_blueprint(register.register_bp)
    app.register_blueprint(main.main_bp)
    app.register_blueprint(login.login_bp)
    app.register_blueprint(logout.logout_bp)
    return app