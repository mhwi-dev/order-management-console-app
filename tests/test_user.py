import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.user import User
from repositories.user_repo import UserRepo
from services.user_service import UserService

def make_service(tmp_path):
    repo = UserRepo(file_path=str(tmp_path / "users.json"))
    return UserService(repo)

def test_sign_up_success(tmp_path):
    service = make_service(tmp_path)

    user = service.sign_up("huy_test", "123456", "Nguyen Minh Huy", "customer")
    assert user is not None

def test_login_correct_password(tmp_path):
    service = make_service(tmp_path)
    service.sign_up("huy_test", "123456", "Nguyen Minh Huy", "customer")
    logged_in = service.login("huy_test", "123456")
    assert logged_in is not None

def test_login_wrong_password(tmp_path):
    service = make_service(tmp_path)
    service.sign_up("huy_test", "123456", "Nguyen Minh Huy", "customer")
    with pytest.raises(ValueError):
        service.login("huy_test", "sai_pass")

def test_get_user_invalid(tmp_path):
    service = make_service(tmp_path)

    repo = service.user_repo

    users_raw = {
        "1": {
            "user_id": 1,
            "username": "huy_nguyen",
            "password": "123456",
            "full_name": "Nguyen Huy",
            "role": "customer"
        },
        "2": {
            "user_id": 2,
            "username": "user_loi_1",
            "password": "123456",
            "full_name": "",
            "role": "customer"
        },
        "3": {
            "user_id": 3,
            "username": "user_loi_2",
            "password": "123456",
            "full_name": "Nguyen Van B",
            "role": "invalid_role"
        }
    }

    repo._save_raw(users_raw)

    invalid_list = service.get_user_invalid()

    assert len(invalid_list) == 2

    invalid_usernames = [u.username for u in invalid_list]

    assert "user_loi_1" in invalid_usernames
    assert "user_loi_2" in invalid_usernames
    assert "huy_nguyen" not in invalid_usernames

def test_duplicate_username(tmp_path):
    service = make_service(tmp_path)

    service.sign_up("huy_nguyen", "123456", "Nguyen Huy", "customer")

    with pytest.raises(ValueError):
        service.sign_up("huy_nguyen", "123456", "Nguyen Huy", "customer")

def test_login_nonexistent_username(tmp_path):
    service = make_service(tmp_path)

    service.sign_up("gdsagsa", "123456", "Nguyen Huy", "customer")

    with pytest.raises(ValueError):
        service.login("khong_ton_tai", "123456")

def test_unauthenticated_user_cannot_create_admin(tmp_path):
    service = make_service(tmp_path)

    with pytest.raises(ValueError):
        service.sign_up("huy_nguyen", "123456", "Nguyen Huy", "admin")

def test_customer_cannot_create_admin(tmp_path):
    service = make_service(tmp_path)

    customer = service.sign_up(
        "customer_01",
        "123456",
        "Customer",
        "customer"
    )

    with pytest.raises(ValueError):
        service.sign_up(
            "admin_01",
            "123456",
            "Admin",
            "admin",
            customer
        )

def test_admin_can_create_admin(tmp_path):
    service = make_service(tmp_path)

    admin = User(
        user_id=1,
        username="admin",
        password="123456",
        full_name="Admin",
        role="admin"
    )

    new_admin = service.sign_up(
        "admin_02",
        "123456",
        "New Admin",
        "admin",
        admin
    )

    assert new_admin.role == "admin"
    assert new_admin.username == "admin_02"