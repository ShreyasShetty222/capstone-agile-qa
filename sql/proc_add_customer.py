import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "bank_ecomm.db"

def add_customer(customer_id:int, first_name:str, last_name:str, email:str, city:str, is_active:bool=True):
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            INSERT INTO customers (customer_id, first_name, last_name, email, city, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (customer_id, first_name, last_name, email, city, 1 if is_active else 0))
        conn.commit()

def get_customer(email:str):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT customer_id, first_name, last_name, email, city, is_active FROM customers WHERE email = ?;", (email,))
        return cur.fetchone()

if __name__ == "__main__":
    # Demo insert
    add_customer(105, "Kiran", "Desai", "kiran.desai@example.com", "Chennai", True)
    print("Inserted:", get_customer("kiran.desai@example.com"))
