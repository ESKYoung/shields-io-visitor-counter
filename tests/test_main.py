from main import app, get_page_hash, redirect_to_github_repository
import os
import pytest

# Import environmental variables
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")


class TestRedirectToGithubRepository:

    def test_flask_redirect_called_correctly(self, patch_flask_redirect):
        """Test flask.redirect is called in the redirect_to_github_repository function with the correct arguments."""

        # Get the / page of the app
        _ = app.test_client().get("/")

        # Assert flask.redirect is called with the correct arguments
        patch_flask_redirect.assert_called_once_with(GITHUB_REPOSITORY, code=302)

    def test_returns_correctly(self, patch_flask_redirect):
        """Test the redirect_to_github_repository function returns correctly."""

        # Get the / page of the app
        _ = app.test_client().get("/")

        # Execute the redirect_to_github_repository function
        assert redirect_to_github_repository() == patch_flask_redirect()


# Define test cases for the test_get_page_hash_returns_correctly test
args_test_get_page_hash_returns_correctly = [
    ("foo", "bar", "ff32a30c3af5012ea395827a3e99a13073c3a8d8410a708568ff7e6eb85968fccfebaea039bc21411e9d43fdb9a851b529b"
                   "9960ffea8679199781b8f45ca85e2"),
    ("bar", "foo", "b491a039c51aab2e18c4a7f38401981a078730408bd939df651668cecaf10c1145c55688b28b9f96fd9b966daf66a945131"
                   "aa59c3fed7f321f3fdfc3c47c5b9c")
]


@pytest.mark.parametrize("test_input_page, test_input_hash, test_expected", args_test_get_page_hash_returns_correctly)
def test_get_page_hash_returns_correctly(mocker, test_input_page: str, test_input_hash: str,
                                         test_expected: str) -> None:
    """Test get_page_hash returns the correct value."""

    # Patch the HASH_KEY environment variable
    _ = mocker.patch("main.HASH_KEY", test_input_hash)

    assert get_page_hash(test_input_page) == test_expected
