import base64

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.models.message import Message
from app.models.user import User
from crypto.aes_utils import decrypt_message, encrypt_message, generate_aes_key
from crypto.rsa_utils import decrypt_aes_key, encrypt_aes_key


chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/")
@chat_bp.route("/chat", methods=["GET", "POST"])
@login_required
def chat():

    if request.method == "POST":
        recipient_email = (
            request.form.get("recipient", "")
            .strip()
            .lower()
        )

        plaintext = request.form.get("message", "").strip()

        if not recipient_email or not plaintext:
            flash(
                "Recipient and message are required.",
                "danger",
            )
            return redirect(url_for("chat.chat"))

        if recipient_email == current_user.email:
            flash(
                "You cannot send a message to yourself.",
                "danger",
            )
            return redirect(url_for("chat.chat"))

        if len(plaintext) > 2000:
            flash(
                "Message is too long.",
                "danger",
            )
            return redirect(url_for("chat.chat"))

        recipient = User.query.filter_by(
            email=recipient_email
        ).first()

        if not recipient:
            flash(
                "Recipient account was not found.",
                "danger",
            )
            return redirect(url_for("chat.chat"))

        # Generate a unique AES-256 key for this message.
        aes_key = generate_aes_key()

        # Encrypt the actual message using AES-256-GCM.
        nonce, ciphertext = encrypt_message(
            aes_key,
            plaintext,
        )

        # Protect the AES key using the recipient's RSA public key.
        encrypted_aes_key = encrypt_aes_key(
            recipient.public_key,
            aes_key,
        )

        encrypted_message = Message(
            sender_id=current_user.id,
            recipient_id=recipient.id,
            encrypted_aes_key=base64.b64encode(
                encrypted_aes_key
            ).decode("utf-8"),
            nonce=base64.b64encode(
                nonce
            ).decode("utf-8"),
            ciphertext=base64.b64encode(
                ciphertext
            ).decode("utf-8"),
        )

        db.session.add(encrypted_message)
        db.session.commit()

        flash(
            "Encrypted message sent successfully.",
            "success",
        )

        return redirect(url_for("chat.chat"))

    messages = (
        Message.query
        .filter_by(recipient_id=current_user.id)
        .order_by(Message.created_at.desc())
        .all()
    )

    inbox = []

    for message in messages:
        try:
            encrypted_aes_key = base64.b64decode(
                message.encrypted_aes_key
            )

            nonce = base64.b64decode(
                message.nonce
            )

            ciphertext = base64.b64decode(
                message.ciphertext
            )

            aes_key = decrypt_aes_key(
                current_user.encrypted_private_key,
                encrypted_aes_key,
                current_app.config[
                    "PRIVATE_KEY_ENCRYPTION_KEY"
                ],
            )

            plaintext = decrypt_message(
                aes_key,
                nonce,
                ciphertext,
            )

        except Exception:
            plaintext = "[Unable to decrypt message]"

        inbox.append(
            {
                "sender": message.sender.email,
                "message": plaintext,
                "created_at": message.created_at,
            }
        )

    return render_template(
        "chat.html",
        inbox=inbox,
    )
