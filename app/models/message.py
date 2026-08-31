from datetime import datetime, timezone

from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    recipient_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    encrypted_aes_key = db.Column(
        db.Text,
        nullable=False,
    )

    nonce = db.Column(
        db.Text,
        nullable=False,
    )

    ciphertext = db.Column(
        db.Text,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        backref="sent_messages",
    )

    recipient = db.relationship(
        "User",
        foreign_keys=[recipient_id],
        backref="received_messages",
    )

    def __repr__(self):
        return (
            f"<Message sender={self.sender_id} "
            f"recipient={self.recipient_id}>"
        )
