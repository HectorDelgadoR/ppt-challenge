from flask import Blueprint

from app.resources.api_view import ProgramAPI, ProgramQueryAPI
from app.resources.etl_view import ETLView

api_bp = Blueprint("api", __name__)

api_bp.add_url_rule("/upload", view_func=ETLView.as_view("etl_view"))

program_view = ProgramAPI.as_view("program_api")
api_bp.add_url_rule(
    "/programs/<int:program_id>", view_func=program_view, methods=["GET"]
)

api_bp.add_url_rule(
    "/programs", view_func=ProgramQueryAPI.as_view("program_query_api"), methods=["GET"]
)


def init_routes(app):
    app.register_blueprint(api_bp, url_prefix="/api")
