from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Kuunda database na table kama haipo
def init_db():
    conn = sqlite3.connect('jina.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS majina (id INTEGER PRIMARY KEY AUTOINCREMENT, jina TEXT NOT NULL)')
    conn.commit()
    conn.close()

init_db()

# Route ya kuonyesha form na kupokea jina
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        jina = request.form.get('jina')
        if jina:
            conn = sqlite3.connect('jina.db')
            c = conn.cursor()
            c.execute('INSERT INTO majina (jina) VALUES (?)', (jina,))
            conn.commit()
            conn.close()
            message = f'Jina "{jina}" limehifadhiwa kikamilifu!'
        else:
            message = 'Tafadhali ingiza jina.'
    
    form_html = '''
    <html>
    <head>
      <title>Ingiza Jina</title>
      <style>
        body {
          background-color: #f0f0f0;
          font-family: Arial, sans-serif;
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
        }
        .container {
          background-color: white;
          padding: 40px;
          border-radius: 12px;
          box-shadow: 0 0 10px rgba(0,0,0,0.1);
          text-align: center;
        }
        input[type="text"] {
          padding: 10px;
          width: 250px;
          font-size: 16px;
          margin-bottom: 15px;
        }
        button {
          padding: 10px 20px;
          font-size: 16px;
          background-color: gray;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
        }
        button:hover {
          background-color: darkgray;
        }
        p {
          margin-top: 20px;
          color: green;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <h2>Ingiza Jina</h2>
        <form method="POST">
          <input type="text" name="jina" placeholder="Andika jina hapa" required><br>
          <button type="submit">Hifadhi</button>
        </form>
        <p>{{ message }}</p>
      </div>
    </body>
    </html>
    '''

    return render_template_string(form_html, message=message)

if __name__ == '__main__':
    app.run(debug=True)
