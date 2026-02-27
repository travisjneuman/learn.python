"""Tests for Module 03 / Project 06 — Weather API Dashboard.

All tests mock the network layer with unittest.mock.patch so no real HTTP
requests are made. This keeps tests fast, deterministic, and runnable
offline.

WHY mock?
- Real API calls are slow, flaky, and depend on network access.
- Mocking lets us simulate every scenario: success, errors, bad data.
- We test OUR code, not the Open-Meteo server.
"""

import sys
import os
from unittest.mock import patch, MagicMock

import requests as real_requests
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from project import (
    parse_arguments,
    fetch_weather,
    describe_weather_code,
    format_dashboard,
    main,
    CITY_PRESETS,
)


# ---------------------------------------------------------------------------
# Tests for parse_arguments()
# ---------------------------------------------------------------------------

def test_parse_city_preset():
    """parse_arguments() should resolve a known city name to coordinates."""
    lat, lon = parse_arguments(["new-york"])

    assert lat == pytest.approx(40.7128)
    assert lon == pytest.approx(-74.0060)


def test_parse_city_preset_case_insensitive():
    """City names should be case-insensitive."""
    lat, lon = parse_arguments(["TOKYO"])

    assert lat == pytest.approx(35.6762)
    assert lon == pytest.approx(139.6503)


def test_parse_raw_coordinates():
    """parse_arguments() should accept two numeric strings as lat/lon."""
    lat, lon = parse_arguments(["51.5", "-0.13"])

    assert lat == pytest.approx(51.5)
    assert lon == pytest.approx(-0.13)


def test_parse_unknown_city_raises():
    """parse_arguments() should raise ValueError for unknown city names."""
    with pytest.raises(ValueError, match="Unknown city"):
        parse_arguments(["atlantis"])


def test_parse_invalid_coordinates_raises():
    """parse_arguments() should raise ValueError for non-numeric coordinates."""
    with pytest.raises(ValueError, match="Coordinates must be numbers"):
        parse_arguments(["abc", "def"])


def test_parse_latitude_out_of_range():
    """parse_arguments() should reject latitude outside -90 to 90."""
    with pytest.raises(ValueError, match="Latitude must be between"):
        parse_arguments(["100", "50"])


def test_parse_longitude_out_of_range():
    """parse_arguments() should reject longitude outside -180 to 180."""
    with pytest.raises(ValueError, match="Longitude must be between"):
        parse_arguments(["50", "200"])


def test_parse_no_args_raises():
    """parse_arguments() should raise ValueError when given no arguments."""
    with pytest.raises(ValueError, match="Usage"):
        parse_arguments([])


def test_parse_three_args_raises():
    """parse_arguments() should raise ValueError when given three arguments."""
    with pytest.raises(ValueError, match="Usage"):
        parse_arguments(["1", "2", "3"])


# ---------------------------------------------------------------------------
# Tests for describe_weather_code()
# ---------------------------------------------------------------------------

def test_describe_known_code():
    """describe_weather_code() should return the description for known codes."""
    assert describe_weather_code(0) == "Clear sky"
    assert describe_weather_code(63) == "Moderate rain"
    assert describe_weather_code(95) == "Thunderstorm"


def test_describe_unknown_code():
    """describe_weather_code() should return a fallback string for unknown codes."""
    result = describe_weather_code(999)

    assert "Unknown" in result
    assert "999" in result


