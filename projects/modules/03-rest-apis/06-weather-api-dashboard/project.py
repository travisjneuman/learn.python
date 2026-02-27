"""Module 03 / Project 06 — Weather API Dashboard.

Fetch real weather data from the Open-Meteo API and display a formatted
dashboard in the terminal. Accepts coordinates as command-line arguments,
parses JSON for temperature, humidity, and wind speed, and handles
network errors gracefully.

Open-Meteo is free and requires no API key — perfect for learning.
"""

import sys
import json
import requests


# WHY a dictionary of presets? -- Typing raw coordinates every time is
# tedious. Named presets let users say "new-york" instead of remembering
# "40.7128,-74.0060". The dict maps friendly names to (lat, lon) tuples.
CITY_PRESETS = {
    "new-york": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "sydney": (-33.8688, 151.2093),
    "paris": (48.8566, 2.3522),
    "cairo": (30.0444, 31.2357),
    "sao-paulo": (-23.5505, -46.6333),
    "mumbai": (19.0760, 72.8777),
}


def parse_arguments(args):
    """Parse command-line arguments into latitude and longitude.

    Accepts either a city preset name or a pair of numbers (lat, lon).
    Returns a tuple of (latitude, longitude) as floats.
    Raises ValueError if the arguments cannot be parsed.
    """
    if len(args) == 1:
        # Single argument: try as a city preset name.
        city = args[0].lower().strip()
        if city in CITY_PRESETS:
            return CITY_PRESETS[city]
        raise ValueError(
            "Unknown city '{}'. Available presets: {}".format(
                city, ", ".join(sorted(CITY_PRESETS.keys()))
            )
        )

    if len(args) == 2:
        # Two arguments: treat as latitude and longitude.
        try:
            lat = float(args[0])
            lon = float(args[1])
        except ValueError:
            raise ValueError(
                "Coordinates must be numbers. Got: '{}', '{}'".format(
                    args[0], args[1]
                )
            )

        # WHY validate ranges? -- Latitude is -90 to 90, longitude is
        # -180 to 180. Values outside these ranges are not valid locations
        # on Earth and the API would return an error anyway.
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90. Got: {}".format(lat))
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180. Got: {}".format(lon))

        return (lat, lon)

    raise ValueError(
        "Usage: python project.py <city-name>  OR  python project.py <lat> <lon>\n"
        "Examples:\n"
        "  python project.py new-york\n"
        "  python project.py 40.7128 -74.0060"
    )


def fetch_weather(latitude, longitude):
    """Fetch current weather data from the Open-Meteo API.

    Sends a GET request with query parameters for the desired weather
    variables. Returns the parsed JSON response as a dictionary.
    Raises requests.exceptions.RequestException on network/HTTP errors.

    Open-Meteo API docs: https://open-meteo.com/en/docs
    """
    url = "https://api.open-meteo.com/v1/forecast"

    # WHY these specific parameters? -- Open-Meteo returns only the fields
    # you ask for. "current" tells it we want real-time values (not hourly
    # forecasts). We request temperature, humidity, wind speed, and the
    # weather code (a numeric code describing conditions like "clear" or
    # "rain"). We also ask for the timezone so times are human-readable.
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "timezone": "auto",
    }

    response = requests.get(url, params=params, timeout=10)

    # WHY raise_for_status? -- If the server returns 4xx or 5xx, we want
    # to know immediately rather than trying to parse an error page as
    # weather data. This raises an HTTPError with the status code.
    response.raise_for_status()

    return response.json()


# WHY a lookup table? -- The WMO weather codes are numeric and meaningless
# to a human. This dict translates the most common ones into plain English.
# Full spec: https://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/
WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def describe_weather_code(code):
    """Convert a WMO weather code integer into a human-readable string.

    Returns "Unknown" for codes not in our lookup table.
    """
    return WEATHER_DESCRIPTIONS.get(code, "Unknown (code {})".format(code))


def format_dashboard(data):
    """Format weather data into a readable terminal dashboard.

    Takes the parsed JSON dict from Open-Meteo and returns a
    multi-line string ready to print.
    """
    current = data["current"]
    units = data["current_units"]

    # WHY .get() with defaults? -- If the API changes or omits a field,
    # .get() returns our fallback instead of crashing with a KeyError.
    temp = current.get("temperature_2m", "N/A")
    humidity = current.get("relative_humidity_2m", "N/A")
    wind = current.get("wind_speed_10m", "N/A")
    weather_code = current.get("weather_code", -1)
    time_str = current.get("time", "N/A")

    temp_unit = units.get("temperature_2m", "")
    humidity_unit = units.get("relative_humidity_2m", "")
    wind_unit = units.get("wind_speed_10m", "")

    condition = describe_weather_code(weather_code)

    lat = data.get("latitude", "?")
    lon = data.get("longitude", "?")
    tz = data.get("timezone", "?")

    # WHY a separator line? -- Visual structure helps users scan the
    # output quickly. The fixed-width labels align values into a column.
    lines = [
        "",
        "========================================",
        "         WEATHER DASHBOARD",
        "========================================",
        "",
        "  Location  : {}, {}".format(lat, lon),
        "  Timezone  : {}".format(tz),
        "  Updated   : {}".format(time_str),
        "",
        "----------------------------------------",
        "  Condition : {}".format(condition),
        "  Temp      : {}{}".format(temp, temp_unit),
        "  Humidity  : {}{}".format(humidity, humidity_unit),
        "  Wind      : {}{}".format(wind, wind_unit),
        "----------------------------------------",
        "",
    ]

    return "\n".join(lines)


def main(args=None):
    """Entry point: parse arguments, fetch weather, display dashboard.

    Accepts an optional args list for testing. If None, uses sys.argv[1:].
    """
    if args is None:
        args = sys.argv[1:]

    # --- Parse arguments ---
    if not args:
        print("Usage: python project.py <city-name>  OR  python project.py <lat> <lon>")
        print("\nAvailable city presets:")
        for name, (lat, lon) in sorted(CITY_PRESETS.items()):
            print("  {:<12s}  ({}, {})".format(name, lat, lon))
        print("\nExample: python project.py tokyo")
        return 1

    try:
        latitude, longitude = parse_arguments(args)
    except ValueError as err:
        print("Error: {}".format(err))
        return 1

    # --- Fetch weather ---
    try:
        data = fetch_weather(latitude, longitude)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the Open-Meteo API.")
        print("Check your internet connection and try again.")
        return 1
    except requests.exceptions.Timeout:
        print("Error: Request timed out. The API might be slow — try again.")
        return 1
    except requests.exceptions.HTTPError as err:
        print("Error: The API returned an error: {}".format(err))
        return 1
    except requests.exceptions.RequestException as err:
        print("Error: Something went wrong with the request: {}".format(err))
        return 1

    # --- Display dashboard ---
    dashboard = format_dashboard(data)
    print(dashboard)
    return 0


if __name__ == "__main__":
    sys.exit(main())
