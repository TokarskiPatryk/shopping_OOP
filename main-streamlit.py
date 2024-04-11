from shopping_cart_user import *
import streamlit as st
import numpy as np

customer = Customer('andrzej3', 'ag3@wp.pl')

### change interface to be button based

def show_menu():
    st.write("\n1. Display products")
    st.write("2. Add product to cart")
    st.write("3. View cart")
    st.write("4. Checkout")
    st.write("5. Exit")

# Insert a chat message container.
with st.chat_message("user"):
    show_menu()


# Display a chat input widget.
choice = st.chat_input("Say something")
if choice:
    if choice == '1':
        st.write(display_products())
    elif choice == '2':
        st.write(display_products())

        form = st.form(key='my_form')
        product_id = form.number_input('Product ID:')
        quantity = form.number_input("Quantity:")
        submit_button = form.form_submit_button(label='Submit')
        print(f'submit_button: {submit_button}')

        if submit_button:
            print('guzik klinkniety')
            print('product_id:', product_id)
            print('quantity:', quantity)
            products = customer.shopping_cart.add_product(product_id, quantity)
            st.write(products)
            print(products)
    elif choice == '3':
        customer.shopping_cart.display_cart()
    elif choice == '4':
        total = customer.shopping_cart.calculate_total()
        st.write(f"Paid: {total:.2f}")
        # TODO delete all products from cart
    else:
        st.write("Invalid choice. Please try again.")

### 

if __name__ == "__aamain__":
    # Login
    # print('\nHello. Please log in to continue.')
    # username = input('Username: ')
    # email = input('Email: ')
    # customer = Customer(username, email)
    customer = Customer('andrzej3', 'ag3@wp.pl')

    # Interface
    while True:
        st.write("\n1. Display products")
        st.write("2. Add product to cart")
        st.write("3. View cart")
        st.write("4. Checkout")
        st.write("5. Exit")
        choice = st.text_input("Enter choice: ")
        
        if choice == '1':
            display_products()
        elif choice == '2':
            product_id = st.number_input("Enter product ID: ")
            quantity = st.number_input("Enter quantity: ")
            customer.shopping_cart.add_product(product_id, quantity)
        elif choice == '3':
            customer.shopping_cart.display_cart()
        elif choice == '4':
            total = customer.shopping_cart.calculate_total()
            st.write(f"Paid: {total:.2f}")
            # TODO delete all products from cart
        else:
            st.write("Invalid choice. Please try again.")
