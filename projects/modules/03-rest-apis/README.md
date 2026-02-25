# Module 03 — REST APIs: Consuming

[README](../../../README.md)

## Overview

This module teaches you how to consume REST APIs with Python. You will make HTTP requests, parse JSON responses, send data to servers, handle errors gracefully, and build a reusable API client class. Every project uses [JSONPlaceholder](https://jsonplaceholder.typicode.com), a free public API that requires no signup or authentication.

By the end of this module you will be comfortable pulling data from any public REST API and handling the things that go wrong along the way.

## Prerequisites

Complete **Level 2** before starting this module. You should be comfortable with:

- Functions and return values
- Dictionaries and lists
- Working with JSON data
- Basic error handling with try/except
- Classes and methods (Level 2 project 08)
- Running scripts from the command line

## Learning objectives

By the end of this module you will be able to:

1. Make GET requests with `requests.get()` and parse JSON responses.
2. Pass query parameters to filter and paginate API results.
3. Send POST requests with JSON bodies and custom headers.
4. Handle HTTP errors, timeouts, and retries with exponential backoff.
5. Build a reusable API client class using `requests.Session`.

## Projects

| # | Project | What you learn |
|---|---------|----------------|
| 01 | [First API Call](./01-first-api-call/) | `requests.get()`, response objects, JSON parsing |
| 02 | [Query Parameters](./02-query-parameters/) | Filtering, pagination, params dict vs URL string |
| 03 | [POST and Auth](./03-post-and-auth/) | POST requests, JSON body, custom headers |
| 04 | [Error Handling](./04-error-handling/) | Status codes, `raise_for_status()`, timeouts, retries |
| 05 | [API Client Class](./05-api-client-class/) | `requests.Session`, base URL pattern, reusable client |

Work through them in order. Each project builds on the previous one.

## Setup

Create a virtual environment and install dependencies before starting:

```bash
cd projects/modules/03-rest-apis
python -m venv .venv
source .venv/bin/activate    # macOS/Linux
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

See [concepts/virtual-environments.md](../../../concepts/virtual-environments.md) for a full explanation of virtual environments.

## Dependencies

This module requires one package (listed in `requirements.txt`):

- **requests** — makes HTTP requests simple. You call `requests.get(url)` and get a response object back with status code, headers, and body.

## A note on API usage

JSONPlaceholder is a free, open API. It does not require API keys or rate limiting. POST/PUT/DELETE requests are accepted but not actually persisted on the server. This makes it a perfect sandbox for learning without consequences.
