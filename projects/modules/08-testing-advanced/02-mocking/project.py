"""
Project 02 — Mocking

A WeatherService class that fetches weather data from an external API.
In real life, this would call a service like OpenWeatherMap or WeatherAPI.
For this project, we simulate the API structure so you can learn how to
mock external HTTP calls in tests.

The key insight: your code talks to requests.get(), and in tests we
replace requests.get() with a fake that returns whatever we want.
"""

import requests


# WHY a fake URL? -- Tests must never make real HTTP calls. They'd be slow,
# flaky (network failures), and non-deterministic (API data changes). By
# mocking requests.get(), we control exactly what the "API" returns, making
# tests fast, reliable, and able to simulate error scenarios on demand.
API_BASE_URL = "https://api.weather-example.com/v1"


class WeatherService:
    """
    A service that fetches weather data from an external API.

    In production, this class would be configured with an API key and
    would make real HTTP requests. In tests, we mock requests.get()
    so no real HTTP calls are made.
    """

    def __init__(self, api_key="demo-key"):
        # Store the API key for authenticating requests.
        # Every request to the weather API needs this key.
        self.api_key = api_key

    def get_temperature(self, city):
        """
        Get the current temperature for a city.

        Makes a GET request to the weather API and extracts the
        temperature from the JSON response.

        Returns the temperature as a float (in Celsius).
        Raises an exception if the API call fails.
        """
        # Build the URL with query parameters. The API expects a city
        # name and an API key.
        url = f"{API_BASE_URL}/current"
        params = {"city": city, "key": self.api_key}

        # Make the HTTP request. This is the line that gets mocked in tests.
        # In real life, this goes over the network to the API server.
        # In tests, it returns a fake response instantly.
        response = requests.get(url, params=params, timeout=10)

        # raise_for_status() throws an HTTPError if the status code
        # indicates failure (4xx or 5xx). This is better than checking
        # the status code manually because it works for all error codes.
        response.raise_for_status()

        # Parse the JSON response body into a Python dictionary.
        data = response.json()

        # Extract the temperature from the nested JSON structure.
        # A real API response might look like:
        # {"location": {"city": "London"}, "current": {"temp_c": 15.5}}
        return data["current"]["temp_c"]

    def get_forecast(self, city, days=3):
        """
        Get a multi-day weather forecast for a city.

        Returns a list of dictionaries, one per day, each containing:
        - "date": the date string
        - "high": the high temperature in Celsius
        - "low": the low temperature in Celsius
        - "condition": a text description like "Sunny" or "Rain"
        """
        url = f"{API_BASE_URL}/forecast"
        params = {"city": city, "key": self.api_key, "days": days}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # The API returns a list of forecast days. We extract just the
        # fields we care about, which also protects us if the API adds
        # new fields later — our code only reads what it needs.
        forecast = []
        for day in data["forecast"]["days"]:
            forecast.append({
                "date": day["date"],
                "high": day["high_c"],
                "low": day["low_c"],
                "condition": day["condition"],
            })

        return forecast


# ── Demo ────────────────────────────────────────────────────────────────
# This demo will fail if you actually run it (the API URL is fake).
# The point is to show how the class would be used. The real action
# happens in tests/test_weather.py, where we mock the API calls.

if __name__ == "__main__":
    print("WeatherService Demo")
    print("=" * 40)
    print()
    print("This demo would call a real API if the URL existed.")
    print("Since the URL is fake, it will raise a ConnectionError.")
    print("The real value of this project is in the tests.")
    print()
    print("Run the tests with:")
    print("  pytest tests/test_weather.py -v")
    print()

    # Uncomment the lines below to see the ConnectionError:
    # service = WeatherService()
    # temp = service.get_temperature("London")
    # print(f"London temperature: {temp}°C")
