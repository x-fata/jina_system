from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'bizkazi_secret_key'

def get_db_connection():
    return psycopg2.connect(
        host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
        port=5432,
        database="jina_db",
        user="jina_db_user",
        password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        jina = request.form['jina']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admins WHERE jina = %s", (jina,))
            admin = cursor.fetchone()

            if admin and check_password_hash(admin[2], password):
                session['admin'] = jina
                return redirect('/add-product')
            else:
                return render_template('login.html', error='Wrong username or password.')

        except Exception as e:
            return render_template('login.html', error=f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('login.html')

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'admin' not in session:
        return redirect('/')

    error, success = None, None

    if request.method == 'POST':
        jina = request.form.get('jina')
        thamani = request.form.get('thamani')
        idadi = request.form.get('idadi')
        added_by = session['admin']
        added_at = datetime.now()

        if not jina or not thamani or not idadi:
            error = "Please fill in all fields."
        else:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO products (jina, thamani, idadi, added_by, added_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (jina, float(thamani), int(idadi), added_by, added_at))
                conn.commit()
                success = "Product added successfully."
            except Exception as e:
                error = f"Database error: {e}"
            finally:
                cursor.close()
                conn.close()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT jina, thamani, idadi, added_by, added_at
            FROM products
            ORDER BY added_at DESC
        """)
        rows = cursor.fetchall()

        products = [
            {
                'jina': r[0],
                'thamani': r[1],
                'idadi': r[2],
                'added_by': r[3],
                'added_at': r[4].strftime("%Y-%m-%d %H:%M:%S")
            } for r in rows
        ]

    except Exception as e:
        error = f"Error loading products: {e}"
        products = []
    finally:
        cursor.close()
        conn.close()

    return render_template('add_product.html', error=error, success=success, products=products)

@app.route('/information')
def information():
    if 'admin' not in session:
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT jina, thamani, idadi, added_by, added_at
            FROM products
            ORDER BY added_at DESC
        """)
        rows = cursor.fetchall()

        products = [
            {
                'jina': r[0],
                'thamani': r[1],
                'idadi': r[2],
                'added_by': r[3],
                'added_at': r[4].strftime("%Y-%m-%d %H:%M:%S")
            } for r in rows
        ]

        cursor.execute("SELECT SUM(thamani) FROM products")
        total = cursor.fetchone()[0]
        total_thamani = total if total else 0.0

        return render_template('information.html', products=products, total_thamani=total_thamani)

    except Exception as e:
        return render_template('information.html', products=[], total_thamani=0, error=f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/restricted')
def restricted():
    if 'admin' not in session:
        return redirect('/')
    return render_template('restricted.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
