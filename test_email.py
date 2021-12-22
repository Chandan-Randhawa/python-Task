from starlette.testclient import TestClient
from main import app 

def test_app_status():
    client = TestClient(app)
    response = client.post("/sendEmail?email=chandanveer.singh@digimantra.com")
    assert response.status_code == 200

def test_app_response():
    client = TestClient(app)
    response = client.post("/sendEmail?email=chandanveer.singh@digimantra.com")
    assert response.json() == {"message": "email has been sent"}


