from flask import Flask, redirect
from typing import Dict, Optional
from urllib.parse import urljoin
import hashlib
import os
import requests
import werkzeug

# Import environmental variables
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
HASH_KEY = os.getenv("HASH_KEY")
URL_COUNTAPI = os.getenv("URL_COUNTAPI")
URL_SHIELDS_IO = os.getenv("URL_SHIELDS_IO")

# Initialise the flask app
app = Flask(__name__)


@app.route("/")
def redirect_to_github_repository() -> werkzeug.wrappers.Response:
    """Redirect application to the GitHub repository.

    Returns:
        A werkzeug.wrappers.Response object redirecting the user to the GitHub repository.

    """
    return redirect(GITHUB_REPOSITORY, code=302)


def get_page_hash(page: str) -> str:
    """Get a SHA3-512 hashed version of page.

    Args:
        page: A string giving the name of the page.

    Returns:
        A SHA3-512 hashed version of the string combined with the HASH_KEY environmental variable.

    """

    # Instantiate a SHA3-512 object
    obj_hash = hashlib.sha3_512()

    # Hash the page, and update with HASH_KEY
    obj_hash.update(page.encode("utf-8"))
    obj_hash.update(HASH_KEY.encode("utf-8"))

    # Return the hashed key
    return obj_hash.hexdigest()


def get_page_count(key: str) -> Optional[int]:
    """Get the page count using a CountAPI.

    Args:
        key: A string as a unique key for the URL_COUNTER CountAPI URL.

    Returns:
        An integer count if CountAPI is called correctly, otherwise None.

    """

    try:

        # Get the count from CountAPI
        countapi_response = requests.get(urljoin(URL_COUNTAPI, key))

        # Check a correct return is supplied
        if countapi_response and countapi_response.status_code == 200:
            return countapi_response.json()["value"]
        else:
            return None

    except Exception:
        return None


def compile_shields_io_url(label: str, message: str, color: str, **kwargs: Dict[str, str]) -> str:
    """Create a Shields.IO API URL to generate a static badge.

    Args:
        label: A string for the label of the shield.
        message: A string for the message of the shield.
        color: A hex color string for the message background.
        **kwargs: Any optional keyword arguments, where the key-value pairs are acceptable as Shields.IO parameters
          for a static badge - see https://shields.io/#styles for further information.

    Returns:
        A Shields.IO API URL string to generate a static badge.

    """

    # If query is not empty, compile the query strings together. For a single query return '?<<<query>>>',
    # for multiple query strings return '?' followed by each string delimited by &. If query is empty, return a blank
    # string
    compiled_query_string = "?{}".format("&".join(f"{k}={v}" for k, v in kwargs.items())) if kwargs else ""

    # Return the compiled Shields.IO URL string
    return urljoin(URL_SHIELDS_IO, f"{label}-{message}-{color}{compiled_query_string}")


if __name__ == '__main__':
    app.run()
