from models.user import User
from repositories.user_repo import UserRepo

VALID_ROLES = {"admin", "customer"}

class UserService:
    def __init__(self, user_repo: UserRepo) -> None:
        self.user_repo = user_repo

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_user_by_user_id(user_id)

    def login(self, username: str, password: str) -> User:
        username = username.strip()

        if not username:
            raise ValueError(f"ERROR: Username must not be empty! Try again.")

        if not password or not password.strip():
            raise ValueError("ERROR: Password must not be empty!")
            
        user = self.user_repo.get_user_by_username(username)

        if not user or password != user.password:
            raise ValueError (f"ERROR: Username or password incorrect! Try again.")

        return user

    def sign_up(
        self,
        username: str,
        password: str,
        full_name: str,
        role: str,
        current_user: User | None = None
    ) -> User:
        
        username = username.strip()
        full_name = full_name.strip()
        role = role.strip().lower()

        if not username:
            raise ValueError(f"ERROR: Username must not be empty! Try again.")

        if not password or not password.strip():
            raise ValueError("ERROR: Password must not be empty! Try again.")

        if not full_name:
            raise ValueError("ERROR: Full name must not be empty! Try again.")
        
        if role not in VALID_ROLES:
            raise ValueError("ERROR: Invalid role! Try again.")

        if role == "admin":
            if not current_user or current_user.role != "admin":
                raise ValueError("ERROR: Permission denied! Try again.")

        if self.user_repo.get_user_by_username(username):
            raise ValueError (f"ERROR: This username already existed! Try again.")

        next_id = self.user_repo.get_next_id()

        new_user = User(
            user_id= next_id,
            username= username,
            password= password,
            full_name= full_name,
            role= role
        )

        self.user_repo.save(new_user)

        return new_user

    def get_user_invalid(self) -> list[User]:
        users = self.user_repo.get_all()
        user_invalid = []

        for u_id, u_info in users.items():

            if (
                u_id <= 0
                or not u_info.username
                or not u_info.password
                or not u_info.full_name
                or u_info.role not in VALID_ROLES
            ):
                user_invalid.append(u_info)

        return user_invalid

