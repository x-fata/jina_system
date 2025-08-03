import psycopg2
from werkzeug.security import generate_password_hash

# Connection details
conn = psycopg2.connect(
    host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
    database="jina_db",
    user="jina_db_user",
    password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
)
cursor = conn.cursor()

# Admin list
admins = ["admin1", "zaq", "tester", "nahya", "x-fata"]
shared_password = "admin"
hashed_password = generate_password_hash(shared_password)

for jina in admins:
    # Check if admin already exists
    cursor.execute("SELECT 1 FROM admins WHERE jina = %s", (jina,))
    if cursor.fetchone():
        print(f"⚠️ Admin '{jina}' tayari yupo. Skip...")
    else:
        cursor.execute(
            "INSERT INTO admins (jina, password_hash) VALUES (%s, %s)",
            (jina, hashed_password)
        )
        print(f"✅ Admin '{jina}' ameongezwa.")

conn.commit()
conn.close()
