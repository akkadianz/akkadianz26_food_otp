import sqlite3

STUDENT_IDS = [
    "921623106034",
    "921623106088",
    "921623106085"
]

conn = sqlite3.connect("food.db")
c = conn.cursor()

for sid in STUDENT_IDS:
    try:
        c.execute(
            "INSERT INTO users VALUES (?, NULL, NULL, 0)",
            (sid,)
        )
    except:
        pass

conn.commit()
conn.close()

print("Participants added")