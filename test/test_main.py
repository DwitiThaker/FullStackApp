# # test/test_main.py
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
# from main import app
# from fastapi.testclient import TestClient
# from main import app
# from fastapi import status
# client = TestClient(app)
# def test_return_health_check():
#     response = client.get("/healthy")
#     assert response.status_code== status.HTTP_200_OK
#     assert response.json() == {'status':'Healthy'}

# test/test_main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from fastapi.testclient import TestClient
from fastapi import status
from main import app

# Create the test client
client = TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}