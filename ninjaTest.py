import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="test",
        password="12345abc",
        host="localhost",
        port=3306,
        database="ninjaRun"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute("SELECT * FROM User;")

for item in cur:
    print(item)
