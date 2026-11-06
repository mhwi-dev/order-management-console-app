import json
import os
from models.product import Product
from mappers.product_mapper import ProductMapper

class ProductRepo:
    def __init__(self, file_path: str = "data/products.json") -> None:
        self.file_path = file_path

    def _load_raw(self) -> dict[str, dict]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("Invalid products.json structure!")

            return data

        except FileNotFoundError:
            return {}

    def _save_raw(self, product_raw: dict[str, dict]) -> None:
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok= True)

        temp_file = f"{self.file_path}.tmp"

        with open(temp_file, 'w', encoding= 'utf-8') as f:
            json.dump(product_raw, f, indent= 4, ensure_ascii= False)

        os.replace(temp_file, self.file_path)

    def save(self, product_obj: Product) -> None:
        products = self._load_raw()
        product_key = str(product_obj.product_id)
        products[product_key] = ProductMapper.to_product_raw(product_obj)
        self._save_raw(products)

    def get_all(self) -> dict[int, Product]:
        products = self._load_raw()

        return {
            int(product_id): ProductMapper.to_product_model(data)
            for product_id, data in products.items()
        }

    def get_product_by_product_id(self, product_id: int) -> Product | None:
        products = self._load_raw()
        product = products.get(str(product_id))

        if product is None:
            return None

        return ProductMapper.to_product_model(product)

    def get_next_id(self) -> int:
        products = self._load_raw()

        return max((int(p_id) for p_id in products.keys()), default=0) + 1

    def exists_by_name(self, name: str) -> bool:
        products = self._load_raw()
        normalized_name = (name or "").strip().casefold()

        if not normalized_name:
            return False
        
        return any(
            isinstance(p, dict) and str(p.get("name", "")).strip().casefold() == normalized_name
            for p in products.values()
        )

    def remove_product(self, product_id: int) -> bool:
        products = self._load_raw()
        product_key = str(product_id)

        if product_key in products:
            del products[product_key]
            self._save_raw(products)
            return True

        return False