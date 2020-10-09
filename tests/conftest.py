import pytest


@pytest.fixture
def patch_flask_redirect(mocker):
    """Patch the flask.redirect function that has been imported in main.py."""
    return mocker.patch("main.redirect")
