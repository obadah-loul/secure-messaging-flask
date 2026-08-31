from datetime import datetime, timezone

from flask_login import UserMixin

from app.extensions import bcrypt, db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(128),
        nullable=False,
    )

    public_key = db.Column(
        db.Text,
        nullable=False,
    )

    encrypted_private_key = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def set_password(self, password):
        self.password_hash = (
            bcrypt.generate_password_hash(password)
            .decode("utf-8")
        )

    def check_password(self, password):
        return bcrypt.check_password_hash(
            self.password_hash,
            password,
        )

    def __repr__(self):
        return f"<User {self.email}>"
