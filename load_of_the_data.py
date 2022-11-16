##DEFINITION OF A DOCUMENT BY HIS CLASS
class Document :

    identifiant = 0
    titre =  ""
    auteur = ""
    resume = ""

    def __init__(self, identifiant , titre , auteur , resume) :
        self.identifiant = identifiant
        self.titre = titre
        self.auteur = auteur
        self.resume = resume




##THIS FILE IS CONTAINING THE LOADING OF THE DATAS
## WE LOAD IT AND CLASSIFY THEN IN THEIR GREAT VALUES


def read_paragraph(file) :
    point_de_fin = ""

    while (point_de_fin != "."):
        line = file.readline()
        paragraph += line
        point_de_fin = line[0]

    return paragraph


liste_de_documents_et_caracteristiques = open("CISI\CISI.ALL" , "r" , encoding="utf-8")

point = "."
grandI = "I"
grandT = "T"
 
## FICHIER
while True :
    line = liste_de_documents_et_caracteristiques.readline()
    if not line :
        break
    if line[0] == point:

        ## ON VERIFIE SI ON A UN GRAND I
        if line[1] == grandI :
            identifiant = line[3:].strip()
        
        elif line[1] == grandT :
            titre = read_paragraph(liste_de_documents_et_caracteristiques)

