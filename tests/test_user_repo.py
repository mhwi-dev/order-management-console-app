import pytest

from repositories.user_repo import UserRepo
from models.user import User


def make_repo(tmp_path):
    file_path = tmp_path / "users.json"
    return UserRepo(file_path=str(file_path))


def make_user():
    return User(
        user_id=1,
        username="huy",
        password="123456",
        full_name="Nguyen Minh Huy",
        role="customer"
    )

def test_load_raw_file_not_found(tmp_path):
    repo = make_repo(tmp_path)

    result = repo._load_raw()

    assert result == {}

def test_save_user_success(tmp_path):
    repo = make_repo(tmp_path)
    user = make_user()

    repo.save(user)

    users = repo._load_raw()

    assert "1" in users
    assert users["1"]["username"] == "huy"
    assert users["1"]["full_name"] == "Nguyen Minh Huy"

def test_get_user_by_user_id(tmp_path):
    repo = make_repo(tmp_path)
    user = make_user()

    repo.save(user)

    result = repo.get_user_by_user_id(1)

    assert result is not None
    assert result.user_id == 1
    assert result.username == "huy"

def test_get_user_by_username(tmp_path):
    repo = make_repo(tmp_path)
    user = make_user()

    repo.save(user)

    result = repo.get_user_by_username("huy")

    assert result is not None
    assert result.username == "huy"

def test_get_all_users(tmp_path):
    repo = make_repo(tmp_path)

    user_1 = make_user()

    user_2 = User(
        user_id=2,
        username="nam",
        password="654321",
        full_name="Nguyen Van Nam",
        role="customer"
    )

    repo.save(user_1)
    repo.save(user_2)

    result = repo.get_all()

    assert len(result) == 2
    assert 1 in result
    assert 2 in result
    assert result[1].username == "huy"
    assert result[2].username == "nam"

def test_get_next_id(tmp_path):
    repo = make_repo(tmp_path)

    user_1 = make_user()

    user_2 = User(
        user_id=5,
        username="nam",
        password="654321",
        full_name="Nguyen Van Nam",
        role="customer"
    )

    repo.save(user_1)
    repo.save(user_2)

    result = repo.get_next_id()

    assert result == 6
    