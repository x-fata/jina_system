from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PostgreSQL connection settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jina_db_user:295a2tHLmhTeHFjTI4AxznPHmRMKJptc@dpg-d265eimuk2gs73bhvjcg-a.oregon-postgres.render.com:5432/jina_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Model ya Jina
class Jina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jina = db.Column(db.String(100), nullable=False)

# Kuunda tables
with app.app_context():
    db.create_all()

# Route ya form
@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        jina_input = request.form.get('jina')
        if jina_input:
            jina_obj = Jina(jina=jina_input)
            db.session.add(jina_obj)
            db.session.commit()
            message = f'Jina "{jina_input}" limehifadhiwa kikamilifu!'
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
