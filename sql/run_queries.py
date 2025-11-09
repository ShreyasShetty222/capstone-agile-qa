import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "bank_ecomm.db"

def row_print(rows, title):
    print(f"\n=== {title} ===")
    for r in rows:
        print(r)

def main():
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()

        # SELECT
        cur.execute("SELECT customer_id, first_name, last_name, email, city, is_active FROM customers ORDER BY customer_id;")
        row_print(cur.fetchall(), "All customers")

        # UPDATE (set Meera active)
        cur.execute("UPDATE customers SET is_active = 1 WHERE email = ?;", ("meera.patil@example.com",))
        conn.commit()
        cur.execute("SELECT customer_id, first_name, last_name, is_active FROM customers WHERE email = ?;", ("meera.patil@example.com",))
        row_print(cur.fetchall(), "After UPDATE Meera to active")

        # DELETE (delete a demo order)
        cur.execute("DELETE FROM orders WHERE order_id = ?;", (1003,))
        conn.commit()
        cur.execute("SELECT order_id, customer_id, product_id, qty FROM orders ORDER BY order_id;")
        row_print(cur.fetchall(), "Orders after DELETE order_id=1003")

        # JOIN (Customer + Orders + Products)
        cur.execute("""
            SELECT o.order_id,
                   c.first_name || ' ' || c.last_name AS customer,
                   p.name AS product,
                   o.qty,
                   p.price,
                   (o.qty * p.price) AS total
            FROM orders o
            JOIN customers c ON c.customer_id = o.customer_id
            JOIN products  p ON p.product_id  = o.product_id
            ORDER BY o.order_id;
        """)
        row_print(cur.fetchall(), "JOIN: orders with customer + product + totals")

        # VIEW (Active customers)
        cur.execute("SELECT * FROM active_customers_view ORDER BY customer_id;")
        row_print(cur.fetchall(), "VIEW: active_customers_view")

    print("\n✅ Queries executed successfully.")

if __name__ == "__main__":
    main()
