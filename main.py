from flask import Flask, redirect
import os
import werkzeug

# Import environmental variables
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

# Initialise the flask app
app = Flask(__name__)


@app.route("/")
def redirect_to_github_repository() -> werkzeug.wrappers.Response:
    """Redirect application to the GitHub repository.

    Returns:
        A werkzeug.wrappers.Response object redirecting the user to the GitHub repository.

    """
    return redirect(GITHUB_REPOSITORY, code=302)


if __name__ == '__main__':
    app.run()
