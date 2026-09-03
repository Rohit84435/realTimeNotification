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
