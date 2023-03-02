from flask import Flask
from flask import g
from flask import render_template
from flask import request
from flask import redirect, url_for
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
    posts = get_db().get_last_five_posts()
    return render_template('accueil.html', title="Publications", posts=posts)

# Route pour la recherche
@app.route('/search')
def search():
    query = request.args.get('query')
    results = get_db().search(query)
    return render_template('search.html', query=query, results=results)


@app.route('/article/<identifiant>')
def article(identifiant):
    article = get_db().get_article_by_id(identifiant) 
    if not article:
        return render_template('404.html'), 404
    return render_template('article.html', article=article)

@app.route('/admin')
def admin():
    articles = get_db().get_all_articles()
    return render_template('admin.html', articles=articles)

@app.route('/admin/modifier/<identifiant>', methods=['GET', 'POST'])
def modifier(identifiant):
    identifiants = get_db().get_all_articles_id()
    if identifiant not in identifiants:
        return render_template('404.html'), 404

    article = get_db().get_article_by_id(identifiant)
    if request.method == 'POST':
        new_titre = request.form.get('titre')
        new_paragraphe = request.form.get('paragraphe')

        get_db().update_title(new_titre,identifiant)
        get_db().update_content(new_paragraphe,identifiant)

        # Rediriger l'utilisateur vers la page d'administration après modification
        return redirect('/admin')

    # Rendre le template HTML en passant l'article à modifier
    return render_template('modification.html', article=article)

@app.route('/admin-nouveau', methods=['GET', 'POST'])
def creer_article():
    if request.method == 'POST':
        titre = request.form.get('titre')
        paragraphe = request.form.get('paragraphe')
        date_publication = datetime.datetime.now()
        
        nouvel_article = Article(titre=titre, paragraphe=paragraphe, date_publication=date_publication)
        get_db().session.add(nouvel_article)
        get_db().session.commit()
        
        # Rediriger vers la page d'accueil
        return redirect('/')
    
    # Si la requête est de type GET, afficher le formulaire de création d'article
    return render_template('creation.html')


if __name__ == '__main__':
    app.run(debug=True)