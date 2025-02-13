import json

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from app.models import (Benefit, Detail, Form, Program, Requirement, db,
                        end_of_current_year)
from app.utils.etl_utils import (extract_eligibility_details_info,
                                 extract_expiration_date_info,
                                 extract_program_details_info,
                                 get_or_create_coverage_eligibilities,
                                 get_or_create_drugs)


class ETLView(Resource):
    def post(self):
        if "file" not in request.files:
            return {"message": "No file part in the request"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"message": "No selected file"}, 400

        if file and file.filename.endswith(".json"):
            try:
                data = json.load(file)
                # Process the JSON data as needed
                program = self.create_program(data)

                program_details, min_out_of_pocket, renewal = (
                    extract_program_details_info(data["ProgramDetails"])
                )
                coverage_eligibilities = get_or_create_coverage_eligibilities(
                    coverage_eligibilities=data["CoverageEligibilities"]
                )
                if coverage_eligibilities:
                    program.coverage_eligibilities.extend(coverage_eligibilities)
                drugs = get_or_create_drugs(data.get("Drugs", []))
                if drugs:
                    program.drugs.extend(drugs)

                self.create_form(data, program.id)

                self.create_benefits(data, program.id, min_out_of_pocket)

                eligibility = self.create_requirements(data, program.id)

                detail = Detail(
                    program_id=program.id,
                    eligibility=eligibility,
                    program_detail=program_details,
                    renewal=renewal,
                    income=(
                        data["IncomeDetails"] if data["IncomeReq"] else "Not required"
                    ),
                )
                db.session.add(detail)
                db.session.commit()
                return {"message": "File successfully parsed"}, 201
            except json.JSONDecodeError:
                return {"message": "Invalid JSON file"}, 400
            except IntegrityError:
                db.session.rollback()
                return {"message": "Program already exists"}, 400
            except Exception as e:
                print(e)
                print(type(e))
                db.session.rollback()
                return {"message": "Unexpected error"}, 400
        else:
            return {"message": "Unsupported file type"}, 400

    def create_form(self, data, program_id):
        form = Form(
            program_id=program_id, name="Enrollment Form", link=data["EnrollmentURL"]
        )
        db.session.add(form)

    def create_requirements(self, data, program_id):
        (
            eligibility,
            us_residency,
            minimum_age,
            insurance_coverage,
            eligibility_length,
        ) = extract_eligibility_details_info(data["EligibilityDetails"])
        requirement_minimum_age = Requirement(
            program_id=program_id,
            name="minimum_age",
            value=minimum_age if minimum_age else "18",
        )
        db.session.add(requirement_minimum_age)
        requirement_insurange_coverage = Requirement(
            program_id=program_id,
            name="insurance_coverage",
            value=str(insurance_coverage).lower(),
        )
        db.session.add(requirement_insurange_coverage)
        requirements_us_residency = Requirement(
            program_id=program_id, name="us_residency", value=str(us_residency).lower()
        )
        db.session.add(requirements_us_residency)
        requirement_eligibility_length = Requirement(
            program_id=program_id,
            name="eligibility_length",
            value=eligibility_length if eligibility_length else "12m",
        )
        db.session.add(requirement_eligibility_length)
        return eligibility

    def create_benefits(self, data, program_id, min_out_of_pocket):
        benefit_max_annual_savings = Benefit(
            program_id=program_id,
            name="max_annual_savings",
            value=str(
                float(data["AnnualMax"].replace("$", "").replace(",", "").strip())
            ),
        )
        db.session.add(benefit_max_annual_savings)
        benefit_min_out_of_pocket = Benefit(
            program_id=program_id, name="min_out_of_pocket", value=min_out_of_pocket
        )
        db.session.add(benefit_min_out_of_pocket)

    def create_program(self, data):
        expiration_date = (
            extract_expiration_date_info(data.get("ExpirationDate"))
            if data.get("ExpirationDate")
            else end_of_current_year()
        )
        program = Program(
            id=data["ProgramID"],
            program_name=data["ProgramName"],
            program_type=data["AssistanceType"],
            funding_evergreen=str(data["OfferRenewable"]).lower(),
            funding_current_level=(
                ", ".join(data["FundLevels"])
                if data["FundLevels"]
                else "Data Not Available"
            ),
            help_line=data.get("HelpLine"),
            free_trial_offer=str(
                data.get("FreeTrialOffer", "Data Not Available")
            ).lower(),
            expiration_date=expiration_date,
        )
        program.last_updated = (
            data.get("LastUpdated")
            if data.get("LastUpdated")
            else db.func.current_date()
        )
        db.session.add(program)
        db.session.commit()
        return program
