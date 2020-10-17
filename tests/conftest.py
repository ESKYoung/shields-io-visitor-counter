import pytest


@pytest.fixture
def patch_flask_redirect(mocker):
    """Patch the flask.redirect function that has been imported in main.py."""
    return mocker.patch("main.redirect")


@pytest.fixture(scope="session")
def patch_requests_get(session_mocker):
    """Patch the request.get function"""
    return session_mocker.patch("requests.get")
