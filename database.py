import sqlite3

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/article.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_titre(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select titre from article")
        titres = cursor.fetchall()
        return [titre[0] for titre in titres]

    def get_auteur(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select auteur from article")
        auteurs = cursor.fetchall()
        return [auteur[0] for auteur in auteurs]

    def get_article_by_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article where identifiant = ? ", (id,))
        article = cursor.fetchone() 
        return article

    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article")
        articles = cursor.fetchall() 
        return articles

    def get_all_articles_id(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select identifiant from article")
        articles = cursor.fetchall()
        new_articles = [article[0] for article in articles] 
        return new_articles


    def get_last_five_posts(self):
        cursor = self.get_connection().cursor()
        cursor.execute("select * from article Where date_publication = DATE('now','localtime') ORDER BY date_publication DESC LIMIT 5")
        publications = cursor.fetchall()
        return publications

    def delete_insertions(self):
        cursor = self.get_connection().cursor()
        cursor.execute("delete * from article")

    def search(self, query):
        cursor = self.get_connection().cursor()
        # Sélectionne les publications contenant la chaîne de recherche
        cursor.execute("SELECT titre, date_publication, identifiant FROM article WHERE (titre LIKE ? OR paragraphe LIKE ?) AND date_publication <= date('now')", 
            ('%' + query + '%', '%' + query + '%'))
        resultats = cursor.fetchall()
        return resultats

    def insert_article(self, titre, identifiant, auteur, date_publication, paragraphe):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into article(titre, identifiant, auteur, date_publication, paragraphe)"
                        "values(?, ?, ?, ?, ?)"), (titre, identifiant, auteur, date_publication, paragraphe))
        connection.commit()

    def update_title(self,id,title):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update article SET titre = ? WHERE identifiant=?", (title,id))
        connection.commit()

    def update_content(self,id,content):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("update article SET paragraphe = ? WHERE identifiant=?", (content,id))
        connection.commit()