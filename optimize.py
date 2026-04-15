import sqlite3

conn = sqlite3.connect("services.db")
cursor = conn.cursor()

cursor.execute("CREATE INDEX IF NOT EXISTS idx_service_no ON services(service_no)")

conn.commit()
conn.close()

print("Database optimized!")
