import hashlib
import os
from datetime import datetime, timedelta
from typing import Any, Tuple, Union
from urllib.parse import SplitResult, urlsplit, urlunsplit

import requests
import werkzeug
from flask import Flask, Response, redirect, render_template, request

# Import environmental variables
DEFAULT_SHIELDS_IO_LABEL = os.environ["DEFAULT_SHIELDS_IO_LABEL"]
DEFAULT_SHIELDS_IO_COLOR = os.environ["DEFAULT_SHIELDS_IO_COLOR"]
GITHUB_REPOSITORY = os.environ["GITHUB_REPOSITORY"]
HASH_KEY = os.environ["HASH_KEY"]
HTML_CRON = os.environ["HTML_CRON"]
URL_COUNTAPI = os.environ["URL_COUNTAPI"].rstrip("/")
URL_SHIELDS_IO = os.environ["URL_SHIELDS_IO"].rstrip("/")

# Initialise the flask app
app = Flask(__name__)


@app.route("/")
def redirect_to_github_repository() -> werkzeug.wrappers.Response:
    """Redirect application to the GitHub repository.

    Returns:
        A ``werkzeug.wrappers.Response`` object redirecting the user to the GitHub
        repository.

    """
    return redirect(GITHUB_REPOSITORY, code=302)


def get_page_hash(page: str) -> str:
    """Get a SHA3-512 hashed version of page.

    Args:
        page (str): A string giving the name of the page.

    Returns:
        A SHA3-512 hashed version of the string combined with the ``HASH_KEY``
        environmental variable.

    """

    # Instantiate a SHA3-512 object
    obj_hash = hashlib.sha3_512()

    # Hash the page, and update with HASH_KEY
    obj_hash.update(page.encode("utf-8"))
    obj_hash.update(HASH_KEY.encode("utf-8"))

    # Return the hashed key
    return obj_hash.hexdigest()


def combine_url_and_query(url: Union[str, SplitResult], query: str) -> str:
    """Combine ``ParseResult`` object with a query, quoting any part of the query."""

    # Get the URL components, if it is a string
    url_components = url if isinstance(url, SplitResult) else urlsplit(url)

    # Set the query to the url query attribute, and return the url as a complete string
    return urlunsplit(url_components._replace(query=query))


def get_page_count(key: str) -> Any:
    """Get the page count using a CountAPI.

    Args:
        key (str): A string as a unique key for the URL_COUNTER CountAPI URL.

    Returns:
        An integer count if CountAPI is called correctly, otherwise None.

    """
    try:
        # Get the count from CountAPI
        countapi_response = requests.get(f"{URL_COUNTAPI}/{key}")

        # Check a correct return is supplied
        if countapi_response and countapi_response.status_code == 200:
            return countapi_response.json()["value"]
        else:
            return None

    except Exception:
        return None


def compile_shields_io_url(
    label: str,
    message: str,
    color: str,
    **kwargs: Any,
) -> str:
    """Create a Shields.IO API URL to generate a static badge.

    Args:
        label (str): A string for the label of the shield.
        message (str): A string for the message of the shield.
        color (str): A hex color string for the message background.
        **kwargs (Any): Any optional keyword arguments, where the key-value pairs are
            acceptable as Shields.IO parameters for a static badge - see
            https://shields.io/#styles for further information.

    Returns:
        A Shields.IO API URL string to generate a static badge.

    """

    # If query is not empty, compile the query strings together. For a single query
    # return '?<<<query>>>', for multiple query strings return '?' followed by each
    # string delimited by &. If query is empty, return a blank string
    compiled_query_string = (
        "&".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
    )

    # Return the compiled Shields.IO URL string
    return combine_url_and_query(
        f"{URL_SHIELDS_IO}/{label}-{message}-{color}", compiled_query_string
    )


@app.route("/badge")
def get_shields_io_badge() -> Union[Response, Tuple[str, int]]:
    """Create Shields.IO static badge with visit count, based on request arguments.

    Returns:
        A Shields.IO static badge with a visit count, based on request arguments.

    """

    # Get all the request arguments as a dictionary
    request_arguments = request.args.to_dict()

    # Set default keys
    for k, d in zip(
        ["label", "color"], [DEFAULT_SHIELDS_IO_LABEL, DEFAULT_SHIELDS_IO_COLOR]
    ):
        _ = request_arguments.setdefault(k, d)

    try:
        # Check that the user hasn't entered a message argument
        assert "message" not in request_arguments.keys()

        # Get the page hash
        page_hash = get_page_hash(request_arguments.pop("page"))

        # Get the page count from CountAPI, and assert it is not empty
        page_count = get_page_count(page_hash[:64])
        message = "" if page_count is None else str(page_count)
        assert message

    except KeyError:
        # Modify the label and message to inform the user that the page argument is
        # missing
        request_arguments["label"] = "HTTP 400"
        message = "Missing required argument: page"

    except AssertionError:
        # Modify the label and message to inform the user that they either don't need
        # the message parameter, or there is an error with CountAPI
        if "message" in request_arguments.keys():
            _ = request_arguments.pop("message", None)
            request_arguments["label"] = "HTTP 400"
            message = "Argument not needed: message"
        else:
            request_arguments["label"] = "HTTP 503"
            message = "Error with CountAPI"

    except Exception as e:
        # Raise the error
        raise e

    # Get the Shields.IO badge
    svg = requests.get(compile_shields_io_url(message=message, **request_arguments))

    # Set the expiry time, and create a response header
    expiry_time = datetime.utcnow() - timedelta(minutes=10)
    headers = {
        "Cache-Control": "no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate",
        "Expires": expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }

    # Return the badge to the user
    return Response(response=svg, content_type="image/svg+xml", headers=headers)


@app.route("/cron")
def cron_page() -> Any:
    """Add a page for cron jobs to wake up the application.

    Returns:
        A HTML viewed by the cron job once it successfully wakes the application.

    """
    return render_template(HTML_CRON)


if __name__ == "__main__":
    app.run()
