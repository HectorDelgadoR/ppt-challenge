import openai
from flask import Blueprint, current_app, jsonify, request

from app.models import CoverageEligibility, Drug, db


def get_or_create_coverage_eligibilities(coverage_eligibilities):
    """
    Get or create coverage_eligibilities from the database
    """
    coverage_elibilities_output = []
    for coverage_eligibility in coverage_eligibilities:
        eligibility = CoverageEligibility.query.filter_by(
            eligibility=coverage_eligibility
        ).first()
        if not eligibility:
            eligibility = CoverageEligibility(eligibility=coverage_eligibility)
            db.session.add(eligibility)
        coverage_elibilities_output.append(eligibility)
    db.session.commit()
    return coverage_elibilities_output


def get_or_create_drugs(drug_names):
    """
    Get or create drugs from the database
    """
    drugs_output = []
    for drug_name in drug_names:
        drug = Drug.query.filter_by(name=drug_name).first()
        if not drug:
            drug = Drug(name=drug_name)
            db.session.add(drug)
        drugs_output.append(drug)
    db.session.commit()
    return drugs_output


def extract_eligibility_details_info(eligibility_details):
    client = openai.OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {
                "role": "user",
                "content": 'Extract the following parameters from the given "EligibilityDetails" text and return them as a Python tuple:\n\n'
                '- eligibility (string): A short summary of the overall eligibility criteria (e.g., "Patient must have commercial insurance and be a legal resident of the US").\n'
                "- us_residency (true/false): Whether the patient must be a legal U.S. resident.\n"
                "- minimum_age (integer or None): If an age requirement is mentioned, return the minimum age; otherwise, return `None`.\n"
                "- insurance_coverage (true/false): Whether the patient must have insurance.\n"
                '- eligibility_length (string or None): The eligibility duration (e.g., "12m" for 12 months) if specified; otherwise, return `None`.\n\n'
                "Return only a valid Python tuple, without explanations or additional text.\n\n"
                'Example output format:\n("Patient must have commercial insurance and be a legal resident of the US", True, 18, True, "12m")\n\n'
                'Here is the "EligibilityDetails" text:\n'
                f'"{eligibility_details}"',
            },
        ],
    )
    parsed_tuple = eval(response.choices[0].message.content)
    return parsed_tuple


def extract_program_details_info(program_details):
    client = openai.OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {
                "role": "user",
                "content": 'Extract the following parameters from the given "ProgramDetails" text and return them as a Python tuple:\n\n'
                '- program (string): A short summary of the program\'s benefit (e.g., "Patients may pay as little as $0 for every month of Dupixent").\n'
                '- min_out_of_pocket (float): The minimum amount a patient has to pay. If "$0" or similar is mentioned, return 0.0.\n'
                '- renewal (string): A short summary of how the program handles renewal (e.g., "Automatically re-enrolled every January 1st").\n\n'
                "Return only a valid Python tuple, without explanations or additional text.\n\n"
                'Example output format:\n("Patients may pay as little as $0 for every month of Dupixent", 0.0, "Automatically re-enrolled every January 1st")\n\n'
                'Here is the "ProgramDetails" text:\n'
                f'"{program_details}"',
            },
        ],
    )
    parsed_tuple = eval(response.choices[0].message.content)
    return parsed_tuple


def extract_expiration_date_info(expiration_date):
    client = openai.OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {
                "role": "user",
                "content": 'Extract the expiration date from the given "ExpirationDate" text and return it as a Python string.\n\n'
                "Return only a valid Python string, without explanations or additional text.\n\n"
                "Example output format:\n17/12/2025\n\n"
                'Here is the "ExpirationDate" text:\n'
                f'"{expiration_date}"',
            },
        ],
    )
    parsed_string = response.choices[0].message.content
    return parsed_string
