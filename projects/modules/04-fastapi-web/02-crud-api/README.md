# Module 04 / Project 02 — CRUD API

Home: [README](../../../../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

GET/POST/PUT/DELETE endpoints, Pydantic models for request validation, proper HTTP status codes.

## Why this project exists

Most web APIs revolve around four operations: Create, Read, Update, Delete (CRUD). This project builds a todo list API that demonstrates all four. You will learn how Pydantic models validate incoming data automatically, how to return the right HTTP status codes, and how to structure an API that follows REST conventions.

## Run

```bash
cd projects/modules/04-fastapi-web/02-crud-api
python app.py
```

Then open **http://127.0.0.1:8000/docs** to test every endpoint interactively.

Press `Ctrl+C` to stop the server.

## Expected output

Using the `/docs` interface or `curl`:

```bash
# Create a todo
curl -X POST http://127.0.0.1:8000/todos -H "Content-Type: application/json" -d '{"title": "Learn FastAPI"}'
# Returns: {"id": 1, "title": "Learn FastAPI", "completed": false}  (status 201)

# List all todos
curl http://127.0.0.1:8000/todos
# Returns: [{"id": 1, "title": "Learn FastAPI", "completed": false}]

# Update a todo
curl -X PUT http://127.0.0.1:8000/todos/1 -H "Content-Type: application/json" -d '{"title": "Learn FastAPI", "completed": true}'
# Returns: {"id": 1, "title": "Learn FastAPI", "completed": true}

# Delete a todo
curl -X DELETE http://127.0.0.1:8000/todos/1
# Returns: (empty, status 204)
```

## Alter it

1. Add a `description` field (optional string) to the todo model. Make sure it appears in create, update, and response models.
2. Add a `GET /todos?completed=true` query parameter that filters the list to only completed or only incomplete todos.
3. Add a `PATCH /todos/{todo_id}` endpoint that allows partial updates (only the fields you send get changed).

## Break it

1. Send a POST request with an empty body (no JSON). What error does FastAPI return?
2. Send a POST request where `title` is an integer instead of a string. Does Pydantic accept it? Why?
3. Try to GET, PUT, or DELETE a todo with an ID that does not exist. What happens?

## Fix it

1. The empty body error (422) is correct — Pydantic requires the `title` field. No fix needed; understand why validation matters.
2. Pydantic coerces the integer to a string by default. If you want strict validation, use `StrictStr` from pydantic. Try it and see how the behavior changes.
3. The 404 response for missing IDs is already handled. If it is not, add a check that raises `HTTPException(status_code=404, detail="Todo not found")`.

## Explain it

1. What is the difference between `TodoCreate` (the request model) and `TodoResponse` (the response model)? Why use separate models?
2. Why does the POST endpoint return status code 201 instead of 200?
3. Why does the DELETE endpoint return status code 204 with no body?
4. How does Pydantic validation work? Where do you define what fields are required vs. optional?

## Mastery check

You can move on when you can:

- create all four CRUD endpoints from memory,
- explain why separate request and response Pydantic models are a good practice,
- intentionally trigger a 422 validation error and explain the response body,
- describe what status codes 200, 201, 204, 404, and 422 mean.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [How Loops Work](../../../../concepts/how-loops-work.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Types and Conversions](../../../../concepts/types-and-conversions.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Continue to [03-database-backed](../03-database-backed/).
