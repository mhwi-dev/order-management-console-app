import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from repositories.product_repo import ProdudctRepo
from services.product_service import ProductService

def make_service(tmp_path):
    repo = ProdudctRepo(file_path= str(tmp_path / "products.json"))
    return ProductService(repo)

def test_add_product_success(tmp_path):
    service = make_service(tmp_path)

    new_product = service.add_new_product("Peach Tea", 55000, 15)

    assert new_product.product_id == 1
    assert new_product.name == "Peach Tea"
    assert new_product.price == 55000
    assert new_product.stock == 15
    assert len(service.show_products()) == 1

def test_add_product_negative_price(tmp_path):
    service = make_service(tmp_path)

    with pytest.raises(ValueError):
        service.add_new_product("Bad Tea", -5, 10)

    assert len(service.show_products()) == 0

def test_add_product_negative_stock(tmp_path):
    service = make_service(tmp_path)

    with pytest.raises(ValueError):
        service.add_new_product("Blended", 5, -10)

    assert len(service.show_products()) == 0

def test_add_product_duplicate(tmp_path):
    service = make_service(tmp_path)

    service.add_new_product("Peach Tea", 55000, 15)

    with pytest.raises(ValueError):
        service.add_new_product("Peach Tea", 55000, 15)

@pytest.mark.parametrize("name", ["", "   "])
def test_add_product_empty_name(tmp_path, name):
    service = make_service(tmp_path)

    with pytest.raises(ValueError):
        service.add_new_product(name, 55000, 15)

    assert len(service.show_products()) == 0

def test_update_product_not_found(tmp_path):
    service = make_service(tmp_path)

    with pytest.raises(ValueError):
        service.update_product(999, name="Ghost")

def test_update_product_negative_price(tmp_path):
    service = make_service(tmp_path)
    service.add_new_product("Peach Tea", 55000, 15)

    with pytest.raises(ValueError):
        service.update_product(1, price= -5)

def test_update_product_negative_price(tmp_path):
    service = make_service(tmp_path)
    service.add_new_product("Peach Tea", 55000, 15)

    with pytest.raises(ValueError):
        service.update_product(1, stock= -5)

def test_update_product_duplicate_name(tmp_path):
    service = make_service(tmp_path)
    service.add_new_product("Peach Tea", 55000, 15)
    service.add_new_product("Pink Guava", 55000, 12)

    with pytest.raises(ValueError):
        service.update_product(2, name= 'Peach Tea')

def test_update_product_same_name_allowed(tmp_path):
    service = make_service(tmp_path)
    service.add_new_product("Peach Tea", 55000, 15)
    service.update_product(1, name="Peach Tea", price=59000)

    updated = service.get_product_by_id(1)
    assert updated.price == 59000
    assert updated.name == "Peach Tea"