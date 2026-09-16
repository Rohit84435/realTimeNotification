from fastapi import FastAPI,status, HTTPException,Query , WebSocket, WebSocketDisconnect
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
    
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    def connect(self, user_id, websocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        print("Connected - ","user_id ->",user_id," websocket ->",websocket)
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, user_id, websocket):
        self.active_connections[user_id].remove(websocket)
        print("Disconnected - ","user_id ->",user_id," websocket ->",websocket)
        if len(self.active_connections[user_id]) == 0:
            del self.active_connections[user_id]
    
    async def send_to_user(self, user_id, message):
        
        print("Creating notifiaction for : ", user_id)
        if user_id in self.active_connections:
            
            for websocket in self.active_connections[user_id]:
                await websocket.send_json(message)


manager = ConnectionManager()          


@app.get("/")
async def home():
    return {"message": "NotifyFlow is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/notifications")
async def get_notifications(unread:bool=False, limit:int = Query(ge=1,le=100)):
    return {
        "unread":unread,
        "limit":limit
    }


@app.get("/about")
async def about_me():
    return {
        "project": "NotifyFlow",
        "version": "0.1.0",
        "description": "Real-time notification system",
    }


@app.post("/notifications", response_model=NotificationResponse,status_code=status.HTTP_201_CREATED)
async def create_notification(notification: NotificationCreate):
    
    notification_data = {
    "id": 1,
    "user_id": notification.user_id,
    "title": notification.title,
    "message": notification.message,
    }
    
    await manager.send_to_user(user_id=notification.user_id, message=notification_data)
    return {
        "id": 1,
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
    }

@app.get("/notifications/{notification_id}")
async def get_notification(notification_id: int):
    if notification_id != 1:
        raise HTTPException(status_code=404,detail="Notification not found")

    return {
        "id":1,
        "user_id": "rohit",
        "title":"Order update",
        "message" : "Your order has shipped"
    }

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket:WebSocket,user_id:str):
    await websocket.accept()
    
    manager.connect(user_id=user_id, websocket=websocket)
    
    await websocket.send_json({
        "message":"Connected",
        "user_id":user_id
    })
    
    try:
        while True:
            message = await websocket.receive_text()
            print("This is connected message ->",message)
            await websocket.send_text(message)
    
    except WebSocketDisconnect:
        print(f"{user_id} disconnected")
    
    finally:
        manager.disconnect(user_id, websocket)