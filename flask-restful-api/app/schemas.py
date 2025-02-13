from marshmallow import Schema, fields


class RequirementSchema(Schema):
    name = fields.Str()
    value = fields.Str()


class BenefitSchema(Schema):
    name = fields.Str()
    value = fields.Str()


class FormSchema(Schema):
    name = fields.Str()
    link = fields.Str()


class DetailSchema(Schema):
    eligibility = fields.Str()
    program_detail = fields.Str()
    renewal = fields.Str()
    income = fields.Str()


class DrugSchema(Schema):
    name = fields.Str()


class ProgramSchema(Schema):
    id = fields.Int(dump_only=True)
    program_name = fields.Str()
    program_type = fields.Str()
    help_line = fields.Str()
    last_updated = fields.Str()
    free_trial_offer = fields.Str()
    expiration_date = fields.Str()
    requirements = fields.List(fields.Nested(RequirementSchema))
    benefits = fields.List(fields.Nested(BenefitSchema))
    forms = fields.List(fields.Nested(FormSchema))
    funding = fields.Method("get_funding")
    details = fields.List(fields.Nested(DetailSchema))
    drugs = fields.List(fields.Nested(DrugSchema))
    funding = fields.Method("get_funding")
    coverage_eligibilities = fields.List(fields.Str())

    def get_funding(self, obj):
        return {
            "evergreen": obj.funding_evergreen,
            "current_funding_level": obj.funding_current_level,
        }
