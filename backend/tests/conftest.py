from backend.api import create_app
from backend.utils import db

import os

import pytest


@pytest.fixture
def app(tmp_path):
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    os.environ["ADMIN_USERNAME"] = "test_admin"
    os.environ["ADMIN_PASSWORD"] = "super-secret"

    app = create_app("testing")
    db.init_db(app)

    engine = db.SessionLocal.bind
    db.Base.metadata.create_all(bind=engine)

    yield app

    db.SessionLocal.remove()
    db.Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def admin_headers(client):
    resp = client.post(
        "/api/auth/login",
        json={"username": os.environ["ADMIN_USERNAME"], "password": os.environ["ADMIN_PASSWORD"]},
    )
    assert resp.status_code == 200
    token = resp.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
