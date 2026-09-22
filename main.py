#USER IMPORT
from repositories.user_repo import UserRepo
from services.user_service import UserService
from controllers.user_controller import UserController

#PRODUCT IMPORT
from repositories.product_repo import ProdudctRepo
from services.product_service import ProductService
from controllers.product_controller import ProductController

#CART IMPORT
from repositories.cart_repo import CartRepo
from services.cart_service import CartSerivce
from controllers.cart_controller import CartController

#ORDER IMPORT
from repositories.order_repo import OrderRepo
from services.order_service import OrderService
from controllers.order_controller import OrderController

#MAIN IMPORT
from controllers.main_controller import MainController

def run_system():

    #USER
    user_repo = UserRepo()
    user_service = UserService(user_repo)
    user_controller = UserController(user_service)

    #PRODUCT
    product_repo = ProdudctRepo()
    product_service = ProductService(product_repo)
    product_controller = ProductController(product_service)

    #CART
    cart_repo = CartRepo()
    cart_service = CartSerivce(cart_repo)
    cart_controller = CartController(cart_service, product_service)

    #ORDER
    order_repo = OrderRepo()
    order_service = OrderService(order_repo, user_service, cart_service, product_service)
    order_controller = OrderController(order_service, cart_service)

    #MAIN
    main_controller = MainController(user_controller, product_controller, cart_controller, order_controller)
    main_controller.run()

if __name__ == '__main__':
    run_system()
