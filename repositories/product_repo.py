import json
import os
from models.product import Product
from mappers.product_mapper import ProductMapper

class ProdudctRepo:
    def __init__(self, file_path = 'data/products.json'):
        self.file_path = file_path

    def _load_raw(self):
        try:
            with open(self.file_path, 'r', encoding= 'utf-8') as f:
                return json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_raw(self, product_raw):
        dir_name = os.path.dirname(self.file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok= True)

        temp_file = f"{self.file_path}.tmp"

        with open(temp_file, 'w', encoding= 'utf-8') as f:
            json.dump(product_raw, f, indent= 4, ensure_ascii= False)

        os.replace(temp_file, self.file_path)

    def save(self, product_obj):
        products = self._load_raw()
        product_key = str(product_obj.product_id)
        products[product_key] = ProductMapper.to_product_raw(product_obj)
        self._save_raw(products)

    def get_all(self):
        products = self._load_raw()

        return {
            int(product_id): ProductMapper.to_product_model(data)
            for product_id, data in products.items()
        }

    def get_product_by_product_id(self, product_id):
        products = self._load_raw()
        product = products.get(str(product_id))

        if not product:
            return None

        return ProductMapper.to_product_model(product)

    def get_next_id(self):
        products = self._load_raw()

        return max((int(p_id) for p_id in products.keys()), default= 0) +1

    def exists_by_name(self, name):
        products = self._load_raw()

        return any(p.get('name').lower() == name.lower() for p in products.values())

    def remove_product(self, product_id):
        products = self._load_raw()
        product_key = str(product_id)

        if product_key in products:
            del products[product_key]
            self._save_raw(products)
            return True

        return False