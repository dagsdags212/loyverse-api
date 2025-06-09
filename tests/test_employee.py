import pytest
from loyverse.api import Loyverse
from loyverse.schemas import Employee


@pytest.fixture
def data():
    """Retrieve customer data from API"""
    return Loyverse.employees.get()


def test_employee_get(data):
    """Expecting at least two employees"""
    assert len(data) >= 2


def test_employee_ingestion(data):
    """Must return at least two employees and be validated by the Employee schema"""
    for d in data:
        e = Employee.model_validate(d)
        assert isinstance(e.stores, str)
