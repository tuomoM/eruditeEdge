from flask import Flask, Blueprint, session
import db
from views import user, vocab, train, entry,user_info
from config import Config



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(user.user_bp)
    app.register_blueprint(vocab.vocab_bp)
    app.register_blueprint(train.train_bp)
    app.register_blueprint(entry.entry_bp)
    app.register_blueprint(user_info.user_info_bp)

    return app