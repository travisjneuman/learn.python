"""
Tests for Project 02 — Mocking

These tests demonstrate how to use unittest.mock to replace external
dependencies (in this case, requests.get) with fake versions that
return controlled data.

Key concepts:
- @patch replaces a function/method for the duration of one test
- MagicMock creates objects that accept any attribute or method call
- return_value controls what the mock returns
- side_effect can raise exceptions or return different values per call

IMPORTANT: We patch "project.requests.get", not "requests.get".
This is because our code imports requests at the top of project.py,
so by the time our test runs, project.py has its own reference to
requests.get. We need to replace THAT reference, not the original.

Run with: pytest tests/test_weather.py -v
"""

from unittest.mock import patch, MagicMock
import pytest
import requests

from project import WeatherService


# ── Helpers ─────────────────────────────────────────────────────────────
# These helper functions create fake response objects that mimic what
# requests.get() would return. This keeps our tests clean and readable.

def make_mock_response(json_data, status_code=200):
    """
    Create a fake response object that behaves like requests.Response.

    MagicMock() creates an object that accepts any attribute access or
    method call without raising an error. We configure it to return
    specific values for .json(), .status_code, and .raise_for_status().
    """
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.json.return_value = json_data

    # raise_for_status() should do nothing for success codes (2xx)
    # and raise an HTTPError for error codes (4xx, 5xx).
    if status_code >= 400:
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            f"{status_code} Error"
        )

    return mock_response


# ── get_temperature tests ───────────────────────────────────────────────

# WHY: This is the happy path — the API returns valid data and we extract
# the temperature correctly. Every feature needs a "does it work at all?" test.

@patch("project.requests.get")
def test_get_temperature_success(mock_get):
    """Test that we correctly extract temperature from a successful API response."""
    # Set up the mock to return a fake response with known data.
    # When our code calls requests.get(), it will get this fake response.
    mock_get.return_value = make_mock_response({
        "current": {"temp_c": 15.5, "humidity": 72}
    })

    service = WeatherService(api_key="test-key")
    temp = service.get_temperature("London")

    # Verify we got the right temperature back.
    assert temp == 15.5

    # Verify that requests.get was called exactly once.
    # This catches bugs where the code accidentally makes multiple requests.
    mock_get.assert_called_once()


# WHY: APIs return error codes when something goes wrong (city not found,
# server error, etc.). Our code must handle these gracefully.

@patch("project.requests.get")
def test_get_temperature_city_not_found(mock_get):
    """Test that a 404 response raises an HTTPError."""
    mock_get.return_value = make_mock_response(
        {"error": "City not found"}, status_code=404
    )

    service = WeatherService()

    # pytest.raises checks that the code inside the block raises the
    # expected exception. If it does not raise, the test fails.
    with pytest.raises(requests.exceptions.HTTPError):
        service.get_temperature("FakeCity")


# WHY: Server errors (500) can happen at any time. We need to verify
# our code does not silently swallow these.

@patch("project.requests.get")
def test_get_temperature_api_error(mock_get):
    """Test that a 500 server error raises an HTTPError."""
    mock_get.return_value = make_mock_response(
        {"error": "Internal server error"}, status_code=500
    )

    service = WeatherService()

    with pytest.raises(requests.exceptions.HTTPError):
        service.get_temperature("London")


# WHY: Network timeouts are a common failure mode. side_effect lets us
# simulate exceptions that requests.get itself would raise (not HTTP errors,
# but actual network failures).

@patch("project.requests.get")
def test_get_temperature_timeout(mock_get):
    """Test that a network timeout is properly raised."""
    # side_effect makes the mock raise an exception instead of returning
    # a value. This simulates what happens when the network is slow or down.
    mock_get.side_effect = requests.exceptions.Timeout("Connection timed out")

    service = WeatherService()

    with pytest.raises(requests.exceptions.Timeout):
        service.get_temperature("London")


# WHY: We want to make sure the service works for different cities,
# not just "London". This also verifies the city parameter is being
# passed through to the API call correctly.

@patch("project.requests.get")
def test_get_temperature_different_cities(mock_get):
    """Test that the city name is passed correctly to the API."""
    mock_get.return_value = make_mock_response({
        "current": {"temp_c": 28.0}
    })

    service = WeatherService(api_key="test-key")
    temp = service.get_temperature("Tokyo")

    assert temp == 28.0

    # Check that the URL and parameters were correct.
    # call_args gives us the positional and keyword arguments from the
    # most recent call to the mock.
    call_args = mock_get.call_args
    assert call_args.kwargs["params"]["city"] == "Tokyo"
    assert call_args.kwargs["params"]["key"] == "test-key"


# ── get_forecast tests ──────────────────────────────────────────────────

# WHY: The forecast method returns structured data (a list of dicts).
# We need to verify the structure is correct, not just that it does not crash.

@patch("project.requests.get")
def test_get_forecast_success(mock_get):
    """Test that forecast data is correctly extracted and structured."""
    # This fake response mimics the structure a real weather API would return.
    mock_get.return_value = make_mock_response({
        "forecast": {
            "days": [
                {
                    "date": "2025-01-15",
                    "high_c": 8.0,
                    "low_c": 2.0,
                    "condition": "Cloudy",
                },
                {
                    "date": "2025-01-16",
                    "high_c": 10.0,
                    "low_c": 4.0,
                    "condition": "Sunny",
                },
                {
                    "date": "2025-01-17",
                    "high_c": 6.0,
                    "low_c": 1.0,
                    "condition": "Rain",
                },
            ]
        }
    })

    service = WeatherService()
    forecast = service.get_forecast("London", days=3)

    # Verify the structure and content of the returned data.
    assert len(forecast) == 3
    assert forecast[0]["date"] == "2025-01-15"
    assert forecast[0]["high"] == 8.0
    assert forecast[0]["condition"] == "Cloudy"
    assert forecast[2]["condition"] == "Rain"


# WHY: The days parameter should control how many days of forecast we get.
# We want to make sure the parameter is actually being passed to the API.

@patch("project.requests.get")
def test_get_forecast_returns_correct_days(mock_get):
    """Test that the days parameter is passed to the API."""
    mock_get.return_value = make_mock_response({
        "forecast": {
            "days": [
                {"date": "2025-01-15", "high_c": 8.0, "low_c": 2.0, "condition": "Sunny"},
            ]
        }
    })

    service = WeatherService(api_key="test-key")
    service.get_forecast("Paris", days=1)

    # Verify the days parameter was passed correctly to the API.
    call_args = mock_get.call_args
    assert call_args.kwargs["params"]["days"] == 1
    assert call_args.kwargs["params"]["city"] == "Paris"
