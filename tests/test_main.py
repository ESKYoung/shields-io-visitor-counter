from datetime import timedelta
from http import HTTPStatus
from flask import render_template, request
from main import (
    app,
    combine_url_and_query,
    compile_shields_io_url,
    cron_page,
    get_page_count,
    get_page_hash,
    redirect_to_github_repository,
)
from typing import Any, Dict, Union
from unittest.mock import MagicMock
from urllib.parse import SplitResult, urlsplit
import os
import pytest

# Import environmental variables
DEFAULT_SHIELDS_IO_LABEL = os.getenv("DEFAULT_SHIELDS_IO_LABEL")
DEFAULT_SHIELDS_IO_COLOR = os.getenv("DEFAULT_SHIELDS_IO_COLOR")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")
HTML_CRON = os.getenv("HTML_CRON")
URL_COUNTAPI = os.getenv("URL_COUNTAPI").rstrip("/")
URL_SHIELDS_IO = os.getenv("URL_SHIELDS_IO").rstrip("/")


class TestRedirectToGithubRepository:
    def test_flask_redirect_called_correctly(
        self,
        patch_flask_redirect: MagicMock,
    ) -> None:
        """Test ``flask.redirect`` is called correctly."""
        # Get the `/` page of the app
        _ = app.test_client().get("/")

        # Assert `flask.redirect` is called with the correct arguments
        patch_flask_redirect.assert_called_once_with(GITHUB_REPOSITORY, code=302)

    def test_returns_correctly(self, patch_flask_redirect: MagicMock) -> None:
        """Test the function returns correctly."""
        # Get the `/` page of the app
        _ = app.test_client().get("/")

        # Execute the `redirect_to_github_repository` function
        assert redirect_to_github_repository() == patch_flask_redirect()


# Define test cases for the test_get_page_hash_returns_correctly test
args_test_get_page_hash_returns_correctly = [
    (
        "foo",
        "bar",
        "ff32a30c3af5012ea395827a3e99a13073c3a8d8410a708568ff7e6eb85968fccfebaea039bc21"
        "411e9d43fdb9a851b529b9960ffea8679199781b8f45ca85e2",
    ),
    (
        "bar",
        "foo",
        "b491a039c51aab2e18c4a7f38401981a078730408bd939df651668cecaf10c1145c55688b28b9f"
        "96fd9b966daf66a945131aa59c3fed7f321f3fdfc3c47c5b9c",
    ),
]


@pytest.mark.parametrize(
    "test_input_page, test_input_hash, test_expected",
    args_test_get_page_hash_returns_correctly,
)
def test_get_page_hash_returns_correctly(
    mocker,
    test_input_page: str,
    test_input_hash: str,
    test_expected: str,
) -> None:
    """Test ``get_page_hash`` returns the correct value."""
    # Patch the `HASH_KEY` environment variable
    _ = mocker.patch("main.HASH_KEY", test_input_hash)
    assert get_page_hash(test_input_page) == test_expected


# Define test cases for the combine_url_and_query function
args_test_combine_url_and_query_returns_correctly = [
    ("http://www.google.com", "hello world", "http://www.google.com?hello world"),
    ("https://www.google.com", "hello\nworld", "https://www.google.com?hello\nworld"),
    (
        urlsplit("http://www.google.com"),
        "hello world",
        "http://www.google.com?hello world",
    ),
    (
        urlsplit("https://www.google.com"),
        "hello\nworld",
        "https://www.google.com?hello\nworld",
    ),
]


@pytest.mark.parametrize(
    "test_input_url, test_input_query, test_expected",
    args_test_combine_url_and_query_returns_correctly,
)
def test_combine_url_and_query_returns_correctly(
    test_input_url: Union[str, SplitResult],
    test_input_query: str,
    test_expected: str,
) -> None:
    """Test ``combine_url_and_query`` returns correctly."""
    assert combine_url_and_query(test_input_url, test_input_query) == test_expected


