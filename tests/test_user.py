import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    service.sign_up("huy_nguyen", "123456", "Nguyen Huy", "customer")
    service.sign_up("user_loi_1", "123456", "", "customer")
    service.sign_up("user_loi_2", "123456", "Nguyen Van B", "")

    invalid_list= service.get_user_invalid()

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

