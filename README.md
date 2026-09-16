# To run fast api through uv

uv run uvicorn app.main:app --reload

# 16. Status Code Cheat Sheet

- Keep this mental model:
- 200 → successful operation
- 201 → resource created
- 404 → resource doesn't exist
- 422 → request validation failed
- 401 → authentication problem
- 403 → authorization problem
- 500 → server-side failure

# WebSockets & Real-Time Communication

WebSocket is a persistent, bidirectional communication channel between a client and server. Unlike normal HTTP request/response communication, a WebSocket connection remains open, allowing both the client and server to send messages whenever needed.

In NotifyFlow, REST APIs and WebSockets have different responsibilities. REST APIs are used for operations such as creating and retrieving notifications, while WebSockets will eventually be used to deliver new notifications to connected users in real time.

FastAPI provides WebSocket support using @app.websocket() and the WebSocket class. A connection is first accepted using await websocket.accept(). Messages can then be received using await websocket.receive_text() and sent using await websocket.send_text().

A while True loop keeps the connection active so that the server can continuously receive and respond to messages.

We also learned why async/await is important for WebSocket applications. While one connection is waiting for network input, the asynchronous event loop can handle other requests and connections instead of blocking the entire application.

## Day 8 — WebSocket Connection Manager & User-Specific Delivery

Today we converted the basic WebSocket connection into a user-specific connection management system.

We created a `ConnectionManager` class responsible for maintaining active WebSocket connections. Since a single user can have multiple browser tabs or devices connected simultaneously, we store a list of WebSocket connections for each user.

The connection structure is:

{
"rohit": [websocket1, websocket2],
"alice": [websocket3]
}

The `ConnectionManager` provides three main operations:

- `connect()` — adds a WebSocket connection for a user.
- `disconnect()` — removes a specific WebSocket connection. If the user has no remaining connections, the user's entry is removed.
- `send_to_user()` — sends a JSON message to every active WebSocket connection belonging to a specific user.

We integrated the `ConnectionManager` into the WebSocket endpoint. When a client connects, its WebSocket is registered with the manager. When the client disconnects, the connection is removed using cleanup logic.

We also learned how `WebSocketDisconnect` represents a normal client-side disconnection and why `try/except/finally` can be used to handle the disconnect and guarantee connection cleanup.

The notification API was then connected to the WebSocket delivery mechanism. A notification created through the REST API can be passed to `send_to_user()`, which pushes the notification through every active WebSocket connection belonging to the target user.

For example:

POST /notifications
{
"user_id": "rohit",
"title": "Order Update",
"message": "Your order has shipped"
}

The notification is delivered to all of Rohit's active connections:

Rohit Tab 1 → receives notification
Rohit Tab 2 → receives notification

while another user's connection does not receive it:

Alice Tab → no notification

This is the first real user-specific real-time notification flow in NotifyFlow.

### Current Architecture

REST API
↓
Create Notification
↓
ConnectionManager
↓
send_to_user()
↓
User's WebSocket connections
↓
Browser clients

### Important limitation

The current `ConnectionManager` stores connections in Python process memory. Therefore, connection information is lost when the FastAPI process restarts and separate FastAPI instances cannot share the same connection state.

This is acceptable for the initial MVP. Later, Redis will be introduced to support communication and coordination when NotifyFlow runs across multiple FastAPI instances.

Another current limitation is that notifications are not yet persisted in PostgreSQL. If the target user is offline, there is currently nowhere to store the notification for later delivery.

The next major stage will introduce durable notification storage so that offline users can retrieve notifications after reconnecting.

## Day 22 — pytest Fundamentals

### What I Learned

Today I started automated testing for NotifyFlow using pytest.

### Key Concepts

- pytest is a Python testing framework used to automate application testing.
- Tests are discovered using test files such as `test_*.py`.
- Test functions normally start with `test_`.
- `assert` is used to verify expected behavior.
- FastAPI's `TestClient` allows API endpoints to be tested without manually using Postman.
- `client.get()` is used to test GET endpoints.
- `client.post()` is used to test POST endpoints.
- JSON request bodies are passed using the `json` parameter.
- `response.status_code` verifies the HTTP status code.
- `response.json()` allows validation of the API response body.
- FastAPI validation errors return HTTP `422`.

### Example

```python
response = client.post(
    "/notifications",
    json={
        "user_id": "rohit",
        "title": "Order Update",
        "message": "Your order has shipped"
    }
)

assert response.status_code == 201
```
