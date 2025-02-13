from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def end_of_current_year():
    today = date.today()
    end_of_year = date(today.year, 12, 31)
    return end_of_year.strftime("%d/%m/%Y")


def current_date():
    return datetime.now().strftime("%d/%m/%Y")


program_coverage_eligibility = db.Table(
    "program_coverage_eligibility",
    db.Column("program_id", db.Integer, db.ForeignKey("programs.id"), primary_key=True),
    db.Column(
        "coverage_eligibility_id",
        db.Integer,
        db.ForeignKey("coverage_eligibilities.id"),
        primary_key=True,
    ),
)

program_drug = db.Table(
    "program_drug",
    db.Column("program_id", db.Integer, db.ForeignKey("programs.id"), primary_key=True),
    db.Column("drug_id", db.Integer, db.ForeignKey("drugs.id"), primary_key=True),
)


class Requirement(db.Model):
    __tablename__ = "requirements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)


class Benefit(db.Model):
    __tablename__ = "benefits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)


class Form(db.Model):
    __tablename__ = "forms"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(200), nullable=False)


class Detail(db.Model):
    __tablename__ = "details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program_id = db.Column(db.Integer, db.ForeignKey("programs.id"), nullable=False)
    eligibility = db.Column(db.String(500), nullable=False)
    program_detail = db.Column(
        db.String(500), nullable=False
    )  # Renamed to avoid conflict
    renewal = db.Column(db.String(500), nullable=False)
    income = db.Column(db.String(100), nullable=False)


class CoverageEligibility(db.Model):
    __tablename__ = "coverage_eligibilities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eligibility = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return self.eligibility


class Drug(db.Model):
    __tablename__ = "drugs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Drug {self.name}>"


class Program(db.Model):
    __tablename__ = "programs"

    id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(100), nullable=False)
    program_type = db.Column(db.String(50), nullable=False)
    funding_evergreen = db.Column(db.String(10), nullable=False, default=True)
    funding_current_level = db.Column(
        db.String(100), nullable=False, default="Data Not Available"
    )
    help_line = db.Column(db.String(100), nullable=True)
    last_updated = db.Column(db.String(12), nullable=False, default=current_date)
    free_trial_offer = db.Column(
        db.String(10), nullable=False, default="Data Not Available"
    )
    expiration_date = db.Column(
        db.String(12), nullable=False, default=end_of_current_year
    )
    requirements = db.relationship("Requirement", backref="program", lazy=True)
    benefits = db.relationship("Benefit", backref="program", lazy=True)
    forms = db.relationship("Form", backref="program", lazy=True)
    details = db.relationship("Detail", backref="program", lazy=True)
    coverage_eligibilities = db.relationship(
        "CoverageEligibility",
        secondary=program_coverage_eligibility,
        lazy="subquery",
        backref=db.backref("programs", lazy=True),
    )
    drugs = db.relationship(
        "Drug",
        secondary=program_drug,
        lazy="subquery",
        backref=db.backref("programs", lazy=True),
    )

    def __repr__(self):
        return f"<Program {self.program_name}>"
