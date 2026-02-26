"""
WebSocket Chat Server — Real-time bidirectional communication.

This project builds a WebSocket server that evolves from a simple echo
server to a multi-user chat room with usernames and broadcast messaging.

Run:
    python project.py

Connect from browser console:
    const ws = new WebSocket("ws://localhost:8765");
    ws.onmessage = (e) => console.log(e.data);
    ws.send("/name Alice");
    ws.send("Hello everyone!");
"""

import asyncio
import json
import logging
from datetime import datetime

import websockets

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logger = logging.getLogger(__name__)


# WHY a global dict for connected clients? -- WebSocket connections are
# long-lived (unlike HTTP requests that open/close). We need to track who
# is connected so we can broadcast messages to everyone. The dict maps
# websocket objects to usernames for O(1) lookup during send operations.
clients: dict = {}


# --- Message Handling ---

async def broadcast(message: str, sender=None):
    """Send a message to all connected clients except the sender."""
    disconnected = set()
    for ws in clients:
        if ws != sender:
            try:
                await ws.send(message)
            except websockets.ConnectionClosed:
                disconnected.add(ws)
    # Clean up any clients that disconnected during broadcast
    for ws in disconnected:
        clients.pop(ws, None)


def format_message(username: str, text: str) -> str:
    """Format a chat message with timestamp and username."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] {username}: {text}"


async def handle_command(websocket, command: str) -> bool:
    """Handle slash commands. Returns True if the message was a command."""
    if not command.startswith("/"):
        return False

    parts = command.split(" ", 1)
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else ""

    if cmd == "/name":
        if not arg.strip():
            await websocket.send("Usage: /name <your-name>")
        else:
            old_name = clients[websocket]
            clients[websocket] = arg.strip()
            await websocket.send(f"Name set to: {arg.strip()}")
            await broadcast(f"*** {old_name} is now known as {arg.strip()} ***")
        return True

    elif cmd == "/users":
        user_list = ", ".join(sorted(clients.values()))
        await websocket.send(f"Connected users: {user_list}")
        return True

    elif cmd == "/help":
        help_text = (
            "Commands:\n"
            "  /name <name>  — Set your display name\n"
            "  /users        — List connected users\n"
            "  /help         — Show this help message\n"
            "  /quit         — Disconnect"
        )
        await websocket.send(help_text)
        return True

    elif cmd == "/quit":
        await websocket.close()
        return True

    else:
        await websocket.send(f"Unknown command: {cmd}. Type /help for commands.")
        return True


# --- Connection Handler ---

async def handle_client(websocket):
    """Handle a single WebSocket client connection."""
    # Assign a default username
    username = f"user-{id(websocket) % 10000}"
    clients[websocket] = username

    logger.info(f"{username} connected ({len(clients)} clients)")
    await websocket.send(f"Welcome! You are {username}. Type /name <name> to change it.")
    await broadcast(f"*** {username} joined the chat ***", sender=websocket)

    try:
        async for message in websocket:
            # Check for commands first
            if await handle_command(websocket, message):
                continue

            # Regular message — broadcast to everyone
            current_name = clients.get(websocket, username)
            formatted = format_message(current_name, message)
            logger.info(formatted)
            await broadcast(formatted, sender=websocket)
            # Echo back to sender with confirmation
            await websocket.send(formatted)

    except websockets.ConnectionClosed:
        logger.info(f"{clients.get(websocket, username)} disconnected")
    finally:
        name = clients.pop(websocket, username)
        await broadcast(f"*** {name} left the chat ***")
        logger.info(f"{name} removed ({len(clients)} clients)")


# --- Server ---

async def start_server(host: str = "localhost", port: int = 8765):
    """Start the WebSocket chat server."""
    logger.info(f"Starting chat server on ws://{host}:{port}")
    async with websockets.serve(handle_client, host, port):
        await asyncio.Future()  # Run forever


def get_server_info() -> dict:
    """Return current server state (for testing)."""
    return {
        "client_count": len(clients),
        "usernames": list(clients.values()),
    }


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        logger.info("Server stopped")
