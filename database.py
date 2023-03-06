import sqlite3


# gère l'accès à la BDD
class Database:

    def __init__(self):
        self.connection = None

    # connexion à la bdd
    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/article.db')
        return self.connection

    # déconexion de la bdd
    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # retourne l'article avec l'id donnée en paramètre
    def get_article_by_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where identifiant = ? ", (id,))
        article = cursor.fetchone()
        return article

    # retourne tout les articles de la BDD
    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article")
        articles = cursor.fetchall()
        return articles

    # retourne l'id de tout les articles
    def get_all_articles_id(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select identifiant from article")
        articles = cursor.fetchall()
        new_articles = [article[0] for article in articles]
        return new_articles

    # retourne les 5 derniers articles publiés
    # pour retourner les 5 derniers articles publiés 
    # à la date d'aujourd'hui, il suffit de
    # remplacer date_publication <= DATE('now','localtime') "
    # par date_publication = DATE('now','localtime') "
    def get_last_five_posts(self):
        cursor = self.get_connection().cursor()
        cursor.execute(
            "select * from article Where date_publication <= "
            "DATE('now','localtime') "
            "ORDER BY date_publication DESC LIMIT 5")
        publications = cursor.fetchall()
        return publications

    # fonction simulant un moteur de recherche
    def search(self, query):
        cursor = self.get_connection().cursor()
        # Sélectionne les publications contenant la chaîne de recherche
        # (soit dans letitre ou dans le paragraphe)
        cursor.execute(
            "SELECT titre, date_publication, identifiant FROM article WHERE "
            "(titre LIKE ? OR paragraphe LIKE ?) "
            "AND date_publication <= date('now')",
            ('%' + query + '%', '%' + query + '%'))
        resultats = cursor.fetchall()
        return resultats

    # crée un article selon les données entrées
    def create_article(self, titre, identifiant, auteur, date_publication,
                       paragraphe):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into article(titre, identifiant, auteur, "
                        "date_publication, paragraphe)"
                        "values(?, ?, ?, ?, ?)"),
                       (titre, identifiant, auteur, date_publication,
                        paragraphe))
        connection.commit()

    # modifie le titre
    def update_title(self, id, title):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update article SET titre = ? WHERE identifiant=?",
                       (title, id))
        connection.commit()

    # modifie le paragraphe
    def update_content(self, id, content):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update article SET paragraphe = ? WHERE identifiant=?",
                       (content, id))
        connection.commit()
