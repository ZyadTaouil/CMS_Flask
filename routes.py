from flask import Flask, render_template, request, g
from .database import Database

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()

@app.route('/')
def index(): 
    title= "Publications"
    return render_template('accueil.html', title=title)

@app.route('/form', methods=["POST"])
def form():
    age = request.form['age']
    genre = request.form['genre']
    nom = request.form['nom']
    return render_template('form.html',title="Merci", age=age, genre=genre, nom=nom)