from shopping_cart_user import *
import os

if __name__ == "__main__":
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
    # Login
    # print('\nHello. Please log in to continue.')
    # username = input('Username: ')
    # email = input('Email: ')
    # customer = Customer(username, email)
    clear()
    customer = Customer('andrzej3', 'ag3@wp.pl')

    # Interface
    while True:
        print("\n1. Display products")
        print("2. Add product to cart")
        print("3. View cart")
        print("4. Checkout")
        print("5. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            clear()
            display_products()
        elif choice == '2':
            product_id = int(input("Enter product ID: "))
            quantity = int(input("Enter quantity: "))
            clear()
            customer.shopping_cart.add_product( product_id, quantity)
        elif choice == '3':
            clear()
            customer.shopping_cart.display_cart()
        elif choice == '4':
            clear()
            total = customer.shopping_cart.calculate_total()
            print(f"Paid: {total:.2f}")
        elif choice == '5':
            clear()
            break
        else:
            clear()
            print("Invalid choice. Please try again.")
