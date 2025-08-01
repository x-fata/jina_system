from flask import Flask, render_template, request, redirect, session
import psycopg2
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'bizkazi_secret_key'

# Function ya ku-connect database (inaitwa kila request)
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
        database="jina_db",
        user="jina_db_user",
        password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        jina = request.form['jina']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM admins WHERE jina = %s", (jina,))
            admin = cursor.fetchone()

            if admin and check_password_hash(admin[2], password):  # password_hash iko index 2
                session['admin'] = jina
                login_time = datetime.now()
                cursor.execute(
                    "INSERT INTO activities (jina, action, timestamp) VALUES (%s, %s, %s)",
                    (jina, 'login', login_time)
                )
                conn.commit()
                return redirect('/page2')
            else:
                error = 'Jina au Password si sahihi.'

        except Exception as e:
            error = f"Kuna tatizo: {e}"

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html', error=error)

@app.route('/page2')
def page2():
    if 'admin' not in session:
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Hapa tunaondoa 'added' na 'removed' mpaka zitakapokuwa tayari kwenye DB
        cursor.execute("""
            SELECT jina, action, timestamp
            FROM activities
            ORDER BY timestamp DESC
        """)
        rows = cursor.fetchall()

        activities = []
        for row in rows:
            activities.append({
                'jina': row[0],
                'action': row[1],
                'timestamp': row[2].strftime("%Y-%m-%d %H:%M:%S"),
                'added': '',    # Bado data hizi hazipo, tutaongeza baadaye
                'removed': ''   # Bado data hizi hazipo, tutaongeza baadaye
            })

    except Exception as e:
        return f"Kuna tatizo: {e}"

    finally:
        cursor.close()
        conn.close()

    return render_template('page2.html', activities=activities)

if __name__ == '__main__':
    app.run(debug=True)
