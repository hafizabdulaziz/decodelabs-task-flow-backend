"""
Integration tests for task CRUD API endpoints, pagination, filtering, search, and sorting.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


async def get_auth_header(ac: AsyncClient, email: str = "taskuser@decodelabs.com") -> dict:
    await ac.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "SecurePassword123!",
            "full_name": "Task User",
        },
    )
    login_resp = await ac.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "SecurePassword123!",
        },
    )
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.anyio
async def test_task_crud_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = await get_auth_header(ac)

        # 1. Create task
        create_resp = await ac.post(
            "/api/v1/tasks/",
            headers=headers,
            json={
                "title": "Complete Backend API",
                "description": "Implement task CRUD endpoints",
                "status": "pending",
                "priority": "high",
            },
        )
        assert create_resp.status_code == 201
        task_data = create_resp.json()
        assert task_data["title"] == "Complete Backend API"
        assert task_data["status"] == "pending"
        assert task_data["priority"] == "high"
        task_id = task_data["id"]

        # 2. List tasks
        list_resp = await ac.get("/api/v1/tasks/", headers=headers)
        assert list_resp.status_code == 200
        tasks = list_resp.json()
        assert len(tasks) == 1
        assert tasks[0]["id"] == task_id

        # 3. Get single task
        get_resp = await ac.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["title"] == "Complete Backend API"

        # 4. Update task
        update_resp = await ac.patch(
            f"/api/v1/tasks/{task_id}",
            headers=headers,
            json={"status": "in_progress", "title": "Complete Backend API (Updated)"},
        )
        assert update_resp.status_code == 200
        updated_data = update_resp.json()
        assert updated_data["title"] == "Complete Backend API (Updated)"
        assert updated_data["status"] == "in_progress"

        # 5. Delete task
        delete_resp = await ac.delete(f"/api/v1/tasks/{task_id}", headers=headers)
        assert delete_resp.status_code == 204

        # 6. Verify task is deleted (404)
        get_deleted_resp = await ac.get(f"/api/v1/tasks/{task_id}", headers=headers)
        assert get_deleted_resp.status_code == 404


@pytest.mark.anyio
async def test_task_filtering_pagination_search_sorting():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        headers = await get_auth_header(ac, email="advanceduser@decodelabs.com")

        # Create multiple tasks
        tasks_to_create = [
            {"title": "Alpha Task", "description": "Database migration", "status": "pending", "priority": "low"},
            {"title": "Beta Task", "description": "API security auth", "status": "in_progress", "priority": "medium"},
            {"title": "Gamma Task", "description": "Database optimization", "status": "completed", "priority": "high"},
            {"title": "Delta Task", "description": "Frontend UI", "status": "completed", "priority": "high"},
        ]

        for t in tasks_to_create:
            resp = await ac.post("/api/v1/tasks/", headers=headers, json=t)
            assert resp.status_code == 201

        # Test Pagination (skip=1, limit=2)
        pag_resp = await ac.get("/api/v1/tasks/?skip=1&limit=2", headers=headers)
        assert pag_resp.status_code == 200
        assert len(pag_resp.json()) == 2

        # Test Filtering (status_filter=completed)
        filter_resp = await ac.get("/api/v1/tasks/?status_filter=completed", headers=headers)
        assert filter_resp.status_code == 200
        filtered_tasks = filter_resp.json()
        assert len(filtered_tasks) == 2
        for task in filtered_tasks:
            assert task["status"] == "completed"

        # Test Search (q=Database)
        search_resp = await ac.get("/api/v1/tasks/?q=Database", headers=headers)
        assert search_resp.status_code == 200
        search_tasks = search_resp.json()
        assert len(search_tasks) == 2

        # Test Sorting (sort_by=title, order=asc)
        sort_resp = await ac.get("/api/v1/tasks/?sort_by=title&order=asc", headers=headers)
        assert sort_resp.status_code == 200
        sorted_tasks = sort_resp.json()
        assert sorted_tasks[0]["title"] == "Alpha Task"
        assert sorted_tasks[1]["title"] == "Beta Task"
