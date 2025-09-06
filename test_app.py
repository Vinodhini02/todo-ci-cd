import pytest
from app import create_app, db

@pytest.fixture()
def test_client():
    # Create app with in-memory SQLite for tests
    app = create_app(testing=True, database_uri="sqlite:///:memory:")

    with app.app_context():
        db.drop_all()   # Clear old tables
        db.create_all() # Fresh schema

    # Yield test client
    yield app.test_client()

    # Cleanup after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()

# -----------------------------
# ✅ Actual test functions below
# -----------------------------

def test_health(test_client):
    """Check health endpoint"""
    r = test_client.get("/api/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_create_and_list_task(test_client):
    """Add a new task and list it"""
    r = test_client.post("/api/tasks", json={"title": "learn CI/CD"})
    assert r.status_code == 201

    r = test_client.get("/api/tasks")
    assert r.status_code == 200
    data = r.get_json()
    assert any(t["title"] == "learn CI/CD" for t in data)
