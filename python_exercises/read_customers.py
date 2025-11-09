import csv
from pathlib import Path

DATA = Path(__file__).parent / "data" / "customers.csv"

def read_customers(path=DATA):
    customers = []
    # Add encoding='utf-8-sig' to remove BOM issue
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            row["is_active"] = str(row["is_active"]).strip().lower() == "true"
            customers.append(row)
    return customers

def demo_collections(customers):
    emails = [c["email"] for c in customers]
    cities_tuple = tuple(c["city"] for c in customers)
    unique_cities = {c["city"] for c in customers}
    id_to_name = {
        int(c["customer_id"]): f'{c["first_name"]} {c["last_name"]}'
        for c in customers
    }
    return emails, cities_tuple, unique_cities, id_to_name

if __name__ == "__main__":
    rows = read_customers()
    print("✅ Loaded customers:", len(rows))
    for c in rows:
        print(f'- {c["customer_id"]}: {c["first_name"]} {c["last_name"]} | {c["email"]} | {c["city"]} | active={c["is_active"]}')

    emails, cities_t, unique_cities, id_to_name = demo_collections(rows)
    print("\nEmails (list):", emails)
    print("Cities (tuple):", cities_t)
    print("Unique cities (set):", unique_cities)
    print("ID→Name (dict):", id_to_name)
