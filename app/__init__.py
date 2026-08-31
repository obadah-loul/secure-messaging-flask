from flask import Flask

from config import Config
from app.extensions import bcrypt, csrf, db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.models.user import User
    from app.models.message import Message

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(
                User,
                int(user_id),
            )
        except (TypeError, ValueError):
            return None

    from app.routes.auth import auth_bp
    from app.routes.chat import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    with app.app_context():
        db.create_all()

    return app
