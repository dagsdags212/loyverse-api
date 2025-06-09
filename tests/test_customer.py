import pytest
from loyverse.api import Loyverse
from loyverse.schemas import Customer


@pytest.fixture
def data():
    """Retrieve data from API"""
    return Loyverse.customers.get()


def test_customer_get(data):
    """Expecting at least one customer"""
    assert len(data) >= 1


def test_customer_ingestion(data):
    """Model must have an `id` field"""
    for d in data[:5]:
        m = Customer.model_validate(d)
        assert m.id is not None
