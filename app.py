from flask import Flask, Blueprint, session
from flask import render_template
import db
from views import register, main, login, logout, maintain, edit, update, train_fl
import config



def create_app():
    app = Flask(__name__)
    app.secret_key = config.secret_key
    app.register_blueprint(register.register_bp)
    app.register_blueprint(main.main_bp)
    app.register_blueprint(login.login_bp)
    app.register_blueprint(logout.logout_bp)
    app.register_blueprint(maintain.maintain_bp)
    app.register_blueprint(edit.edit_bp)
    app.register_blueprint(update.update_bp)
    app.register_blueprint(train_fl.train_fl_bp)

    return app