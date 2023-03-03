from flask import Flask
from flask import g
from flask import redirect
from flask import render_template
from flask import request

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


# route pour la modification d'un article
@app.route('/admin/modifier/<identifiant>', methods=['GET', 'POST'])
def modifier_article(identifiant):
    identifiants = get_db().get_all_articles_id()
    if identifiant not in identifiants:
        return render_template('404.html'), 404

    article = get_db().get_article_by_id(identifiant)
    if request.method == 'POST':
        new_titre = request.form.get('title')
        new_paragraphe = request.form.get('content')

        get_db().update_title(identifiant, new_titre)
        get_db().update_content(identifiant, new_paragraphe)

        return redirect('/admin')

    return render_template('modification.html', article=article)


@app.route('/admin-nouveau', methods=['GET', 'POST'])
def creer_article():
    if request.method == 'POST':
        titre = request.form.get('titre')
        identifiant = request.form.get('identifiant')
        auteur = request.form.get('auteur')
        paragraphe = request.form.get('paragraphe')
        date = request.form.get('date_publication')
        get_db().create_article(titre, identifiant, auteur, date, paragraphe)

        return redirect('/')

    return render_template('creation.html')


if __name__ == '__main__':
    app.run(debug=True)
