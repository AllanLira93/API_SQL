import requests

def test_show_discipline(api_url):
    response = requests.get(f"{api_url}/discipline")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) >0

def test_create_discipline(api_url):
    professor_res = requests.post(f"{api_url}/professor",json={"name":"Test"})
    assert professor_res.status_code == 200
    professor_id = professor_res.json()["Professor"]["id"]
    payload = {"discipline_name": "test_discipline", "professor_id": professor_id}
    response = requests.post(f"{api_url}/discipline", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["Message"] == "Discipline added"
    assert data["Discipline"]["discipline_name"] == "test_discipline"
    assert data["Discipline"]["professor_id"] == professor_id

def test_create_discipline_without_name(api_url):
    payload = {"professor_id":1}
    response = requests.post(f"{api_url}/discipline", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "Error" in data
    assert data["Error"] == "Discipline name is required"

def test_create_discipline_without_professor_id(api_url):
    payload = {"discipline_name": "test_discipline"}
    response = requests.post(f"{api_url}/discipline", json=payload)

    assert response.status_code == 400
    data = response.json()
    assert "Error" in data
    assert data["Error"] == "Professor_id is required"

def test_delete_discipline(api_url):
    professor_res = requests.post(f"{api_url}/professor",json={"name":"Test_professor_delete"})
    assert professor_res.status_code == 200
    professor_id = professor_res.json()["Professor"]["id"]
    discipline_res = requests.post(f"{api_url}/discipline", json={"discipline_name": "discipline_deleted", "professor_id": professor_id})
    assert discipline_res.status_code == 200
    discipline_id = discipline_res.json()["Discipline"]["discipline_id"]

    delete_res = requests.delete(f"{api_url}/discipline/{discipline_id}")
    assert delete_res.status_code == 200

    data = delete_res.json()
    assert data["Message"] == "Discipline deleted"
    assert data["Discipline"]["id"] == discipline_id
    assert data["Discipline"]["discipline_name"] == "discipline_deleted"

def test_delete_discipline_not_found(api_url):
    delete_res = requests.delete(f"{api_url}/discipline/99999")
    assert delete_res.status_code == 404

    data = delete_res.json()
    assert "Error" in data
    assert data["Error"] == "Discipline not found"
