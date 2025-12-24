from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    session,
    request,
)
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth.forms import (
    RegistrationForm,
    LoginForm,
    ResetPasswordForm,
    NewPasswordForm,
)
from app.database.crud_operations import UserCRUD, EmailTokenCRUD
from werkzeug.security import check_password_hash
from app.services.mail_sender import sendmail
from datetime import datetime, timezone, timedelta
from app import limiter, blocked_ips
from flask_limiter.util import get_remote_address

# Register blueprint
auth_bp = Blueprint(
    name="auth",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/auth",
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    user_crud = UserCRUD()

    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if form.validate_on_submit():
        if user_crud.get_by_email(email=form.email.data):
            flash("Email already exists.", "warning")
            return render_template("register.html", form=form)

        # try-except block to catch errors
        try:
            user_obj = user_crud.create(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )

            # should send token to email to authenticate user

            # load into session
            session["user_id"] = user_obj.id

            # log user and redirect into protected route
            login_user(user_obj)
            flash("Registration successful.", "success")

            return redirect(url_for("dashboard.index"))

        except Exception as e:
            current_app.logger.error(f"❗  Error creating user: {e}")
            flash("Registration failed.", "danger")
            return render_template("register.html", form=form)

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5/minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    user_crud = UserCRUD()

    if form.validate_on_submit():
        user_obj = user_crud.get_by_email(email=form.email.data)
        if not user_obj:
            flash("User not found.", "warning")
            return render_template("login.html", form=form)

        if not check_password_hash(user_obj.hash_pwd, form.password.data):
            flash("Invalid Credentials.", "danger")
            return render_template("login.html", form=form)

        # load into session
        session["user_id"] = user_obj.id

        # log user and redirect into protected route
        login_user(user_obj, remember=form.remember.data)
        flash("Login successful.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))

    logout_user()
    session.clear()
    flash("Logout successful.", "success")
    current_app.logger.info("✅  User logged out.")
    return redirect(url_for("auth.login"))


@auth_bp.route("/reset-password-request", methods=["GET", "POST"])
@limiter.limit("5/minute")
def reset_password_request():
    form = ResetPasswordForm()
    user_crud = UserCRUD()
    email_token_crud = EmailTokenCRUD()

    if form.validate_on_submit():
        user_obj = user_crud.get_by_email(email=form.email.data)
        if not user_obj:
            flash("User not found.", "warning")
            return render_template("reset_password_request.html", form=form)

        try:
            email_token_obj = email_token_crud.create(user_id=user_obj.id)

            server_url = url_for(
                "auth.reset_password", token=email_token_obj.token, _external=True
            )
            if not sendmail(
                email=user_obj.email,
                subject="Reset Password",
                content=f"To reset your password, click the link below:\n\n{server_url}",
            ):

                flash("Error sending email.", "danger")
                return render_template("reset_password_request.html", form=form)

            flash("Email sent successfully.", "success")
            return render_template("reset_password_request.html", form=form)

        except Exception as e:
            current_app.logger.error(f"❗  Error creating email token: {e}")
            flash("Error creating email token.", "danger")
            return render_template("reset_password_request.html", form=form)

    return render_template("reset_password_request.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
@limiter.limit("3/hour")
def reset_password(token):
    form = NewPasswordForm()
    user_crud = UserCRUD()
    crud_email_token = EmailTokenCRUD()

    token_obj = crud_email_token.get_by_token(token=token)

    if not token_obj:
        flash("Token not found.", "warning")
        return redirect(url_for("auth.reset_password_request"))

    if token_obj.used or token_obj.expires_at.replace(
        tzinfo=timezone.utc
    ) < datetime.now(timezone.utc):
        flash("Token expired or already used.", "warning")
        return redirect(url_for("auth.reset_password_request"))

    if form.validate_on_submit():
        try:
            user_crud.update_password(
                user_id=token_obj.user_id, password=form.password.data
            )
            crud_email_token.validate_token(user_id=token_obj.user_id)
            flash("Password updated successfully.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            current_app.logger.error(f"❗  Error updating password: {e}")
            flash("Error updating password.", "danger")

    return render_template("reset_password.html", form=form, token=token)


@auth_bp.route("/block", methods=["GET", "POST"])
def block():
    ip = request.headers.get("X-Forwarded-For") or get_remote_address()
    unblock_time = blocked_ips.get(ip)
    if not unblock_time:
        return redirect(url_for("auth.login"))

    remaining_time = max(
        0, int((unblock_time - datetime.now(timezone.utc)).total_seconds())
    )

    return render_template("block.html", retry_after=remaining_time)
