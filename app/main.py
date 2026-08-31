from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def home():
    return {"message":"NotifyFlow is running"}

@app.get("/health")
async def health():
    return {"status":"ok"}


@app.get("/notifications")
async def get_notifactions():
    return []