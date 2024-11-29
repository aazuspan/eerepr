from pathlib import Path

import ee
import pytest


def pytest_sessionstart(session):
    ee.Initialize()


@pytest.fixture(scope="session")
def original_datadir():
    """Set the pytest-regressions directory."""
    return Path(__file__).parent / "data"
