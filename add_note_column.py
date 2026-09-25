import sqlite3

conn = sqlite3.connect('instance/ssmart.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE attendance ADD COLUMN actions VARCHAR(300)")
    conn.commit()
    print("Column 'actions' has been added to the attendance table")

except sqlite3.OperationalError as e:
    print(f"Note: {e}")

conn.close