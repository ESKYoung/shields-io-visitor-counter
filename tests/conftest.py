import os

import pytest
from pytest_mock import MockerFixture


def pytest_sessionstart(session: pytest.Session) -> None:
    """Set environment variables on start of the pytest session."""
    os.environ["HASH_KEY"] = "pytest"


@pytest.fixture
def patch_flask_redirect(mocker: MockerFixture) -> MockerFixture:
    """Patch the ``flask.redirect`` function that has been imported in main.py."""
    return mocker.patch("main.redirect")


@pytest.fixture(scope="session")
def patch_requests_get(session_mocker: MockerFixture) -> MockerFixture:
    """Patch the ``request.get`` function."""
    return session_mocker.patch("requests.get")
