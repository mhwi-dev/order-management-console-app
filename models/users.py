class User:
    def __init__(self, user_id, username, password, full_name, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.role = role

    def __str__(self):
        return (
            f"User ID: {self.user_id} | "
            f"Username: {self.username} | "
            f"Password: ************* | "
            f"Full name: {self.full_name} | "
            f"Role: {self.role}"
        )

    def __repr__(self):
        return (
            f"User(user_id={self.user_id!r}, "
            f"username={self.username!r}, "
            f"password='******', "
            f"full_name={self.full_name!r}, "
            f"role={self.role!r})"
        )

