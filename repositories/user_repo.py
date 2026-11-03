import json
import os
from models.user import User
from mappers.user_mapper import UserMapper

class UserRepo:
    def __init__(self, file_path: str = 'data/users.json') -> None:
        self.file_path = file_path

    def _load_raw(self) -> dict[str, dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("Invalid users.json structure!")

            return data

        except FileNotFoundError:
            return {}

    def _save_raw(self, users_raw: dict[str, dict]) -> None:
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok= True)

        temp_file = f"{self.file_path}.tmp"

        with open(temp_file, 'w', encoding= 'utf-8') as f:
            json.dump(users_raw, f, indent=4, ensure_ascii= False)

        os.replace(temp_file, self.file_path)

    def save(self, user_obj: User) -> None:
        users = self._load_raw()
        user_key = str(user_obj.user_id)
        users[user_key] = UserMapper.to_user_raw(user_obj)
        self._save_raw(users)

    def get_all(self) -> dict[int, User]:
        users = self._load_raw()

        return {
            int(user_id): UserMapper.to_user_model(u_raw)
            for user_id, u_raw in users.items()
        }

    def get_user_by_user_id(self, user_id: int) -> User | None:
        users = self._load_raw()

        user_raw = users.get(str(user_id))

        if user_raw is None:
            return None

        return UserMapper.to_user_model(user_raw)

    def get_user_by_username(self, username: str) -> User | None:
        users = self._load_raw()

        return next(
            (
                UserMapper.to_user_model(u)
                for u in users.values()
                if username == u.get("username")
            ),
            None
        )

    def get_next_id(self) -> int:
        users = self._load_raw()

        return max((int(u_id) for u_id in users.keys()), default= 0) + 1

