import pytest
from loyverse.api import Loyverse
from loyverse.schemas import Variant


@pytest.fixture
def data():
    return Loyverse.variants.get()


def test_variant_get(data):
    assert len(data) > 0


def test_variant_ingestion(data):
    for d in data[:5]:
        m = Variant.model_validate(d)
        assert m.variant_id is not None
