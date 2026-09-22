import json
import os
from mappers.order_mapper import OrderMapper

class OrderRepo:
    def __init__(self, file_path = 'data/orders.json'):
        self.file_path = file_path

    def _load_raw(self):
        try:
            with open(self.file_path, 'r', encoding= 'utf-8') as f:
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_raw(self, orders_raw):
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        temp_file = f"{self.file_path}.tmp"

        try:
            with open(temp_file, 'w', encoding= 'utf-8') as f:
                json.dump(orders_raw, f, indent= 4, ensure_ascii= False)

            os.replace(temp_file, self.file_path)

        except Exception as e:
            if os.path.exists(temp_file):
                os.remove(temp_file)

            raise e

    def save(self, order_obj):
        orders = self._load_raw()
        orders[str(order_obj.order_id)] = OrderMapper.to_order_raw(order_obj)
        self._save_raw(orders)

    def get_next_id(self):
        orders = self._load_raw()

        return max((int(o_id) for o_id in orders.keys()), default= 0) + 1