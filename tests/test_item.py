import pytest
from loyverse.api import Loyverse
from loyverse.schemas import Item


@pytest.fixture
def data():
    """Retrieve data from API"""
    return Loyverse.items.get()


def test_item_get(data):
    assert len(data) > 0


def test_item_ingestion(data):
    """Model must have an `id` field"""
    for d in data:
        m = Item.model_validate(d)
        assert m.id is not None
