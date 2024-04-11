from __future__ import annotations
from threading import Lock, Thread
from typing import Optional

import sqlite3



class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instance: Optional[Database] = None

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Database(metaclass=SingletonMeta):

    def __init__(self, db_file: str = 'sklep') -> None:
        self.db_file = db_file
        self.conn = None

        try:
            self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        except sqlite3.Error as e:
            print('Sqlite3 error:')
            print(e)


def get_all_products():
    conn = Database().conn
    """Fetch all products from the products table"""
    sql = ''' SELECT * FROM products '''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()  # This returns a list of tuples

def display_products():
    to_return = ''
    products = get_all_products()
    if products:
        to_return+=f"{'ID':<10}{'Name':<20}{'Description':<30}{'Price':<10}\n"
        for product in products:
            product_id, name, description, price = product
            to_return+=f"{product_id:<10}{name:<20}{description:<30}{price:<10.2f}\n"
    else:
        to_return+="No products found.\n"
    return to_return


class Product:
    pass    

class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.shopping_cart = ShoppingCart(self)

        self.conn = Database().conn
        cur = self.conn.cursor()
        sql = ''' SELECT name, email
                    FROM users
                    WHERE name = ? AND email = ? '''
        cur.execute(sql, (self.name, self.email))
        self.conn.commit()

        if cur.fetchall():
            print("Logged in successfully!")
        else:
            sql = ''' INSERT INTO users(name,email)
                     VALUES(?,?) '''
            
            cur.execute(sql, (self.name, self.email))
            self.conn.commit() 
            print("Registered successfully!")
        self.id =cur.lastrowid

class ShoppingCart:
    def __init__(self, owner: Customer):
        self.owner = owner
        self.products = {}  # Maps product_id to quantity

    def add_product(self, product_id, quantity=1):
        conn = self.owner.conn
        to_return = ''

        """Fetch a single product by its ID from the database"""
        sql = ''' SELECT * FROM products WHERE product_id = ? '''
        cur = conn.cursor()
        cur.execute(sql, (product_id,))
        product = cur.fetchone()  # Returns a tuple of the product details

        if product:
            """Add a product to the cart by its ID"""
            if product_id in self.products:
                self.products[product_id] += quantity
            else:
                self.products[product_id] = quantity
            

            to_return+=f"Added {quantity} of {product[1]} to the cart."
        else:
            to_return+="Product not found."

        

    def remove_product(self, product_id):
        """Remove a product from the cart by its ID"""
        if product_id in self.products:
            del self.products[product_id]

    def calculate_total(self):
        """Calculate the total cost of the shopping cart"""
        total = 0
        for product_id, quantity in self.products.items():
            cur = self.owner.conn.cursor()
            cur.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
            price = cur.fetchone()[0]
            total += price * quantity
        return total
    
    def display_cart(self):
        """Display the contents of the shopping cart"""
        if self.products:
            print(f"{'ID':<10}{'Name':<20}{'Price':<10}{'Quantity':<10}")
            for product_id, quantity in self.products.items():
                cur = self.owner.conn.cursor()
                cur.execute("SELECT name, price FROM products WHERE product_id = ?", (product_id,))
                name, price = cur.fetchone()
                print(f"{product_id:<10}{name:<20}{price:<10.2f}{quantity:<10}")
            print(f"Total: {self.calculate_total():.2f}")
        else:
            print("Cart is empty.")



# sprawić aby klasa product była używana w shopping cart
# sprawdzić bezpieczeństwo połączenia z bazą
# dodać nowy main.py interfejs do web appki (streamlit?)
# postawić interface na dockerze?
