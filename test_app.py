import pytest
from app import create_app, db

@pytest.fixture()
def client():
    # ✅ Create app with in-memory SQLite for tests
    app = create_app(testing=True, database_uri="sqlite:///:memory:")

    with app.app_context():
        db.drop_all()   # ✅ Clear all old tables before tests
        db.create_all() # ✅ Recreate fresh schema

    # ✅ Return test client
    yield app.test_client()

    # ✅ Clean up after tests (optional, but good practice)
    with app.app_context():
        db.session.remove()
        db.drop_all()
