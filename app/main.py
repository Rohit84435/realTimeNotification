from fastapi import FastAPI,status
from pydantic import BaseModel, Field


app = FastAPI()


class NotificationCreate(BaseModel):
    user_id: str = Field(min_length=1)
    title: str = Field(min_length=3, max_length=100)
    message: str = Field(min_length=1, max_length=500)


class NotificationResponse(BaseModel):
    id: int
    user_id: str
    title: str
    message: str


@app.get("/")
async def home():
    return {"message": "NotifyFlow is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/notifications")
async def get_notifications():
    return []


@app.get("/about")
async def about_me():
    return {
        "project": "NotifyFlow",
        "version": "0.1.0",
        "description": "Real-time notification system",
    }


@app.post("/notifications", response_model=NotificationResponse,status_code=status.HTTP_201_CREATED)
async def create_notification(notification: NotificationCreate):
    return {
        "id": 1,
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
    }