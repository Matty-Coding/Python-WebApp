from config import Config
from flask import Flask, request, redirect, url_for, current_app
from app.database.models import db, User
from flask_session import Session
from flask_migrate import Migrate
from flask_login.login_manager import LoginManager
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta, datetime, timezone

# memory cache for blocked ips
blocked_ips = {}

# limiter configuration
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour", "50 per minute"],
    storage_uri="memory://",
    headers_enabled=True,
)


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Login manager initialization
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    # User loader managed by login manager (flask_login)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Database initialization + migrations
    db.init_app(app)
    Migrate(app, db)

    # Adding db to SQLALCHEMY Session
    app.config["SESSION_SQLALCHEMY"] = db

    # Session initialization
    Session(app)

    # Limiter initialization
    limiter.init_app(app)

    # Error handlers for limiter
    @app.errorhandler(429)
    def ratelimit_handler(e):
        ip = request.headers.get("X-Forwarded-For") or get_remote_address()
        blocked_ips[ip] = datetime.now(timezone.utc) + timedelta(minutes=1)
        current_app.logger.warning(
            f"⚠️  Rate limit exceeded for IP: {ip} until {blocked_ips[ip]}"
        )

        return redirect(url_for("auth.block"))

    # Force block ip addresses
    @app.before_request
    def check_block_ip():
        ip = request.headers.get("X-Forwarded-For") or get_remote_address()
        unblock_time = blocked_ips.get(ip)
        if unblock_time and unblock_time > datetime.now(timezone.utc):
            if request.endpoint not in ("auth.block", "static"):
                return redirect(url_for("auth.block"))
        elif unblock_time and unblock_time <= datetime.now(timezone.utc):
            blocked_ips.pop(ip, None)

    # Talisman
    # Configuring Content Security Policy to serve CDN Framework like Bootstrap
    csp = {
        "default-src": "'self'",
        "style-src": "'self' https://cdn.jsdelivr.net",
        "script-src": "'self' https://cdn.jsdelivr.net",
        "font-src": "'self' https://cdn.jsdelivr.net",
        "img-src": "'self' data:",
    }

    Talisman(app, content_security_policy=csp)

    # CSRF Protection
    CSRFProtect(app)

    # Blueprints initialization
    from app.blueprints.auth.routes import auth_bp

    app.register_blueprint(auth_bp)

    from app.blueprints.dashboard.routes import dashboard_bp

    app.register_blueprint(dashboard_bp)

    return app
