import requests

def test_professor(api_url):
    response = requests.get(f"{api_url}/professor")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_create_professor(api_url):
    payload = {"name":"Test_Professor"}
    response = requests.post(f"{api_url}/professor",json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["Message"] == "Professor added"
    assert data["Professor"]["name"] == "Test_Professor"
    assert "id" in data["Professor"]

def test_create_professor_without_name(api_url):
    payload = {}
    response = requests.post(f"{api_url}/professor",json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "Error" in data
    assert data["Error"] == "Name is required"

def test_delete_professor(api_url):
    create_res = requests.post(f"{api_url}/professor", json={"name": "Test_Professor"})
    assert create_res.status_code == 200
    professor_id = create_res.json()["Professor"]["id"]
    delete_res = requests.delete(f"{api_url}/professor/{professor_id}")
    assert delete_res.status_code == 200

    data = delete_res.json()

    assert data["Message"] == "Professor deleted"
    assert data["Professor"]["id"] == professor_id
    assert data["Professor"]["name"] == "Test_Professor"

def test_professor_not_found(api_url):
    delete_res = requests.delete(f"{api_url}/professor/99999")
    assert delete_res.status_code == 404
    data = delete_res.json()

    assert "Error" in data
    assert data["Error"] == "Professor not found"

