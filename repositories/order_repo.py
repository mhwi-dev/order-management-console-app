import json
import os

from mappers.order_mapper import OrderMapper
from models.order import Order


class OrderRepo:
    def __init__(self, file_path: str = 'data/orders.json') -> None:
        self.file_path = file_path

    def _load_raw(self) -> dict[str, dict]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("Invalid orders.json structure!")

            return data

        except FileNotFoundError:
            return {}

    def _save_raw(self, orders_raw: dict[str, dict]) -> None:
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        temp_file = f"{self.file_path}.tmp"

        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(orders_raw, f, indent=4, ensure_ascii=False)

            os.replace(temp_file, self.file_path)

        except Exception:
            if os.path.exists(temp_file):
                os.remove(temp_file)

            raise

    def save(self, order_obj: Order) -> None:
        orders = self._load_raw()
        orders[str(order_obj.order_id)] = OrderMapper.to_order_raw(order_obj)
        self._save_raw(orders)

    def get_next_id(self) -> int:
        orders = self._load_raw()

        return max((int(o_id) for o_id in orders.keys()), default=0) + 1