
##DEFINITION OF A DOCUMENT BY HIS CLASS
class Document :

    identifiant = 0
    titre =  ""
    auteur = ""
    resume = ""
    vocab_resume = {}
    representative_vector_resume = []

    def __init__(self, identifiant) :
        self.identifiant = identifiant

## DEFINITION OF A REQUEST BY HIS CLASS
class Requete :

    identifiant = 0
    contenu = ""


    def __init__(self, identifiant) :
        self.identifiant = identifiant