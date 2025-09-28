from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models import User

from tests.utils.utils import random_email, random_lower_string


def test_create_user(client: TestClient, db: Session) -> None:
    email = random_email()
    password = random_lower_string()

    r = client.post(
        f"{settings.API_V1_STR}/private/users/",
        json={
            "email": email,
            "password": password,
            "full_name": "Pollo Listo"
        },
    )

    # older hardcoded email & password
    # r = client.post(
    #     f"{settings.API_V1_STR}/private/users/",
    #     json={
    #         "email": "pollo@listo.com",
    #         "password": "password123",
    #         "full_name": "Pollo Listo",
    #     },
    # )

    assert r.status_code == 200

    data = r.json()

    user = db.exec(select(User).where(User.id == data["id"])).first()

    assert user
    # assert user.email == "pollo@listo.com" # hard coded email
    assert user.email == email
    assert user.full_name == "Pollo Listo"
