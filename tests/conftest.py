import json
from pathlib import Path

import pytest
from pygenezys.client import GenezysClient

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def client():
    return GenezysClient("test-token")


@pytest.fixture
def load_fixture():
    def _load(name):
        return json.loads((FIXTURES_DIR / name).read_text(encoding="utf-8"))
    return _load
