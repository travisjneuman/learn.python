"""
Tests for Project 02 — Mocking (test_project.py)

Additional mock-based tests that complement test_weather.py. These
demonstrate different mocking patterns: patching, side_effect for
exceptions, and verifying call arguments.

Why mock external dependencies?
    The WeatherService calls a fake API URL. In tests, we replace
    requests.get with a mock so no HTTP calls are made. This makes
    tests fast, reliable, and independent of network connectivity.

Run with: pytest tests/test_project.py -v
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from project import WeatherService


# ── Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture
def service():
    """Create a WeatherService instance for testing.

    WHY: Each test gets a fresh instance so state does not leak between
    tests. The API key 'test-key' makes it obvious this is a test.
    """
    return WeatherService(api_key="test-key")


# ── Test: get_temperature with mocked response ────────────────────────

@patch("project.requests.get")
def test_get_temperature_returns_temp(mock_get, service):
    """get_temperature should extract temp_c from the JSON response.

    WHY: The function navigates a nested JSON structure (data["current"]["temp_c"]).
    If the key names change or the nesting is wrong, this test catches it.

    How the mock works:
    1. @patch replaces requests.get with mock_get for the duration of this test.
    2. We configure mock_get to return a fake response with .json() returning
       our test data.
    3. The function calls requests.get (which is now mock_get) and gets our data.
    """
    # Configure the mock to return a fake response.
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "current": {"temp_c": 22.5}
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    temp = service.get_temperature("London")

    assert temp == 22.5, "Should extract temperature from response JSON"


@patch("project.requests.get")
def test_get_temperature_calls_correct_url(mock_get, service):
    """get_temperature should call the API with the correct URL and params.

    WHY: If the URL or parameters are wrong, the API would return an error
    or wrong data. Verifying the mock was called with expected arguments
    ensures the request is constructed correctly.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"current": {"temp_c": 15.0}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    service.get_temperature("Paris")

    # Verify requests.get was called with the right arguments.
    mock_get.assert_called_once()
    call_args = mock_get.call_args

    # Check the URL starts with the base URL.
    assert "current" in call_args[0][0], "URL should include /current endpoint"

    # Check the params include city and key.
    params = call_args[1]["params"]
    assert params["city"] == "Paris", "Should pass the city name"
    assert params["key"] == "test-key", "Should pass the API key"


# ── Test: get_temperature handles HTTP errors ──────────────────────────

@patch("project.requests.get")
def test_get_temperature_raises_on_http_error(mock_get, service):
    """get_temperature should propagate HTTP errors from the API.

    WHY: When the API returns a 4xx or 5xx error, raise_for_status() throws
    an HTTPError. The function should not catch it — the caller needs to
    know the request failed.
    """
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        service.get_temperature("NonexistentCity")


# ── Test: get_forecast with mocked response ───────────────────────────

@patch("project.requests.get")
def test_get_forecast_returns_list_of_days(mock_get, service):
    """get_forecast should return a list of forecast dictionaries.

    WHY: The function transforms the API response into a cleaner format.
    This test verifies the transformation extracts the right fields
    (date, high, low, condition) from the nested API structure.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "forecast": {
            "days": [
                {"date": "2024-01-01", "high_c": 12.0, "low_c": 5.0, "condition": "Sunny"},
                {"date": "2024-01-02", "high_c": 10.0, "low_c": 3.0, "condition": "Cloudy"},
            ]
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    forecast = service.get_forecast("London", days=2)

    assert len(forecast) == 2, "Should return 2 forecast days"
    assert forecast[0]["date"] == "2024-01-01"
    assert forecast[0]["high"] == 12.0, "Should map 'high_c' to 'high'"
    assert forecast[0]["low"] == 5.0, "Should map 'low_c' to 'low'"
    assert forecast[0]["condition"] == "Sunny"


@patch("project.requests.get")
def test_get_forecast_passes_days_param(mock_get, service):
    """get_forecast should pass the days parameter to the API.

    WHY: The days parameter controls how many forecast days the API returns.
    If it is not passed correctly, the API might return the wrong number
    of days.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"forecast": {"days": []}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    service.get_forecast("Berlin", days=5)

    params = mock_get.call_args[1]["params"]
    assert params["days"] == 5, "Should pass days=5 to the API"


# ── Test: connection error ─────────────────────────────────────────────

@patch("project.requests.get")
def test_get_temperature_raises_on_connection_error(mock_get, service):
    """get_temperature should propagate connection errors.

    WHY: If the network is down or the server is unreachable, requests.get
    raises a ConnectionError. The function should let this propagate so
    the caller can handle it (retry, show an error message, etc.).
    """
    mock_get.side_effect = requests.ConnectionError("Network unreachable")

    with pytest.raises(requests.ConnectionError):
        service.get_temperature("London")
