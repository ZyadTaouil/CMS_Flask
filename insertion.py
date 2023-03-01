from flask import g
from .database import Database

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


get_db().insert_article("Apple","D2190","Steve Jobs","01/03/2023","Apple Inc. [ˈæpəl] est une entreprise multinationale américaine qui crée et commercialise des produits électroniques grand public, des ordinateurs personnels et des logiciels.")
get_db().insert_article("Samsung","S2413","Lee Byung-chul","01/03/2023","Le Groupe Samsung (hangeul : 삼성 ; hanja : 三星 ; RR : Samseong, qui signifie « trois étoiles ») est un des principaux chaebols coréens (conglomérat coréen constitué de différentes sociétés que lient des relations financières complexes).")
get_db().insert_article("Sony","F2982","Kenichiro Yoshida","01/03/2023","Sony Corporation (ソニー株式会社, Sonī kabushiki gaisha?, TYO: 6758, NYSE: SNE), est une société multinationale japonaise basée dans l'arrondissement de Minato à Tokyo (Japon). Elle est active dans différents domaines tels que l'électronique, la téléphonie, l'informatique, le jeu vidéo, la musique, le cinéma et l'audiovisuel en général.")
get_db().insert_article("Ubisoft","E2990","Claude Guillemot","01/03/2023","Ubisoft (anciennement Ubi Soft Entertainment) est une entreprise française de développement, d'édition et de distribution de jeux vidéo, créée en mars 1986 par les cinq frères Guillemot, originaires de Carentoir dans le Morbihan, en France.")
get_db().insert_article("EA Sports","O1019","Trip Hawkins","02/03/2023","EA Sports est une marque de l'entreprise américaine Electronic Arts spécialisée dans les jeux vidéo sportifs. Il s'agit d'un « sous-label » qui sort des séries de jeux telles que NBA Live, FIFA, NHL, Madden NFL ou encore NASCAR. La plupart des jeux sont développés par EA Vancouver situé à Burnaby en Colombie-Britannique.")


