import requests
from pygments.lexers import data

def test_show_person(api_url):
    response = requests.get(f"{api_url}/people")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_create_person(api_url):
    payload = {"name": "Kratos", "age": 1000}
    response = requests.post(f"{api_url}/people", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["Message"] == "Person added"
    assert data["Person"]["name"] == "Kratos"
    assert data["Person"]["age"] == 1000

def test_create_person_without_name(api_url):
    payload = {"age": 30}
    response = requests.post(f"{api_url}/people", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "Error" in data
    assert data["Error"] == "Name is required"

def test_delete_person(api_url):
    create_res = requests.post(
        f"{api_url}/people",
        json={"name": "Test", "age": 30}
    )
    assert create_res.status_code == 200
    person_id = create_res.json()["Person"]["id"]

    delete_res = requests.delete(f"{api_url}/people/{person_id}")
    assert delete_res.status_code == 200
    assert delete_res.json()["Message"] == "Person deleted"

    check_res = requests.get(f"{api_url}/people/{person_id}")
    assert check_res.status_code == 405

def test_delete_person_not_found(api_url):
    response = requests.delete(f"{api_url}/people/99999")
    assert response.status_code == 404
    data = response.json()
    assert "Error" in data
    assert data["Error"] == "Person not found"

