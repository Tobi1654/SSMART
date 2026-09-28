import sqlite3

conn = sqlite3.connect('instance/ssmart.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE attendance ADD COLUMN attendance_percentage FLOAT DEFAULT 0.0")
    conn.commit()
    print("Column 'attendance_percentage' has been added to the attendance table")

except sqlite3.OperationalError as e:
    print(f"Note: {e}")

conn.close