import re
import numpy as np

##DEFINITION OF A DOCUMENT BY HIS CLASS
class Document :

    identifiant = 0
    titre =  ""
    auteur = ""
    resume = ""

    def __init__(self, identifiant) :
        self.identifiant = identifiant

class Requete :

    identifiant = 0
    contenu = ""

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


#cette fonction construit un vocab pour un document
def vocabular_of_the_document(element, doc, vocab, is_principal_vocab = False) :
    
    position = 0
    for word in get_words_from_string(getattr(doc, element)):
        if word in vocab :
            if is_principal_vocab == False :
                vocab[word] = vocab[word]+1
        else:
            if is_principal_vocab :
                vocab[word] = position
                position += 1
            else :
                vocab[word] = 1
    
    return vocab

#cette fonction construit un vocabulaire en fonction de l'élement constitutif d'une document (titre , resume...)
#Creation du vocabulaire : enregistrement de tous les mots differents dans le dictionnaire vocab avec leur nombre d occurences
def vocabular_of_the_element(element, documents_list, vocab) :
    
    for doc in documents_list:
        vocab = vocabular_of_the_document(element, doc, vocab , True)
    
    return vocab

# Retourne la similarité consine entre le vect_a et vect_b
def cosine_similarity(vect_a, vect_b):
    return np.dot(vect_a, vect_b) / np.linalg.norm(vect_a)*np.linalg.norm(vect_b)

"""----------------------------------------------------------------------------------------------------------------
                                            CODE PRINCIPAL
-------------------------------------------------------------------------------------------------------------"""

liste_de_documents_et_caracteristiques = open("CISI\CISI.ALL" , "r" , encoding="utf-8")

point = "."
grandI = "I"
grandT = "T"
grandA = "A"
grandW = "W"

documents_list = []
 
## Parcours du fichier
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




vocab = {}
#vocab = vocabular_of_the_element("titre", documents_list, vocab)
vocab = vocabular_of_the_element("resume", documents_list, vocab)
vocab_size = len(vocab)

## CONSTRUCTION DES VECTEURS DE DOCUMENTS
documents_index = {}
for doc in documents_list :
    vocab_doc = vocabular_of_the_document("resume", doc, {})
    vector_doc = np.zeros(vocab_size)

    for word in vocab_doc :
        vector_doc[vocab[word]] = vocab_doc[word]
    
    documents_index[doc.identifiant] = vector_doc




##FONCTION DE LECTURE DU CONTENU DE FICHIER DES REQUETES

fichier_requetes = open("CISI\CISI.QRY" , "r" , encoding="utf-8")

requete_list = []
 
## Parcours du fichier des requêtes
while True :
    line = fichier_requetes.readline()

    if not line :
        break
    if line[0] == point:

        ## Lecture de l'identifiant
        if line[1] == grandI :
            identifiant = line[3:].strip()
            requete = Requete(identifiant)
            requete_list.append(requete)

        ## Lecture du contenu
        elif line[1] == grandW :
            requete.contenu = read_paragraph(fichier_requetes)

#for requete in requete_list:
#    print ( f"{requete.identifiant} : {requete.contenu}")
requete_vectors = {}
for req in requete_list:
    vocab_requete = vocabular_of_the_document("contenu", req, {})
    vector_req = np.zeros(vocab_size)

    for word in vocab_requete :
        # Si le mot de la requête est présent dans le vocab
        if word in vocab :
            vector_req[vocab[word]] = vocab_requete[word]
        # Sinon : à faire plus tard
    
    requete_vectors[req.identifiant] = vector_req


## RECHERCHE 

req_vector = requete_vectors['1']

results = {}

for doc_id in documents_index:
    #print(doc_vector_key)
    results[doc_id] = cosine_similarity(req_vector, documents_index[doc_id])

# trier par ordre décroissant

#print(vocab)
#print(len(vocab))
