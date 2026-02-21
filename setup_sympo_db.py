import sqlite3

conn = sqlite3.connect("food.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS users")

c.execute("""
CREATE TABLE users (
    reg_id TEXT PRIMARY KEY,
    tg_id INTEGER,
    otp TEXT,
    redeemed INTEGER
)
""")

conn.commit()
conn.close()

print("One-day symposium database ready")