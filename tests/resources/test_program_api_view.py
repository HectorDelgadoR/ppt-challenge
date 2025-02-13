import pytest

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


def test_get_program_by_id(client, init_database):
    response = client.get("/api/programs/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["program_name"] == "Test Program"
    assert data["program_type"] == "Coupon"


def test_get_program_by_id_not_found(client):
    response = client.get("/api/programs/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "Program with ID 999 not found"
