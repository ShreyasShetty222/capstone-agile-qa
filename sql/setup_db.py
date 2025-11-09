import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "bank_ecomm.db"

schema_sql = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    city        TEXT,
    is_active   INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS products (
    product_id  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    price       REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    qty         INTEGER NOT NULL CHECK(qty > 0),
    order_date  TEXT DEFAULT (date('now')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);

CREATE VIEW IF NOT EXISTS active_customers_view AS
SELECT customer_id, first_name || ' ' || last_name AS full_name, email, city
FROM customers
WHERE is_active = 1;
"""

seed_sql = """
INSERT OR IGNORE INTO customers (customer_id, first_name, last_name, email, city, is_active) VALUES
(101, 'Anita', 'Sharma', 'anita@example.com', 'Mumbai', 1),
(102, 'Ravi', 'Khan',   'ravi.khan@example.com', 'Delhi', 1),
(103, 'Meera','Patil',  'meera.patil@example.com', 'Pune', 0),
(104, 'Ajay', 'Verma',  'ajay.verma@example.com', 'Bengaluru', 1);

INSERT OR IGNORE INTO products (product_id, name, price) VALUES
(1, 'Savings Account Setup', 0.00),
(2, 'Debit Card', 299.00),
(3, 'Credit Card', 499.00);

INSERT OR IGNORE INTO orders (order_id, customer_id, product_id, qty) VALUES
(1001, 101, 2, 1),
(1002, 102, 3, 2),
(1003, 104, 2, 1);
"""

def main():
    with sqlite3.connect(DB) as conn:
        conn.executescript(schema_sql)
        conn.executescript(seed_sql)
    print("✅ Database ready at:", DB)

if __name__ == "__main__":
    main()
