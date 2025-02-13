import json
from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Program, db


@pytest.fixture(scope="module")
def init_database(app):
    program = Program(
        id=1,
        program_name="Test Program",
        program_type="Coupon",
        funding_evergreen="true",
        funding_current_level="Data Not Available",
        help_line="123-456-7890",
        last_updated="01/01/2023",
        free_trial_offer="true",
        expiration_date="31/12/2023",
    )
    db.session.add(program)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()


def test_post_etl_view_no_file(client):
    response = client.post("/api/upload")
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "No file part in the request"


def test_post_etl_view_empty_file(client):
    data = {"file": (BytesIO(b""), "")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "No selected file"


def test_post_etl_view_invalid_json(client):
    data = {"file": (BytesIO(b"invalid json"), "test.json")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Invalid JSON file"


@patch("app.resources.etl_view.get_or_create_coverage_eligibilities")
@patch("app.resources.etl_view.get_or_create_drugs")
@patch("app.resources.etl_view.extract_eligibility_details_info")
@patch("app.resources.etl_view.extract_program_details_info")
@patch("app.resources.etl_view.extract_expiration_date_info")
def test_post_etl_view_success(
    mock_expiration_date,
    mock_program_details,
    mock_eligibility_details,
    mock_get_drugs,
    mock_get_coverage,
    client,
    init_database,
):
    mock_expiration_date.return_value = "31/12/2023"
    mock_program_details.return_value = ("Program details", "0.0", "Renewal details")
    mock_eligibility_details.return_value = (
        "Eligibility details",
        True,
        18,
        True,
        "12m",
    )
    mock_get_drugs.return_value = []
    mock_get_coverage.return_value = []

    json_data = {
        "ProgramID": 2,
        "ProgramName": "New Program",
        "AssistanceType": "Coupon",
        "OfferRenewable": "true",
        "FundLevels": ["Level 1", "Level 2"],
        "HelpLine": "987-654-3210",
        "FreeTrialOffer": "true",
        "ExpirationDate": "31/12/2023",
        "ProgramDetails": "Program details text",
        "EligibilityDetails": "Eligibility details text",
        "IncomeDetails": "Income details text",
        "IncomeReq": True,
        "CoverageEligibilities": ["Eligibility 1", "Eligibility 2"],
        "Drugs": ["Drug 1", "Drug 2"],
        "EnrollmentURL": "http://example.com/enrollment",
        "AnnualMax": "$1000",
        "MinOutOfPocket": "$0",
    }

    data = {"file": (BytesIO(json.dumps(json_data).encode("utf-8")), "test.json")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "File successfully parsed"


@patch("app.resources.etl_view.db.session.commit")
def test_post_etl_view_integrity_error(mock_commit, client, init_database):
    mock_commit.side_effect = IntegrityError(None, None, None)

    json_data = {
        "ProgramID": 3,
        "ProgramName": "Duplicate Program",
        "AssistanceType": "Coupon",
        "OfferRenewable": "true",
        "FundLevels": ["Level 1", "Level 2"],
        "HelpLine": "987-654-3210",
        "FreeTrialOffer": "true",
        "ExpirationDate": "31/12/2023",
        "ProgramDetails": "Program details text",
        "EligibilityDetails": "Eligibility details text",
        "IncomeDetails": "Income details text",
        "IncomeReq": True,
        "CoverageEligibilities": ["Eligibility 1", "Eligibility 2"],
        "Drugs": ["Drug 1", "Drug 2"],
        "EnrollmentURL": "http://example.com/enrollment",
        "AnnualMax": "$1000",
        "MinOutOfPocket": "$0",
    }

    data = {"file": (BytesIO(json.dumps(json_data).encode("utf-8")), "test.json")}
    response = client.post("/api/upload", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Program already exists"
