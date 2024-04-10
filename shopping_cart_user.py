
import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn




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

class Product:
    pass    

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

class ShoppingCart:
    def __init__(self, owner: Customer):
        self.owner = owner
        self.products = {}  # Maps product_id to quantity

    def add_product(self, product_id, quantity=1):
        conn = self.owner.conn

        """Fetch a single product by its ID from the database"""
        sql = ''' SELECT * FROM products WHERE product_id = ? '''
        cur = self.owner.conn.cursor()
        cur.execute(sql, (product_id,))
        product = cur.fetchone()  # Returns a tuple of the product details

        if product:
            """Add a product to the cart by its ID"""
            if product_id in self.products:
                self.products[product_id] += quantity
            else:
                self.products[product_id] = quantity
            
            print(f"Added {quantity} of {product[1]} to the cart.")
        else:
            print("Product not found.")

        

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
# połączenie do bazy powinno być jako singleton? ewentualnie za każdym razem kończyć połączenie do bazy

