
import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def add_user(conn, user):
    """Add a new user into the users table"""
    sql = ''' INSERT INTO users(name,email)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def add_product(conn, product):
    """Add a new product into the products table"""
    sql = ''' INSERT INTO products(name,description,price)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product)
    conn.commit()
    return cur.lastrowid

def add_product_to_cart(customer, product_id, quantity):
    conn = create_connection("sklep")
    product = get_product_by_id(conn, product_id)
    if product:
        customer.shopping_cart.add_product(product_id, quantity)
        print(f"Added {quantity} of {product[1]} to the cart.")
    else:
        print("Product not found.")
    conn.close()


def get_product_by_id(conn, product_id):
    """Fetch a single product by its ID from the database"""
    sql = ''' SELECT * FROM products WHERE product_id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (product_id,))
    return cur.fetchone()  # Returns a tuple of the product details


def get_all_products(conn):
    """Fetch all products from the products table"""
    sql = ''' SELECT * FROM products '''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()  # This returns a list of tuples

def display_products():
    conn = create_connection("sklep")
    products = get_all_products(conn)
    if products:
        print(f"{'ID':<10}{'Name':<20}{'Description':<30}{'Price':<10}")
        for product in products:
            product_id, name, description, price = product
            print(f"{product_id:<10}{name:<20}{description:<30}{price:<10.2f}")
    else:
        print("No products found.")
    conn.close()  # Remember to close the connection when done


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.shopping_cart = ShoppingCart(self)

        self.conn = create_connection("sklep")
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
 


class Product:
    def __init__(self, name, description, price):
        self.conn = create_connection("sklep")
        self.product_id = add_product(self.conn, (name, description, price))
        self.name = name
        self.description = description
        self.price = price


class ShoppingCart:
    def __init__(self, owner: Customer):
        self.owner = owner
        self.products = {}  # Maps product_id to quantity

    def add_product(self, product_id, quantity=1):
        """Add a product to the cart by its ID"""
        if product_id in self.products:
            self.products[product_id] += quantity
        else:
            self.products[product_id] = quantity

    def remove_product(self, product_id):
        """Remove a product from the cart by its ID"""
        if product_id in self.products:
            del self.products[product_id]

    def calculate_total(self, conn):
        """Calculate the total cost of the shopping cart"""
        total = 0
        for product_id, quantity in self.products.items():
            cur = conn.cursor()
            cur.execute("SELECT price FROM products WHERE product_id = ?", (product_id,))
            price = cur.fetchone()[0]
            total += price * quantity
        return total



# sprawić aby klasa product była używana w shopping cart
# funkcja do wypisywania dostępnych produktów
# połączenie do bazy powinno być jako singleton? ewentualnie za każdym razem kończyć połączenie do bazy

