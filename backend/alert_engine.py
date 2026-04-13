import mysql.connector
import pandas as pd
from datetime import datetime

# 🔗 Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="erp_ai"
)

cursor = conn.cursor()

# 📥 Load Data
inventory = pd.read_sql("SELECT * FROM inventory", conn)
sales = pd.read_sql("SELECT * FROM sales", conn)
expiry = pd.read_sql("SELECT * FROM expiry", conn)

# 🔄 Create Product ID → Name Mapping
product_map = dict(zip(inventory['product_id'], inventory['product_name']))

# 🧹 (Optional but recommended) Clear old alerts
cursor.execute("DELETE FROM alerts")

# -------------------------------
# 🚨 LOW STOCK ALERT
# -------------------------------
for _, row in inventory.iterrows():
    if row['stock'] < row['reorder_level']:
        name = row['product_name']
        msg = f"{name} is low in stock"

        cursor.execute("""
            INSERT INTO alerts (product_id, alert_type, message)
            VALUES (%s, %s, %s)
        """, (row['product_id'], "Low Stock", msg))

# -------------------------------
# ⏳ EXPIRY ALERT
# -------------------------------
today = datetime.today()
expiry['expiry_date'] = pd.to_datetime(expiry['expiry_date'])

for _, row in expiry.iterrows():
    days_left = (row['expiry_date'] - today).days

    if days_left <= 7:
        name = product_map.get(row['product_id'], "Unknown Product")
        msg = f"{name} is expiring in {days_left} days"

        cursor.execute("""
            INSERT INTO alerts (product_id, alert_type, message)
            VALUES (%s, %s, %s)
        """, (row['product_id'], "Expiry Alert", msg))

# -------------------------------
# 📈 DEMAND SURGE & 📉 SALES DROP
# -------------------------------
sales_avg = sales.groupby('product_id')['quantity'].mean()

for product_id, avg in sales_avg.items():
    name = product_map.get(product_id, "Unknown Product")

    if avg > 100:
        msg = f"{name} has high demand"

        cursor.execute("""
            INSERT INTO alerts (product_id, alert_type, message)
            VALUES (%s, %s, %s)
        """, (product_id, "Demand Surge", msg))

    elif avg < 20:
        msg = f"{name} sales are dropping"

        cursor.execute("""
            INSERT INTO alerts (product_id, alert_type, message)
            VALUES (%s, %s, %s)
        """, (product_id, "Sales Drop", msg))

# 💾 Save Changes
conn.commit()

print(" Alerts generated successfully!")
