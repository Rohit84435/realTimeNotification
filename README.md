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