# ---------------------------------------------------------------------------
# Tests for fetch_weather() — mocked HTTP
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_fetch_weather_success(mock_get):
    """fetch_weather() should return parsed JSON on a successful response."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "latitude": 40.71,
        "longitude": -74.01,
        "timezone": "America/New_York",
        "current": {
            "time": "2025-01-15T14:00",
            "temperature_2m": 3.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.3,
            "weather_code": 2,
        },
        "current_units": {
            "temperature_2m": "\u00b0C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
        },
    }
    fake_response.raise_for_status = MagicMock()
    mock_get.return_value = fake_response

    data = fetch_weather(40.7128, -74.0060)

    assert data["current"]["temperature_2m"] == 3.5
    assert data["current"]["relative_humidity_2m"] == 65
    assert data["current"]["wind_speed_10m"] == 12.3

    # Verify the correct URL and params were used.
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert call_args[0][0] == "https://api.open-meteo.com/v1/forecast"
    assert call_args[1]["params"]["latitude"] == 40.7128
    assert call_args[1]["params"]["longitude"] == -74.0060


@patch("project.requests.get")
def test_fetch_weather_http_error(mock_get):
    """fetch_weather() should propagate HTTPError when the API returns 4xx/5xx."""
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = real_requests.exceptions.HTTPError(
        "400 Bad Request"
    )
    mock_get.return_value = fake_response

    with pytest.raises(real_requests.exceptions.HTTPError):
        fetch_weather(999, 999)


@patch("project.requests.get")
def test_fetch_weather_connection_error(mock_get):
    """fetch_weather() should propagate ConnectionError on network failure."""
    mock_get.side_effect = real_requests.exceptions.ConnectionError("no network")

    with pytest.raises(real_requests.exceptions.ConnectionError):
        fetch_weather(40.71, -74.01)


@patch("project.requests.get")
def test_fetch_weather_timeout(mock_get):
    """fetch_weather() should propagate Timeout when the request is too slow."""
    mock_get.side_effect = real_requests.exceptions.Timeout("timed out")

    with pytest.raises(real_requests.exceptions.Timeout):
        fetch_weather(40.71, -74.01)


# ---------------------------------------------------------------------------
# Tests for format_dashboard()
# ---------------------------------------------------------------------------

def test_format_dashboard_contains_weather_info():
    """format_dashboard() should include temperature, humidity, and wind."""
    data = {
        "latitude": 40.71,
        "longitude": -74.01,
        "timezone": "America/New_York",
        "current": {
            "time": "2025-01-15T14:00",
            "temperature_2m": 3.5,
            "relative_humidity_2m": 65,
            "wind_speed_10m": 12.3,
            "weather_code": 0,
        },
        "current_units": {
            "temperature_2m": "\u00b0C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
        },
    }

    output = format_dashboard(data)

    assert "3.5" in output
    assert "65" in output
    assert "12.3" in output
    assert "Clear sky" in output
    assert "WEATHER DASHBOARD" in output
    assert "America/New_York" in output


def test_format_dashboard_handles_missing_fields():
    """format_dashboard() should not crash when optional fields are missing."""
    data = {
        "latitude": 0,
        "longitude": 0,
        "timezone": "UTC",
        "current": {},
        "current_units": {},
    }

    output = format_dashboard(data)

    # Should show "N/A" for missing values instead of crashing.
    assert "N/A" in output


# ---------------------------------------------------------------------------
# Tests for main() — full integration with mocked HTTP
# ---------------------------------------------------------------------------

@patch("project.requests.get")
def test_main_with_city_preset(mock_get, capsys):
    """main() should fetch and display weather for a known city preset."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "latitude": 35.68,
        "longitude": 139.65,
        "timezone": "Asia/Tokyo",
        "current": {
            "time": "2025-06-01T12:00",
            "temperature_2m": 28.0,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 8.5,
            "weather_code": 1,
        },
        "current_units": {
            "temperature_2m": "\u00b0C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
        },
    }
    fake_response.raise_for_status = MagicMock()
    mock_get.return_value = fake_response

    exit_code = main(["tokyo"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "28.0" in captured.out
    assert "WEATHER DASHBOARD" in captured.out


@patch("project.requests.get")
def test_main_with_coordinates(mock_get, capsys):
    """main() should accept raw lat/lon coordinates."""
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "latitude": 51.51,
        "longitude": -0.13,
        "timezone": "Europe/London",
        "current": {
            "time": "2025-03-10T09:00",
            "temperature_2m": 10.2,
            "relative_humidity_2m": 80,
            "wind_speed_10m": 15.0,
            "weather_code": 3,
        },
        "current_units": {
            "temperature_2m": "\u00b0C",
            "relative_humidity_2m": "%",
            "wind_speed_10m": "km/h",
        },
    }
    fake_response.raise_for_status = MagicMock()
    mock_get.return_value = fake_response

    exit_code = main(["51.51", "-0.13"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "10.2" in captured.out
    assert "Overcast" in captured.out


def test_main_no_args_shows_usage(capsys):
    """main() with no arguments should show usage and return 1."""
    exit_code = main([])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage" in captured.out
    assert "city presets" in captured.out.lower()


def test_main_bad_city_shows_error(capsys):
    """main() with an unknown city should print an error and return 1."""
    exit_code = main(["atlantis"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error" in captured.out
    assert "Unknown city" in captured.out


@patch("project.requests.get")
def test_main_connection_error(mock_get, capsys):
    """main() should print a friendly message on connection failure."""
    mock_get.side_effect = real_requests.exceptions.ConnectionError("no network")

    exit_code = main(["london"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Could not connect" in captured.out


@patch("project.requests.get")
def test_main_timeout_error(mock_get, capsys):
    """main() should print a friendly message when the request times out."""
    mock_get.side_effect = real_requests.exceptions.Timeout("timed out")

    exit_code = main(["paris"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "timed out" in captured.out.lower()