@pytest.mark.parametrize("test_input", ["foo", "bar", "user_1234"])
def test_get_page_count_calls_countapi_correctly(
    patch_requests_get: MagicMock,
    test_input: str,
) -> None:
    """Test ``get_page_count`` calls CountAPI correctly."""
    # Call the `get_page_count` function
    _ = get_page_count(test_input)

    # Assert the `requests.get` function is called once with the correct argument
    patch_requests_get.assert_called_with(f"{URL_COUNTAPI}/{test_input}")


def mock_requests_get(*args: Any) -> object:
    """Side effect function to mock the ``requests.get`` function.

    Based on this StackOverflow answer: https://stackoverflow.com/a/28507806.

    Args:
        *args: A list of arguments, where the first argument is the URL containing the
        ``URL_SHIELDS_IO`` environmental variable with an additional URL stub.

    Returns:
        The class ``MockResponse``, which has the attributes ``json_data``, and
        ``status_code``, and the method json that returns ``json_data``. If the URL
        stub is "", ``json_data`` will be ``None``, and ``status_code`` will be
        ``404``, otherwise they will be ``{"value": 100}``, and ``200``.

    """

    class MockResponse:
        def __init__(self, json_data, status_code):
            """Mock the attributes, and json method of ``requests.get function``.

            Args:
                json_data: A mock JSON return.
                status_code: A mock HTTP status code.

            """
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            """Mock the json method of the ``requests.get`` function.

            Returns:
                Returns the json_data attribute.

            """
            return self.json_data

    # Define the `MockResponse` attributes if the URL stub is whitespace or otherwise
    # empty
    if args[0].rstrip(" /") != URL_COUNTAPI:
        return MockResponse({"value": HTTPStatus.CONTINUE}, HTTPStatus.OK)
    else:
        return MockResponse(None, HTTPStatus.NOT_FOUND)


@pytest.mark.parametrize("test_input", ["foo", "bar ", "user_1234/", "/", "  ", ""])
def test_get_page_count_returns_correctly_with_working_countapi(
    patch_requests_get: MagicMock,
    test_input: str,
) -> None:
    """Test ``get_page_count`` returns the correct counts."""
    # Add a side effect to the `requests.get` function patch
    patch_requests_get.side_effect = mock_requests_get

    # Call the `get_page_count` function, and assert the returned value is correct
    if test_input.rstrip(" /"):
        assert get_page_count(test_input) == HTTPStatus.CONTINUE
    else:
        assert get_page_count(test_input) is None


def test_get_page_count_returns_correctly_with_failing_countapi(
    patch_requests_get: MagicMock,
) -> None:
    """Test ``get_page_count`` returns correctly with a failing CountAPI response."""

    # dd a side effect to the `requests.get` function patch
    patch_requests_get.side_effect = Exception()

    # Call the `get_page_count` function returns `None` if `request.get` raises an
    # exception
    assert get_page_count("test_key") is None


@pytest.mark.parametrize(
    "test_input_label, test_input_message, test_input_color, test_input_query",
    [
        ("label", "message", "color", {}),
        ("foo", "bar", "foo_bar", {"hello": "world"}),
    ],
)
def test_compile_shields_io_url_returns_correctly(
    test_input_label: str,
    test_input_message: str,
    test_input_color: str,
    test_input_query: Dict[str, Any],
) -> None:
    """Test ``compile_shields_io_url`` returns the correct string."""
    # Compile the query string, depending on if `test_input_query` is an empty
    # dictionary or not
    if test_input_query:
        compiled_query_string = "&".join(
            f"{k}={v}" for k, v in test_input_query.items()
        )
    else:
        compiled_query_string = ""

    # Generate the expected URL string
    test_expected = combine_url_and_query(
        f"{URL_SHIELDS_IO}/{test_input_label}-{test_input_message}-{test_input_color}",
        compiled_query_string,
    )

    # Assert that the actual string is the same as the expected on
    assert test_expected == compile_shields_io_url(
        test_input_label,
        test_input_message,
        test_input_color,
        **test_input_query,
    )


