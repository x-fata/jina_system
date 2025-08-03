from flask import Flask, render_template, request, redirect, session, url_for
import psycopg2
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'bizkazi_secret_key'

# === DATABASE CONNECTION ===
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com",
        port=5432,
        database="jina_db",
        user="jina_db_user",
        password="295a2tHLmhTeHFjTI4AxznPHmRMKJptc"
    )
    return conn

# === LOGIN ROUTE ===
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

            if admin and check_password_hash(admin[2], password):
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

# === PAGE 2 ROUTE ===
@app.route('/page2')
def page2():
    if 'admin' not in session:
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT jina, action, timestamp FROM activities ORDER BY timestamp DESC")
        rows = cursor.fetchall()

        activities = []
        for row in rows:
            activities.append({
                'jina': row[0],
                'action': row[1],
                'timestamp': row[2].strftime("%Y-%m-%d %H:%M:%S"),
            })

    except Exception as e:
        return f"Kuna tatizo: {e}"

    finally:
        cursor.close()
        conn.close()

    return render_template('page2.html', activities=activities)

# === ADD PRODUCT ROUTE ===
@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if 'admin' not in session:
        return redirect('/')

    error = None
    success = None
    products = []

    if request.method == 'POST':
        jina = request.form.get('jina')
        thamani = request.form.get('thamani')
        idadi = request.form.get('idadi')
        added_by = session['admin']
        added_at = datetime.now()

        if not jina or not thamani or not idadi:
            error = "Tafadhali jaza fomu yote ipasavyo."
        else:
            try:
                thamani_float = float(thamani)
                idadi_int = int(idadi)

                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO products (jina, thamani, idadi, added_by, added_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (jina, thamani_float, idadi_int, added_by, added_at))
                conn.commit()
                success = "Bidhaa imeongezwa kikamilifu."
            except Exception as e:
                error = f"Kosa lililotokea: {e}"
            finally:
                cursor.close()
                conn.close()

    # Fetch products - NEWEST FIRST
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT jina, thamani, idadi, added_by, added_at
            FROM products
            ORDER BY added_at DESC
        """)
        rows = cursor.fetchall()

        for row in rows:
            products.append({
                'jina': row[0],
                'thamani': row[1],
                'idadi': row[2],
                'added_by': row[3],
                'added_at': row[4].strftime("%Y-%m-%d %H:%M:%S")
            })
    except Exception as e:
        error = f"Kosa wakati wa kupakua bidhaa: {e}"
    finally:
        cursor.close()
        conn.close()

    return render_template('add_product.html', error=error, success=success, products=products)

# === INFORMATION ROUTE ===
@app.route('/information')
def information():
    if 'admin' not in session:
        return redirect('/')

    error = None
    products = []
    total_thamani = 0.0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT jina, thamani, idadi, added_by, added_at
            FROM products
            ORDER BY added_at DESC
        """)
        rows = cursor.fetchall()

        for row in rows:
            products.append({
                'jina': row[0],
                'thamani': row[1],
                'idadi': row[2],
                'added_by': row[3],
                'added_at': row[4].strftime("%Y-%m-%d %H:%M:%S")
            })

        cursor.execute("SELECT SUM(thamani) FROM products")
        result = cursor.fetchone()
        total_thamani = result[0] if result[0] else 0.0

    except Exception as e:
        error = f"Kosa: {e}"
    finally:
        cursor.close()
        conn.close()

    return render_template('information.html', products=products, total_thamani=total_thamani, error=error)

# === RESTRICTED ROUTE ===
@app.route('/restricted')
def restricted():
    if 'admin' not in session:
        return redirect('/')
    return render_template('restricted.html')

# === RUN APP ===
if __name__ == '__main__':
    app.run(debug=True)
