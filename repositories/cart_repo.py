import os 
import json
from models.cart import Cart
from mappers.cart_mapper import CartMapper

class CartRepo:
    def __init__(self, file_path = 'data/carts.json'):
        self.file_path = file_path

    def _load_raw(self):
        try: 
            with open(self.file_path, 'r', encoding= 'utf-8') as f:
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_raw(self, carts_raw):
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok= True)

        temp_file = f"{self.file_path}.tmp"

        with open(temp_file, 'w', encoding= 'utf-8') as f:
            json.dump(carts_raw, f, indent= 4, ensure_ascii= False)

        os.replace(temp_file, self.file_path)

    def save(self, cart_obj):
        carts = self._load_raw()
        cart_obj_key = str(cart_obj.user_id)
        carts[cart_obj_key] = CartMapper.to_cart_raw(cart_obj)

        self._save_raw(carts)

    def get_cart_by_user_id(self, user_id):
        carts = self._load_raw()
        user_cart = carts.get(str(user_id))

        if not user_cart:
            return None

        return CartMapper.to_cart_model(user_cart)