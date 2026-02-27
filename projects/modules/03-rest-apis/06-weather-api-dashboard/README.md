# Module 03 / Project 06 — Weather API Dashboard

[README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| --- | **This project** | --- | --- | [Flashcards](../../../../practice/flashcards/README.md) | --- | --- |

<!-- modality-hub-end -->

## Focus

- Fetching real-world data from a public REST API (Open-Meteo)
- Passing query parameters to control what the API returns
- Parsing a nested JSON response to extract specific fields
- Accepting command-line arguments with `sys.argv`
- Handling network errors so the program never shows a raw traceback

## Why this project exists

The previous five projects used JSONPlaceholder, a fake API that returns fake data. This project connects you to a real API that returns real weather data. You will see how the same skills (GET requests, query parameters, JSON parsing, error handling) apply to a real-world service. You will also practice accepting user input from the command line, which is how most CLI tools work.

Open-Meteo is free, requires no API key, and returns richly structured JSON. It is an ideal next step before building your own APIs.

## How the Open-Meteo API works

Open-Meteo provides weather forecasts and current conditions via a simple REST endpoint:

```
https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current=temperature_2m
```

Key concepts:

- **No authentication required** — no API keys, no signup, no tokens.
- **Query parameters control everything** — you tell the API which location (latitude/longitude) and which weather variables you want (temperature, humidity, wind, etc.).
- **The response is nested JSON** — the top level has metadata (timezone, location), and the `current` key holds the actual weather values.
- **Units come in a separate key** — `current_units` tells you whether temperature is in Celsius or Fahrenheit, wind in km/h or mph, etc.

Example response (simplified):

```json
{
  "latitude": 40.71,
  "longitude": -74.01,
  "timezone": "America/New_York",
  "current": {
    "time": "2025-01-15T14:00",
    "temperature_2m": 3.5,
    "relative_humidity_2m": 65,
    "wind_speed_10m": 12.3,
    "weather_code": 2
  },
  "current_units": {
    "temperature_2m": "\u00b0C",
    "relative_humidity_2m": "%",
    "wind_speed_10m": "km/h"
  }
}
```

## Run

```bash
cd projects/modules/03-rest-apis/06-weather-api-dashboard
python project.py new-york
```

Or with raw coordinates:

```bash
python project.py 51.5074 -0.1278
```

To run the tests:

```bash
cd projects/modules/03-rest-apis/06-weather-api-dashboard
pytest tests/ -v
```

## Expected output

```text
========================================
         WEATHER DASHBOARD
========================================

  Location  : 40.71, -74.01
  Timezone  : America/New_York
  Updated   : 2025-01-15T14:00

----------------------------------------
  Condition : Partly cloudy
  Temp      : 3.5°C
  Humidity  : 65%
  Wind      : 12.3km/h
----------------------------------------
```

(Actual values will vary since this is live weather data.)

## Error handling

This project handles four categories of network errors:

| Error | What causes it | What the user sees |
|-------|---------------|-------------------|
| `ConnectionError` | No internet, DNS failure, server down | "Could not connect to the Open-Meteo API." |
| `Timeout` | Server too slow, network congestion | "Request timed out. The API might be slow." |
| `HTTPError` | API returns 4xx or 5xx status code | "The API returned an error: 400 Bad Request" |
| `RequestException` | Any other requests-related failure | "Something went wrong with the request." |

The program catches each type separately so it can give a specific, helpful message instead of a Python traceback.

## Alter it

1. Add a `--fahrenheit` flag that appends `&temperature_unit=fahrenheit` to the API request. Display the temperature in Fahrenheit instead of Celsius.
2. Add more city presets to the `CITY_PRESETS` dictionary. Try adding your own city.
3. Request additional weather variables from the API (e.g., `apparent_temperature`, `precipitation`, `surface_pressure`). Add them to the dashboard display.
4. Add color to the output using ANSI escape codes. Make the temperature red if above 30, blue if below 0.

## Break it

1. Change the API URL to `"https://api.open-meteo.com/v1/forecast-BROKEN"`. What error do you get? Is it a `ConnectionError` or `HTTPError`?
2. Set the timeout to `0.001` (1 millisecond). Can the request ever succeed?
3. Remove the `"current"` key from the params dict. What does the API return? Does `format_dashboard()` crash?
4. Pass latitude `999` and longitude `999` directly to `fetch_weather()` (bypassing validation). What does the API say?

## Fix it

1. After breaking the URL, fix it and add a constant `API_URL` at the top of the file so the URL is defined in one place.
2. After testing with a tiny timeout, add a minimum timeout check: if the timeout is less than 1 second, print a warning and use 10 seconds instead.
3. Add a check in `format_dashboard()`: if the `"current"` key is missing from `data`, print "No current weather data available" instead of crashing.

## Explain it

1. What is the difference between a query parameter and a path parameter in a URL? Which does Open-Meteo use?
2. Why does `fetch_weather()` raise exceptions instead of returning `None`? How does this differ from the approach in project 05?
3. What is a WMO weather code? Why does the API return a number instead of a string like "Partly cloudy"?
4. Why do we validate latitude/longitude ranges in `parse_arguments()` even though the API would also reject invalid values?
5. What does `sys.exit(main())` do that `main()` alone does not?

## Mastery check

You can move on when you can:

- fetch data from a real API and extract specific fields from nested JSON,
- handle at least three types of network errors with specific messages,
- accept and validate command-line arguments with `sys.argv`,
- explain why APIs use query parameters to control their behavior.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Collections Explained](../../../../concepts/collections-explained.md)
- [Errors and Debugging](../../../../concepts/errors-and-debugging.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Go back to the [Module 03 index](../README.md). If you are ready for more, continue to [Module 04 — FastAPI Web Apps](../../04-fastapi-web/).
