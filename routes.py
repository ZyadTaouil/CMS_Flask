from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index(): 
    title= "Publications"
    return render_template('login.html', title=title)

@app.route('/form', methods=["POST"])
def form():
    age = request.form['age']
    genre = request.form['genre']
    nom = request.form['nom']
    return render_template('form.html',title="Merci", age=age, genre=genre, nom=nom)