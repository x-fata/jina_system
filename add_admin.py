import psycopg2
from werkzeug.security import generate_password_hash

# Connection details zako
conn = psycopg2.connect(
    host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
    database="jina_db",
    user="jina_db_user",
    password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
)

cursor = conn.cursor()

# Taarifa za admin mpya
jina = "admin1"
password = "admin"
password_hash = generate_password_hash(password)

# Insert kwenye database (tumia password_hash badala ya password)
cursor.execute("INSERT INTO admins (jina, password_hash) VALUES (%s, %s)", (jina, password_hash))
conn.commit()
conn.close()

print("✅ Admin 'admin1' ameongezwa kwa mafanikio.")
