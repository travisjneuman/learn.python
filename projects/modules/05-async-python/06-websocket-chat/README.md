# Module 05 / Project 06 — WebSocket Chat Server

[README](../../../../README.md) · [Module Index](../README.md)

<!-- modality-hub-start -->

### Learn Your Way

| Read | Build | Watch | Test | Review | Visualize | Try |
|:---: | :---: | :---: | :---: | :---: | :---: | :---:|
| — | **This project** | — | — | [Flashcards](../../../../practice/flashcards/README.md) | — | — |

<!-- modality-hub-end -->

## Focus

- WebSocket protocol basics (persistent, bidirectional connections)
- Building a WebSocket server with the `websockets` library
- Broadcasting messages to connected clients
- Handling connect/disconnect events
- Basic room management

## Why this project exists

HTTP is request-response: the client asks, the server answers. But real-time applications — chat, live dashboards, multiplayer games, collaborative editing — need the server to push data to clients without being asked. WebSockets provide a persistent, bidirectional connection that stays open. This project teaches you to build a WebSocket server from scratch, evolving from a simple echo server to a multi-user chat room.

## Prerequisites

- Module 05 Projects 01-05 (async basics through async web server)
- Comfortable with `async`/`await` and `asyncio`

## Run

```bash
cd projects/modules/05-async-python/06-websocket-chat
pip install -r requirements.txt
python project.py
```

Then connect with a WebSocket client (browser console, `websocat`, or the included test client):

```javascript
// Browser console
const ws = new WebSocket("ws://localhost:8765");
ws.onmessage = (e) => console.log(e.data);
ws.send("Hello from browser!");
```

## Tests

```bash
pytest tests/
```

## Alter it

- Add private messaging (`/whisper username message`)
- Add room support (`/join room-name`, `/leave`)
- Add a `/users` command that lists connected usernames
- Persist chat history to a file

## Break it

- What happens when a client disconnects mid-message?
- What if two clients send messages at the exact same time?
- What happens with very large messages?

## Explain it

- How is a WebSocket connection different from an HTTP request?
- What does the `async for message in websocket` pattern do?
- Why do we use a set to track connected clients?
