import ee


def pytest_sessionstart(session):
    ee.Initialize()
