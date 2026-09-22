from models.product import Product

class ProductMapper:

    @staticmethod
    def to_product_model(product_raw: dict) -> Product:
        if not product_raw or not isinstance(product_raw, dict):
            return None
        
        return Product(
            product_id= product_raw.get('product_id'),
            name= product_raw.get('name'),
            price= product_raw.get('price'),
            stock= product_raw.get('stock')
        )

    @staticmethod
    def to_product_raw(product_obj: Product) -> dict:
        if not product_obj or not isinstance(product_obj, Product):
            return None
        
        return {
            'product_id': product_obj.product_id,
            'name': product_obj.name,
            'price': product_obj.price,
            'stock': product_obj.stock
        }
    