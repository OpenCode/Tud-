import pytest


# Mark test as asyncronous
pytestmark = pytest.mark.asyncio


async def test_create_task_success(client):
    """
    Create a task with all valid data.
    """
    response = await client.post(
        "/api/tasks",
        json={"title": "Test Task 1", "description": "Teeeeeeest", "completed": False}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task 1"
    assert "id" in data
    assert "created_at" in data


async def test_create_task_title_too_long(client):
    """
    Test 'too long' title (> 200 characters).
    """
    long_title = "A" * 201
    response = await client.post(
        "/api/tasks",
        json={"title": long_title}
    )
    assert response.status_code == 400
    assert "Il titolo deve essere lungo massimo 200 caratteri" in response.json()["detail"]


async def test_read_tasks_filtered(client):
    """
    Read data filtered by 'completed'
    """
    await client.post("/api/tasks", json={"title": "Completato", "completed": True})
    await client.post("/api/tasks", json={"title": "Attivo", "completed": False})
    response_completed = await client.get("/api/tasks?completed=true")
    assert response_completed.status_code == 200
    assert len(response_completed.json()) == 1
    assert response_completed.json()[0]["title"] == "Completato"
    response_active = await client.get("/api/tasks?completed=false")
    assert response_active.status_code == 200
    assert len(response_active.json()) == 1
    assert response_active.json()[0]["title"] == "Attivo"


async def test_update_task_toggle_completed(client):
    """
    Change data for existing task.
    """
    create_response = await client.post(
        "/api/tasks",
        json={
            "title": "Task da completare", 
            "description": "Inizialmente non completato", 
            "completed": False
        }
    )
    assert create_response.status_code == 201
    initial_data = create_response.json()
    task_id = initial_data["id"]
    update_payload = {
        "title": initial_data["title"],
        "description": initial_data["description"],
        "completed": True
    }
    update_response = await client.put(
        f"/api/tasks/{task_id}",
        json=update_payload
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["id"] == task_id
    assert updated_data["completed"] is True
    final_response = await client.get(f"/api/tasks/{task_id}")
    assert final_response.status_code == 200
    assert final_response.json()["completed"] is True
    invalid_payload = {
        "title": "A" * 201,
        "description": "Titolo troppo lungo",
        "completed": True
    }
    invalid_update_response = await client.put(
        f"/api/tasks/{task_id}",
        json=invalid_payload
    )
    assert invalid_update_response.status_code == 400
    assert "Il titolo deve essere lungo massimo 200 caratteri" in invalid_update_response.json()["detail"]
