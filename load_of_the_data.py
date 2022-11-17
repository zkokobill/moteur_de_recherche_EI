import re

##DEFINITION OF A DOCUMENT BY HIS CLASS
class Document :

    identifiant = 0
    titre =  ""
    auteur = ""
    resume = ""

    def __init__(self, identifiant) :
        self.identifiant = identifiant

##THIS FILE IS CONTAINING THE LOADING OF THE DATAS
## WE LOAD IT AND CLASSIFY THEN IN THEIR GREAT VALUES

def read_paragraph(file) :
    paragraph = ""
    last_pos = file.tell()
    while True:
        ## On sauvegarde la position sur le fichier avant de lire la ligne suivante
        last_pos = file.tell()
        line = file.readline()
        if line[0] == ".":
            ## Si on a atteind le champ suivant on revient a la ligne precedente
            file = file.seek(last_pos)
            break
        paragraph += line.strip()

    return paragraph

# Afficher chaque document contenu dans la liste documents (liste d objets de la classe Document)
def print_all_docs(documents):
    for doc in documents_list:
        print("id:"+doc.identifiant)
        print("titre:"+doc.titre)
        print("auteur:"+doc.auteur)
        print("resume:"+doc.resume)


## Renvoie une liste des mots contenus dans une string, separes par un espace ou un caractere special
def get_words_from_string(input_string):
    word_list=re.split(" |:|,|\.|\?|!|\(|\)|\"|-",input_string);    
    return word_list

liste_de_documents_et_caracteristiques = open("CISI\CISI.ALL" , "r" , encoding="utf-8")

point = "."
grandI = "I"
grandT = "T"
grandA = "A"
grandW = "W"

documents_list = []
 
## FICHIER
while True :
    line = liste_de_documents_et_caracteristiques.readline()

    if not line :
        break
    if line[0] == point:

        ## ON VERIFIE SI ON A UN GRAND I
        if line[1] == grandI :
            identifiant = line[3:].strip()
            document = Document(identifiant)
            documents_list.append(document)
        
        elif line[1] == grandT :
            titre = read_paragraph(liste_de_documents_et_caracteristiques)
            document.titre = titre
        
        elif line[1] == grandA :
            auteur = read_paragraph(liste_de_documents_et_caracteristiques)
            document.auteur = auteur

        elif line[1] == grandW :
            resume = read_paragraph(liste_de_documents_et_caracteristiques)
            document.resume = resume

#print_all_docs(documents_list)

## Creation du vocabulaire : enregistrement de tous les mots differents dans le dictionnaire vocab avec leur nombre d occurences
vocab = {}
position = 0
for doc in documents_list:
    for word in get_words_from_string(doc.titre):
        if word in vocab :
            vocab[word] = vocab[word]+1
        else:
            vocab[word] = 1

print(vocab)