class TestGetShieldsIoBadge:
    @pytest.mark.parametrize("test_input_query", [{}, {"hello": "world"}])
    def test_request_args_to_dict(self, test_input_query: Dict[str, Any]) -> None:
        """Test the ``flask.request.args`` are converted into a dictionary."""
        # Assert the requests arguments when visiting the `/badge` page are correct
        with app.test_request_context(path="/badge", query_string=test_input_query):
            assert request.args.to_dict() == test_input_query

    @pytest.mark.parametrize("test_input_query", [{}, {"hello": "world"}])
    def test_request_arguments_defaults_set(
        self,
        mocker,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test default values are set if label and color not in the query string."""
        # Patch the `get_page_count`, and `compile_shields_io_url` functions
        patch_get_page_count = mocker.patch("main.get_page_count")
        patch_compile_shields_io_url = mocker.patch("main.compile_shields_io_url")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge",
            query_string={"page": "example", **test_input_query},
        )

        # Assert `compile_shields_io_url` is called with default arguments for the
        # label, and color arguments
        patch_compile_shields_io_url.assert_called_once_with(
            message=patch_get_page_count.return_value,
            label=DEFAULT_SHIELDS_IO_LABEL,
            color=DEFAULT_SHIELDS_IO_COLOR,
            **test_input_query,
        )

    @pytest.mark.parametrize(
        "test_input_message, test_input_query",
        [("foo", {"hello": "world"})],
    )
    def test_get_page_count_not_called_if_message_in_request_arguments(
        self, mocker, test_input_message: str, test_input_query: Dict[str, Any]
    ) -> None:
        """Test ``get_page_count`` not called if message is in the request arguments."""
        # Patch the `get_page_count` function
        patch_get_page_count = mocker.patch("main.get_page_count")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge",
            query_string={"message": test_input_message, **test_input_query},
        )

        # Assert `get_page_count` is not called
        patch_get_page_count.assert_not_called()

    @pytest.mark.parametrize(
        "test_input_message, test_input_query",
        [("foo", {"hello": "world"})],
    )
    def test_assertionerror_handling_if_message_in_request_arguments(
        self, mocker, test_input_message: str, test_input_query: Dict[str, Any]
    ) -> None:
        """Test error message and label returned if message is in request arguments."""
        # Patch the `get_page_count`, and `compile_shields_io_url` functions
        _ = mocker.patch("main.get_page_count")
        patch_compile_shields_io_url = mocker.patch("main.compile_shields_io_url")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge",
            query_string={"message": test_input_message, **test_input_query},
        )

        # Set the default colour if colour is not a key in `test_input_query`
        if "color" not in test_input_query.keys():
            test_input_query = {"color": DEFAULT_SHIELDS_IO_COLOR, **test_input_query}

        # Assert `compile_shields_io_url` is called with error values for the label and
        # message arguments
        patch_compile_shields_io_url.assert_called_once_with(
            message="Argument not needed: message",
            label="HTTP 400",
            **test_input_query,
        )

    @pytest.mark.parametrize(
        "test_input_page, test_input_query",
        [("foobar", {"hello": "world"})],
    )
    def test_get_page_hash_called_correctly(
        self,
        mocker,
        test_input_page: str,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test that ``get_page_hash`` is called with the correct arguments."""
        # Patch the `get_page_hash`, and `get_page_count` functions
        patch_get_page_hash = mocker.patch("main.get_page_hash")
        _ = mocker.patch("main.get_page_count")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge", query_string={"page": test_input_page, **test_input_query}
        )

        # Assert get_page_hash is called correctly
        patch_get_page_hash.assert_called_once_with(test_input_page)

    @pytest.mark.parametrize(
        "test_input_page, test_input_query",
        [("foobar", {"hello": "world"})],
    )
    def test_get_page_count_called_correctly(
        self,
        mocker,
        test_input_page: str,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test that ``get_page_count`` is called with the correct arguments."""
        # Patch the `get_page_hash`, and `get_page_count` functions
        patch_get_page_hash = mocker.patch("main.get_page_hash")
        patch_get_page_count = mocker.patch("main.get_page_count")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge",
            query_string={"page": test_input_page, **test_input_query},
        )

        # Assert `get_page_count` is called correctly
        patch_get_page_count.assert_called_once_with(
            patch_get_page_hash.return_value[:64]
        )

    @pytest.mark.parametrize("test_input_query", [{"hello": "world"}])
    def test_get_page_count_not_called_if_page_not_in_request_arguments(
        self, mocker, test_input_query: dict
    ) -> None:
        """Test ``get_page_count`` not called if page not in the request."""
        # Patch the `get_page_count` function
        patch_get_page_count = mocker.patch("main.get_page_count")

        # If page is a key in `test_input_query`, remove it
        if "page" in test_input_query.keys():
            _ = test_input_query.pop("page")

        # Get the `/badge` page of the app
        _ = app.test_client().get("/badge", query_string={**test_input_query})

        # Assert `get_page_count` is not called
        patch_get_page_count.assert_not_called()

    @pytest.mark.parametrize("test_input_query", [{"hello": "world"}])
    def test_keyerror_handling_if_page_not_in_request_arguments(
        self,
        mocker,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test error message and label are produced if page is not in request."""
        # Patch the `get_page_count`, and `compile_shields_io_url` functions
        _ = mocker.patch("main.get_page_count")
        patch_compile_shields_io_url = mocker.patch("main.compile_shields_io_url")

        # If page is a key in `test_input_query`, remove it
        if "page" in test_input_query.keys():
            _ = test_input_query.pop("page")

        # Get the `/badge` page of the app
        _ = app.test_client().get("/badge", query_string={**test_input_query})

        # Set the default colour if colour is not a key in `test_input_query`
        if "color" not in test_input_query.keys():
            test_input_query = {"color": DEFAULT_SHIELDS_IO_COLOR, **test_input_query}

        # Assert `compile_shields_io_url` is called with error values for the label and
        # message arguments
        patch_compile_shields_io_url.assert_called_once_with(
            message="Missing required argument: page",
            label="HTTP 400",
            **test_input_query,
        )

    @pytest.mark.parametrize(
        "test_input_page, test_input_query",
        [("foobar", {"hello": "world"})],
    )
    def test_assertionerror_handling_if_get_page_count_fails(
        self,
        mocker,
        test_input_page: str,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test error message and label are produced if ``get_page_count`` fails."""
        # Patch the `get_page_count`, and `compile_shields_io_url` functions
        _ = mocker.patch("main.get_page_count", return_value=None)
        patch_compile_shields_io_url = mocker.patch("main.compile_shields_io_url")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge",
            query_string={"page": test_input_page, **test_input_query},
        )

        # Set the default colour if colour is not a key in `test_input_query`
        if "color" not in test_input_query.keys():
            test_input_query = {"color": DEFAULT_SHIELDS_IO_COLOR, **test_input_query}

        # Assert `compile_shields_io_url` is called with error values for the label and
        # message arguments
        patch_compile_shields_io_url.assert_called_once_with(
            message="Error with CountAPI",
            label="HTTP 503",
            **test_input_query,
        )

    @pytest.mark.parametrize("test_input_query", [{"hello": "world"}])
    def test_exception_handling_from_get_page_hash(
        self,
        mocker,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test other exception handling by ``get_page_hash`` raises a 500 code."""

        # Patch the get_page_hash, and get_page_count functions
        _ = mocker.patch("main.get_page_hash", side_effect=Exception())
        _ = mocker.patch("main.get_page_count")

        # Set up the app test client
        client = app.test_client()

        # Get the `/badge` page of the app, and assert it returns an HTTP 500 status
        # code
        get_client = client.get(
            "/badge",
            query_string={"page": "example", **test_input_query},
        )
        assert get_client.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    @pytest.mark.parametrize("test_input_query", [{"hello": "world"}])
    def test_exception_handling_from_get_page_count(
        self,
        mocker,
        test_input_query: Dict[str, Any],
    ) -> None:
        """Test other exception handling by ``get_page_count`` raises a 500 status."""
        # Patch the `get_page_hash`, and `get_page_count` functions
        _ = mocker.patch("main.get_page_hash")
        _ = mocker.patch("main.get_page_count", side_effect=Exception())

        # Set up the app test client
        client = app.test_client()

        # Get the `/badge` page of the app, and assert it returns an HTTP 500 status
        # code
        get_client = client.get(
            "/badge",
            query_string={"page": "example", **test_input_query},
        )
        assert get_client.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    @pytest.mark.parametrize(
        "test_input_page, test_input_label, test_input_color, test_input_query",
        [("foo", "bar", "foobar", {"hello": "world"})],
    )
    def test_compile_shields_io_url_called_correctly(
        self,
        mocker,
        test_input_page: str,
        test_input_label: str,
        test_input_color: str,
        test_input_query: dict,
    ) -> None:
        """Test compile_shields_io_url is called correctly."""
        # Patch the `get_page_hash`, `get_page_count`, and `compile_shields_io_url`
        # functions
        _ = mocker.patch("main.get_page_hash")
        patch_get_page_count = mocker.patch("main.get_page_count")
        patch_compile_shields_io_url = mocker.patch("main.compile_shields_io_url")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge",
            query_string={
                "page": test_input_page,
                "label": test_input_label,
                "color": test_input_color,
                **test_input_query,
            },
        )

        # Assert `compile_shields_io_url` is called with the correct arguments
        patch_compile_shields_io_url.assert_called_once_with(
            message=patch_get_page_count.return_value,
            label=test_input_label,
            color=test_input_color,
            **test_input_query,
        )

    @pytest.mark.parametrize(
        "test_input_page, test_input_query",
        [("foo", {"hello": "world"})],
    )
    def test_requests_get_is_called_correctly(
        self, mocker, test_input_page: str, test_input_query: dict
    ) -> None:
        """Test ``requests.get`` function is called correctly."""
        # Patch the `get_page_count`, `compile_shields_io_url`, and `requests.get`
        # functions
        _ = mocker.patch("main.get_page_count")
        patch_compile_shields_io_url = mocker.patch("main.compile_shields_io_url")
        patch_requests_get = mocker.patch("requests.get")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge", query_string={"page": test_input_page, **test_input_query}
        )

        # Assert `requests.get` is called with the correct arguments
        patch_requests_get.assert_called_once_with(
            patch_compile_shields_io_url.return_value
        )

    @pytest.mark.parametrize(
        "test_input_page, test_input_query",
        [("foo", {"hello": "world"})],
    )
    def test_flask_response_is_called_correctly(
        self, mocker, test_input_page: str, test_input_query: dict
    ) -> None:
        """Test ``flask.Response`` class is called correctly."""
        # Patch the `get_page_count`, and `requests.get` functions, and the
        # `flask.Response` class
        _ = mocker.patch("main.get_page_count")
        patch_requests_get = mocker.patch("requests.get")
        patch_datetime = mocker.patch("main.datetime")
        patch_flask_response = mocker.patch("main.Response")

        # Get the `/badge` page of the app
        _ = app.test_client().get(
            "/badge", query_string={"page": test_input_page, **test_input_query}
        )

        # Define the mock expiry time
        mock_expiry_time = patch_datetime.utcnow.return_value - timedelta(minutes=10)

        # Assert `flask.Response` is called with the correct arguments
        patch_flask_response.assert_called_once_with(
            response=patch_requests_get.return_value,
            content_type="image/svg+xml",
            headers={
                "Cache-Control": "no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate",
                "Expires": mock_expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            },
        )


class TestCronPage:
    def test_returns_correct_status_code(self) -> None:
        """Test the `cron_page` function returns correctly."""
        with app.test_request_context(path="/cron"):
            assert cron_page() == render_template(HTML_CRON)

    def test_returns_correctly(self) -> None:
        """Test calling the `/cron` slug returns correctly."""

        # Set up the app test client
        client = app.test_client()

        # Get the `/cron` page of the app, and assert returns an HTTP 200 status code
        assert client.get("/cron").status_code == HTTPStatus.OK
