from shopping_cart_user import *

if __name__ == "__main__":
    customer = Customer('Andrzej7', 'andrzej7@gmail.com')

    # Assuming you have a customer instance
    product_id_to_add = 1  # Example product_id
    quantity_to_add = 2  # Quantity of the product to add

    add_product_to_cart(customer, product_id_to_add, quantity_to_add)

