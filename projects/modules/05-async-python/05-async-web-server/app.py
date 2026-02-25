"""
Async Web Server — FastAPI with async endpoints and background tasks.

This project builds a FastAPI server that uses async patterns:
- Async endpoints that don't block each other
- Background tasks for deferred work
- Streaming responses for large data
- Concurrent external requests from within endpoints

Key concepts:
- async def endpoints: FastAPI runs them on the event loop
- BackgroundTasks: run work after the response is sent
- StreamingResponse: send data in chunks instead of all at once
"""

import asyncio
import time
from datetime import datetime

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import StreamingResponse

# ── Create the app ───────────────────────────────────────────────────

app = FastAPI(
    title="Async Demo Server",
    description="A FastAPI server demonstrating async patterns",
    version="1.0.0",
)

# In-memory storage for background task results.
task_log = []


# ── Basic async endpoint ─────────────────────────────────────────────

@app.get("/")
async def root():
    """A simple endpoint. Because it's async, it doesn't block other requests."""
    return {
        "message": "Hello from the async server!",
        "time": datetime.now().isoformat(),
    }


# ── Slow endpoint (demonstrates non-blocking) ────────────────────────

@app.get("/slow")
async def slow_endpoint():
    """
    This endpoint takes 3 seconds, but it uses asyncio.sleep()
    so other requests can be handled while it waits.

    Try hitting /slow and then immediately hitting / in another tab.
    The / response comes back instantly because asyncio.sleep()
    doesn't block the event loop.
    """
    start = time.time()
    await asyncio.sleep(3)
    elapsed = time.time() - start
    return {
        "message": "Slow response complete",
        "waited_seconds": round(elapsed, 1),
    }


# ── Concurrent work inside an endpoint ───────────────────────────────

async def simulate_api_call(name, seconds):
    """Pretend to call an external API that takes some time."""
    await asyncio.sleep(seconds)
    return {"source": name, "data": f"result from {name}", "took": seconds}


@app.get("/aggregate")
async def aggregate_data():
    """
    Fetch data from multiple "sources" concurrently.
    Instead of 1 + 2 + 1.5 = 4.5 seconds, this takes ~2 seconds
    because all three calls happen at the same time.
    """
    start = time.time()

    # Fire all three "API calls" concurrently.
    results = await asyncio.gather(
        simulate_api_call("service-a", 1.0),
        simulate_api_call("service-b", 2.0),
        simulate_api_call("service-c", 1.5),
    )

    elapsed = time.time() - start
    return {
        "results": results,
        "total_time": round(elapsed, 1),
        "note": "All three ran concurrently, total time ≈ slowest one",
    }


# ── Background tasks ─────────────────────────────────────────────────

async def process_in_background(task_name, duration):
    """
    This runs AFTER the response is already sent to the client.
    Useful for sending emails, writing logs, processing uploads, etc.
    """
    await asyncio.sleep(duration)
    entry = {
        "task": task_name,
        "completed_at": datetime.now().isoformat(),
        "duration": duration,
    }
    task_log.append(entry)
    print(f"  [Background] Completed: {task_name}")


@app.post("/background-job")
async def start_background_job(
    task_name: str = "default-task",
    background_tasks: BackgroundTasks = None,
):
    """
    Start a background task and return immediately.
    The task runs after the response is sent.
    """
    background_tasks.add_task(process_in_background, task_name, 2.0)
    return {
        "message": f"Background task '{task_name}' started",
        "note": "Check /task-log in a few seconds to see the result",
    }


@app.get("/task-log")
async def get_task_log():
    """See which background tasks have completed."""
    return {"completed_tasks": task_log, "total": len(task_log)}


# ── Streaming response ───────────────────────────────────────────────

async def generate_numbers():
    """
    An async generator that yields numbers one at a time.
    Each number arrives with a delay, simulating a slow data source.
    """
    for i in range(1, 11):
        await asyncio.sleep(0.5)
        yield f"Number {i}: {i * i}\n"


@app.get("/stream")
async def stream_numbers():
    """
    Stream data to the client as it becomes available.
    The client sees numbers appearing one by one instead of
    waiting for all 10 to be computed.
    """
    return StreamingResponse(
        generate_numbers(),
        media_type="text/plain",
    )


# ── Health check ─────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    return {"status": "healthy", "background_tasks_completed": len(task_log)}


# ── Run the server ───────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    print("Starting async demo server...")
    print("Visit http://127.0.0.1:8000/docs to see the API documentation\n")

    # uvicorn runs the ASGI event loop that powers FastAPI.
    uvicorn.run(app, host="127.0.0.1", port=8000)
