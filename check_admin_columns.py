import psycopg2

conn = psycopg2.connect(
    host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
    database="jina_db",
    user="jina_db_user",
    password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
)

cursor = conn.cursor()

cursor.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'admins';
""")

columns = cursor.fetchall()

print("🧾 Columns kwenye table ya 'admins':")
for col in columns:
    print("-", col[0])

conn.close()
