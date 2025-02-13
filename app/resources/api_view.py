from flask import Blueprint, jsonify, request
from flask.views import MethodView
from werkzeug.exceptions import NotFound

from app.models import Program, CoverageEligibility
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


class ProgramQueryAPI(MethodView):
    def get(self):
        program_type = request.args.get('program_type')
        coverage_eligibilities = request.args.getlist('coverage_eligibilities')

        query = Program.query

        if program_type:
            query = query.filter_by(program_type=program_type)

        if coverage_eligibilities:
            query = query.join(Program.coverage_eligibilities).filter(CoverageEligibility.eligibility.in_(coverage_eligibilities))

        programs = query.all()
        program_schema = ProgramSchema(many=True)
        result = program_schema.dump(programs)

        return jsonify(result), 200