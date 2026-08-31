from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app.extensions import db
from app.models.user import User
from crypto.rsa_utils import generate_rsa_key_pair, encrypt_private_key


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("chat.chat"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "danger")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return render_template("register.html")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("An account with this email already exists.", "danger")
            return render_template("register.html")

        private_key, public_key = generate_rsa_key_pair()

        encrypted_private_key = encrypt_private_key(
            private_key,
            current_app.config["PRIVATE_KEY_ENCRYPTION_KEY"],
        )

        user = User(
            email=email,
            public_key=public_key.decode("utf-8"),
            encrypted_private_key=encrypted_private_key,
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("chat.chat"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        login_user(user)

        return redirect(url_for("chat.chat"))

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for("auth.login"))
