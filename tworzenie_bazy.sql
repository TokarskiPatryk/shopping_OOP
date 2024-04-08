CREATE TABLE IF NOT EXISTS users (
                                        user_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        email text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
                                        product_id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        description text,
                                        price real NOT NULL
                                        );

INSERT INTO products (name, description, price) 
VALUES  ('Product 1', 'Description 1', 10.99), 
        ('Product 2', 'Description 2', 19.99), 
        ('Product 3', 'Description 3', 14.99);