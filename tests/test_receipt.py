import pytest
from loyverse.api import Loyverse
from loyverse.schemas import Receipt


@pytest.fixture
def data():
    """Retrieve data from API"""
    return Loyverse.receipts.most_recent(5).get("receipts")


def test_receipt_get(data):
    assert len(data) > 0


def test_receipt_ingestion(data):
    """Model must have an `id` field"""
    for d in data:
        # print(d)
        m = Receipt.model_validate(d)
        assert m.id is not None
