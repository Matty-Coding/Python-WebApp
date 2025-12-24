from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint(
    name="dashboard",
    import_name=__name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/",
)


@dashboard_bp.route("/")
def home():
    return render_template("index.html")


@dashboard_bp.route("/dashboard")
@login_required
def index():
    return render_template("dashboard.html")
