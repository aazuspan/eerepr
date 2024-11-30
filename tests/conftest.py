from pathlib import Path

import ee
import pytest

import eerepr


def pytest_sessionstart(session):
    ee.Initialize()


@pytest.fixture(autouse=True)
def reset_eerepr():
    """Reset eerepr after each test to avoid inconsistent state."""
    yield
    eerepr.reset()


@pytest.fixture(scope="session")
def original_datadir():
    """Set the pytest-regressions directory."""
    return Path(__file__).parent / "data"
