import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

# --- Products catalog ---
products = [
    {"name": "Amul Milk 500ml",       "category": "Dairy & Eggs",    "price": 28,  "cost": 20},
    {"name": "Amul Milk 1L",          "category": "Dairy & Eggs",    "price": 54,  "cost": 38},
    {"name": "Britannia Bread",       "category": "Grocery",         "price": 42,  "cost": 28},
    {"name": "Maggi 2-Min Noodles",   "category": "Snacks",          "price": 14,  "cost": 8},
    {"name": "Parle-G Biscuits",      "category": "Snacks",          "price": 10,  "cost": 6},
    {"name": "Coca-Cola 750ml",       "category": "Beverages",       "price": 45,  "cost": 28},
    {"name": "Tata Salt 1kg",         "category": "Grocery",         "price": 22,  "cost": 14},
    {"name": "Aashirvaad Atta 5kg",   "category": "Grocery",         "price": 248, "cost": 185},
    {"name": "Fortune Sunflower Oil", "category": "Grocery",         "price": 165, "cost": 120},
    {"name": "Lay's Classic Salted",  "category": "Snacks",          "price": 20,  "cost": 11},
    {"name": "Sprite 750ml",          "category": "Beverages",       "price": 42,  "cost": 26},
    {"name": "Dove Soap 100g",        "category": "Personal Care",   "price": 55,  "cost": 34},
    {"name": "Colgate Toothpaste",    "category": "Personal Care",   "price": 74,  "cost": 46},
    {"name": "Pampers Diapers S",     "category": "Baby & Kids",     "price": 699, "cost": 510},
    {"name": "Tomatoes 500g",         "category": "Fruits & Veggies","price": 25,  "cost": 16},
    {"name": "Banana Dozen",          "category": "Fruits & Veggies","price": 48,  "cost": 30},
    {"name": "Onions 1kg",            "category": "Fruits & Veggies","price": 34,  "cost": 22},
    {"name": "Kurkure Masala Munch",  "category": "Snacks",          "price": 20,  "cost": 11},
    {"name": "Red Bull 250ml",        "category": "Beverages",       "price": 125, "cost": 82},
    {"name": "Amul Butter 500g",      "category": "Dairy & Eggs",    "price": 262, "cost": 190},
]

# Hourly order weight (peaks at 8am, 1pm, 9pm)
hour_weights = [0.5,0.2,0.1,0.2,0.4,0.8,1.2,2.0,
                3.8,2.5,2.1,2.8,4.2,3.6,2.8,2.4,
                2.6,3.0,3.4,4.8,3.2,2.4,1.8,1.0]

def generate_orders(n=5000):
    rows = []
    start = datetime(2024, 1, 1)
    for i in range(n):
        # random date in 2024
        day_offset = random.randint(0, 364)
        hour = random.choices(range(24), weights=hour_weights)[0]
        minute = random.randint(0, 59)
        ts = start + timedelta(days=day_offset, hours=hour, minutes=minute)

        product = random.choice(products)
        qty = random.choices([1,2,3,4,5], weights=[50,25,12,8,5])[0]
        delivery_min = round(np.random.normal(9.4, 2.1), 1)
        delivery_min = max(4.0, min(25.0, delivery_min))
        refunded = random.random() < 0.023
        rating = random.choices([1,2,3,4,5], weights=[2,3,8,32,55])[0]

        rows.append({
            "order_id":      f"BLK{100000+i}",
            "timestamp":     ts.strftime("%Y-%m-%d %H:%M:%S"),
            "month":         ts.strftime("%b"),
            "hour":          hour,
            "product_name":  product["name"],
            "category":      product["category"],
            "unit_price":    product["price"],
            "unit_cost":     product["cost"],
            "quantity":      qty,
            "revenue":       product["price"] * qty,
            "gross_profit":  (product["price"] - product["cost"]) * qty,
            "delivery_mins": delivery_min,
            "refunded":      refunded,
            "rating":        rating,
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_orders(5000)
    df.to_csv("orders.csv", index=False)
    print(f"Generated {len(df)} orders")
    print(df.head())
