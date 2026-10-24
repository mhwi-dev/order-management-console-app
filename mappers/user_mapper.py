from models.user import User

class UserMapper:
    @staticmethod
    def to_user_model(users_raw: dict) -> User | None:
        if not users_raw or not isinstance(users_raw, dict):
            return None
        
        return User(
            user_id= users_raw.get('user_id'),
            username= users_raw.get('username'),
            password = users_raw.get('password'),
            full_name= users_raw.get('full_name'),
            role= users_raw.get('role')
        )

    @staticmethod
    def to_user_raw(user_obj: User) -> dict:
        if not user_obj or not isinstance(user_obj, User):
            return None
        
        return {
            'user_id': user_obj.user_id,
            'username': user_obj.username,
            'password': user_obj.password,
            'full_name': user_obj.full_name,
            'role': user_obj.role
        }

