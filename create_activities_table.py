import psycopg2

conn = psycopg2.connect(
    host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
    database="jina_db",
    user="jina_db_user",
    password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS activities (
    id SERIAL PRIMARY KEY,
    jina VARCHAR(255) NOT NULL,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);
""")

conn.commit()
cursor.close()
conn.close()

print("✅ Table 'activities' imetengenezwa/kukuwepo tayari.")
