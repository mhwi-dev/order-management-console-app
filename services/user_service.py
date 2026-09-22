from models.users import User

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_user_by_id(self, user_id):
        return self.user_repo.get_user_by_user_id(user_id)

    def login(self, username, password):
        user = self.user_repo.get_user_by_username(username)

        if not user or password != user.password:
            raise ValueError (f"ERROR: Username or password incorrect! Try again.")

        return user

    def sign_up(self, username, password, full_name, role):
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

    def get_user_invalid(self):
        users = self.user_repo.get_all()
        user_invalid = []

        for u_id, u_info in users.items():

            if not u_id or not u_info.username or not u_info.full_name or not u_info.role:
                user_invalid.append(u_info)

        return user_invalid

