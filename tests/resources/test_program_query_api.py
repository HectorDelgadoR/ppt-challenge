import pytest
from app.models import Program, CoverageEligibility, db

@pytest.fixture(scope='module')
def init_database(app):
    # Create test data
    coverage1 = CoverageEligibility(eligibility="Eligibility1")
    coverage2 = CoverageEligibility(eligibility="Eligibility2")
    program1 = Program(
        id=1,
        program_name="Program1",
        program_type="Type1",
        coverage_eligibilities=[coverage1]
    )
    program2 = Program(
        id=2,
        program_name="Program2",
        program_type="Type2",
        coverage_eligibilities=[coverage2]
    )
    program3 = Program(
        id=3,
        program_name="Program3",
        program_type="Type1",
        coverage_eligibilities=[coverage1, coverage2]
    )
    db.session.add_all([coverage1, coverage2, program1, program2, program3])
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()

def test_query_by_program_type(client, init_database):
    response = client.get('/api/programs?program_type=Type1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['program_name'] == "Program1"
    assert data[1]['program_name'] == "Program3"

def test_query_by_coverage_eligibilities(client, init_database):
    response = client.get('/api/programs?coverage_eligibilities=Eligibility1')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['program_name'] == "Program1"
    assert data[1]['program_name'] == "Program3"

def test_query_by_program_type_and_coverage_eligibilities(client, init_database):
    response = client.get('/api/programs?program_type=Type1&coverage_eligibilities=Eligibility2')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['program_name'] == "Program3"

def test_query_no_results(client, init_database):
    response = client.get('/api/programs?program_type=Type3')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0