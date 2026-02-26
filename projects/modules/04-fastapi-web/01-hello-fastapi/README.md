# Module 04 / Project 01 — Hello FastAPI

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

First endpoint, running with uvicorn, automatic interactive docs at `/docs`.

## Why this project exists

FastAPI is the fastest way to build a Python web API. This project gets you from zero to a running server in minutes. You will create your first endpoint, learn how FastAPI turns decorators into routes, and discover the automatic documentation that makes testing your API effortless.

## Run

```bash
cd projects/modules/04-fastapi-web/01-hello-fastapi
python app.py
```

Then open your browser to:

- **http://127.0.0.1:8000** — your root endpoint
- **http://127.0.0.1:8000/docs** — interactive Swagger UI documentation
- **http://127.0.0.1:8000/items/42?q=hello** — path and query parameters in action

Press `Ctrl+C` in the terminal to stop the server.

## Expected output

Visiting `http://127.0.0.1:8000` returns:

```json
{"message": "Hello, FastAPI!"}
```

Visiting `http://127.0.0.1:8000/items/42?q=hello` returns:

```json
{"item_id": 42, "q": "hello"}
```

Visiting `http://127.0.0.1:8000/health` returns:

```json
{"status": "healthy"}
```

## Alter it

1. Add a new `GET /greet/{name}` endpoint that returns `{"greeting": "Hello, {name}!"}`.
2. Add an optional query parameter `uppercase` (bool) to the greet endpoint. When true, return the greeting in all caps.
3. Add a `GET /add/{a}/{b}` endpoint that takes two integers and returns their sum.

## Break it

1. Change the decorator from `@app.get("/")` to `@app.get` (remove the parentheses and path). What error do you get?
2. Try visiting `http://127.0.0.1:8000/items/not-a-number`. What does FastAPI return? Why?
3. Change `item_id: int` to `item_id: str` in the function signature. How does the `/docs` page change?

## Fix it

1. After removing the parentheses, put them back and add the path string. Confirm the endpoint works again.
2. The 422 error from passing a non-integer is FastAPI's automatic validation. There is nothing to fix because validation is the correct behavior. Explain why in your notes.
3. Restore the `int` type hint. Notice how FastAPI uses Python type hints to validate inputs automatically.

## Explain it

1. What does the `@app.get("/")` decorator do? What happens if two routes have the same path?
2. What is the difference between a path parameter (`/items/{item_id}`) and a query parameter (`?q=hello`)?
3. Where does the interactive documentation at `/docs` come from? Did you write any HTML?
4. What role does `uvicorn` play? Why can't you just run a FastAPI app with `python app.py` without it?

## Mastery check

You can move on when you can:

- start the server and visit `/docs` without looking at these instructions,
- add a new endpoint with both path and query parameters,
- explain what uvicorn does and why FastAPI needs it,
- describe how type hints control validation.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [What is a Variable](../../../../concepts/what-is-a-variable.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Continue to [02-crud-api](../02-crud-api/).
