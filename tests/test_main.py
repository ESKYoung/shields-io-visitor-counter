from main import app, redirect_to_github_repository
import os

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
        assert patch_flask_redirect() == redirect_to_github_repository()
