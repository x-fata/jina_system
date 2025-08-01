import psycopg2
from werkzeug.security import generate_password_hash

conn = psycopg2.connect(
    host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
    database="jina_db",
    user="jina_db_user",
    password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
)

c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS admins (
        id SERIAL PRIMARY KEY,
        jina TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
''')

admin_list = [("x-fata", "bizpass123"), ("nahya", "bizpass123")]

for jina, password in admin_list:
    hash = generate_password_hash(password)
    c.execute("INSERT INTO admins (jina, password_hash) VALUES (%s, %s) ON CONFLICT (jina) DO NOTHING", (jina, hash))

conn.commit()
conn.close()
print("✅ Admins database ready.")
