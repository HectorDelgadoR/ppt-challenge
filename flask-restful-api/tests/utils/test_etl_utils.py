from unittest.mock import MagicMock, patch

import pytest

from app.models import CoverageEligibility, Drug, db
from app.utils.etl_utils import (extract_eligibility_details_info,
                                 extract_expiration_date_info,
                                 extract_program_details_info,
                                 get_or_create_coverage_eligibilities,
                                 get_or_create_drugs)


@pytest.fixture
def mock_db_session_commit():
    with patch("app.utils.etl_utils.db.session.commit") as mock_commit:
        yield mock_commit


@pytest.fixture
def mock_coverage_eligibility():
    with patch("app.utils.etl_utils.CoverageEligibility") as MockCoverageEligibility:
        yield MockCoverageEligibility


@pytest.fixture
def mock_drug():
    with patch("app.utils.etl_utils.Drug") as MockDrug:
        yield MockDrug


@pytest.fixture
def mock_openai():
    with patch("app.utils.etl_utils.openai.OpenAI") as MockOpenAI:
        yield MockOpenAI


def test_extract_eligibility_details_info(app, mock_openai):
    eligibility_details = "Eligibility details text"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = (
        '("Eligibility summary", True, 18, True, "12m")'
    )
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    result = extract_eligibility_details_info(eligibility_details)

    assert result == ("Eligibility summary", True, 18, True, "12m")


def test_extract_program_details_info(app, mock_openai):
    program_details = "Program details text"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = (
        '("Program summary", 0.0, "Renewal summary")'
    )
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    result = extract_program_details_info(program_details)

    assert result == ("Program summary", 0.0, "Renewal summary")


def test_extract_expiration_date_info(app, mock_openai):
    expiration_date = "Expiration date text"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "17/12/2025"
    mock_openai.return_value.chat.completions.create.return_value = mock_response

    result = extract_expiration_date_info(expiration_date)

    assert result == "17/12/2025"
