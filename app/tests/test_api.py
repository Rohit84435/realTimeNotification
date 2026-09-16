from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status":"ok"}
    
def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "NotifyFlow is running"}
    
def test_create_notification():
    response = client.post("/notifications",json={
            "user_id": "rohit",
            "title": "Order Update",
            "message": "Your order has shipped"
        })
    
    
    assert response.status_code == 201
    assert response.json() == {
        "id":1,
        "user_id":"rohit",
        "title":"Order Update",
        "message":"Your order has shipped"
    }
    
def test_create_notification_invalid():
    response = client.post("/notifications",json={
        "user_id":"",
        "title":"Hi",
        "message":""
        }
    )
    print(response.json())
    assert response.status_code == 422