from flask import Blueprint, jsonify
from flask.views import MethodView
from werkzeug.exceptions import NotFound

from app.models import Program
from app.schemas import ProgramSchema


class ProgramAPI(MethodView):
    def get(self, program_id):
        try:
            program = Program.query.get_or_404(program_id)
        except NotFound:
            return jsonify({"error": f"Program with ID {program_id} not found"}), 404

        program_schema = ProgramSchema()
        result = program_schema.dump(program)

        return jsonify(result), 200
