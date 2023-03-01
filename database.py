import sqlite3

class Database:
    def __init__(self):
        self.connection = None

    titre, identifiant, auteur, date_publication, paragraphe = row

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

    def insert_article(titre, identifiant, auteur, date_publication, paragraphe):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(("insert into article(titre, identifiant, auteur, date_publication, paragraphe)"
                        "values(?, ?, ?, ?, ?)"), (titre, identifiant, auteur, date_publication, paragraphe))
        connection.commit()