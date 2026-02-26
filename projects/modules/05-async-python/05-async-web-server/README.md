# Module 05 / Project 05 — Async Web Server

Home: [README](../../../../README.md) · Module: [Async Python](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- Async FastAPI endpoints
- Background tasks with `BackgroundTasks`
- Streaming responses with `StreamingResponse`
- Running async operations inside endpoints

## Why this project exists

FastAPI is async by default. This project brings together everything from this module — async functions, concurrent operations, queues — into a real web server. You will see how async makes web servers handle many requests without blocking.

## Run

```bash
cd projects/modules/05-async-python/05-async-web-server
pip install -r ../requirements.txt
python app.py
# Visit http://127.0.0.1:8000/docs to see the API
```

## Expected output

```text
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Then visit `/docs` in your browser to interact with the API.

## Alter it

1. Add an endpoint that fetches data from 3 external APIs concurrently and returns combined results.
2. Add a WebSocket endpoint that sends progress updates to the client.
3. Add a `/stats` endpoint that returns how many background tasks have completed.

## Break it

1. Use `time.sleep(10)` in an endpoint instead of `asyncio.sleep()`. Try hitting another endpoint while it sleeps.
2. Remove `async` from an endpoint that uses `await`. What error do you get?
3. Start a background task that raises an exception. What happens to the response?

## Fix it

1. Replace `time.sleep()` with `asyncio.sleep()` so other requests are not blocked.
2. Add error handling in background tasks so failures are logged, not lost.
3. Add a timeout to the slow endpoint using `asyncio.wait_for()`.

## Explain it

1. Why are FastAPI endpoints `async def` by default?
2. What happens when you define an endpoint with `def` (no async) in FastAPI?
3. How do background tasks differ from running something in the endpoint itself?
4. What would you use for truly long-running tasks that outlive a request?

## Mastery check

You can move on when you can:
- write async FastAPI endpoints,
- use BackgroundTasks for deferred work,
- explain why blocking calls hurt async servers,
- stream data to clients with StreamingResponse.

---

## Related Concepts

- [Api Basics](../../../../concepts/api-basics.md)
- [Async Explained](../../../../concepts/async-explained.md)
- [Functions Explained](../../../../concepts/functions-explained.md)
- [Http Explained](../../../../concepts/http-explained.md)
- [Quiz: Api Basics](../../../../concepts/quizzes/api-basics-quiz.py)

## Next

Go back to [Module index](../README.md) or continue to [Module 06 — Databases & ORM](../../06-databases-orm/).
