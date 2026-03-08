import sqlite3

STUDENT_IDS = [
    "1","2","3","4","5"
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