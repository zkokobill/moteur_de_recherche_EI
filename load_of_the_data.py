#import re
import entity as en
import utils as ut
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS


#nlp = spacy.load("en_core_web_sm")


nlp = spacy.load("en_core_web_sm", exclude = ["attribute_ruler" , \
                                                "tok2vec","parser","senter","ner"])


#nlp = spacy.load("fr_dep_news_trf")

# Retourne la similarité cosine entre le vect_a et vect_b
def cosine_similarity(vect_a, vect_b):
    return np.dot(vect_a, vect_b) / (np.linalg.norm(vect_a)*np.linalg.norm(vect_b))

"""----------------------------------------------------------------------------------------------------------------
                                            CODE PRINCIPAL
------------------------------------------------------------------------------------------------------------- """

liste_de_documents_et_caracteristiques = open("CISI/CISI.ALL" , "r" , encoding="utf-8")

point = "."
grandI = "I"
grandT = "T"
grandA = "A"
grandW = "W"

documents_list = []
 
## PARSING DES DOCUMENTS

while True :
    line = liste_de_documents_et_caracteristiques.readline()
    if not line :
        break

    if line[0] == point:
        ## ON VERIFIE SI ON A UN GRAND I
        if line[1] == grandI :
            identifiant = line[3:].strip()
            # print(identifiant)
            document = en.Document(identifiant)
            documents_list.append(document)
        
        elif line[1] == grandT :
            titre = ut.read_paragraph(liste_de_documents_et_caracteristiques)
            document.titre = titre
        
        elif line[1] == grandA :
            auteur = ut.read_paragraph(liste_de_documents_et_caracteristiques)
            document.auteur = auteur

        elif line[1] == grandW :
            resume = ut.read_paragraph(liste_de_documents_et_caracteristiques)
            document.resume = resume
    


##CONSTRUCTION DU VOCABULAIRE 

vocab = {}
for doc in documents_list :
    # ON TROUVE LES MOTS DE CE DOCUMENT
    vocab_doc, vocab = ut.vocabular_of_a_document("resume", doc, vocab, nlp)
    doc.vocab_resume = vocab_doc


print("Vocab size : ", len(vocab))

vocab_list = list(vocab)

vocab_size = len(vocab)
number_of_documents_with_word = np.zeros(vocab_size)
for doc in documents_list :
    doc.representative_vector = np.zeros(vocab_size)
    for word in doc.vocab_resume :
        # Nombre d'occurences du mots dans le document
        doc.representative_vector[vocab_list.index(word)] = doc.vocab_resume[word]
        # Nombre de documents contenant le mot
        number_of_documents_with_word[vocab_list.index(word)] += 1

# Calcul du TF*IDF
idf_vector = np.ones(vocab_size) * len(documents_list) / number_of_documents_with_word
for doc in documents_list :
    doc.representative_vector = doc.representative_vector / len(doc.vocab_resume)
    doc.representative_vector = doc.representative_vector * idf_vector


##PARSING DU CONTENU DE FICHIER DES REQUETES

fichier_requetes = open("CISI/CISI.QRY" , "r" , encoding="utf-8")

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
            requete = en.Requete(identifiant)
            requete_list.append(requete)

        ## Lecture du contenu
        elif line[1] == grandW :
            requete.contenu = ut.read_paragraph(fichier_requetes)

        elif line[1] == grandA :
            requete.auteur = ut.read_paragraph(fichier_requetes)

        elif line[1] == grandT :
            requete.titre = ut.read_paragraph(fichier_requetes)



requete_vectors = {}
j=0
for req in requete_list:
    vocab_requete = ut.vocabular_of_a_request("contenu", req, {},nlp)
    vocab_requete = ut.vocabular_of_a_request("titre", req, vocab_requete,nlp)
    vocab_requete = ut.vocabular_of_a_request("auteur", req, vocab_requete,nlp)
    vector_req = np.zeros(vocab_size)
    i = 0
    for word in vocab_requete :
        # Si le mot de la requête est présent dans le vocab
        if word in vocab :
            vector_req[vocab_list.index(word)] = vocab_requete[word]

        # Sinon : à faire plus tard
        else :
            i+=1
    
    requete_vectors[req.identifiant] = vector_req

## RECHERCHE 
all_results = {}

for req_id in requete_vectors :
    req_vector = requete_vectors[req_id]
    results = {}

    for doc in documents_list :
        results[documents_list.index(doc)] = cosine_similarity (req_vector , doc.representative_vector)    

    # trier par ordre décroissant
    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse = True))
    
    results_limit = 100
    sorted_results_list = list(sorted_results)[1:results_limit]

    # similarity_seuil = 0.02
    # sorted_results_list = []
    # for result_doc in sorted_results :
    #     if(sorted_results[result_doc] >= similarity_seuil) :
    #         sorted_results_list.append(result_doc)

    all_results[req_id] = sorted_results_list


## ANALYSE DES RESULTATS

# Parsing du fichier de vérification

result_verification_file = open("CISI/CISI.REL" , "r" , encoding="utf-8")

expected_results = {}

while True :
    line = result_verification_file.readline()
    if not line :
        break
    else :
      line_tab = line.split()
      req_id = line_tab[0]
      doc_id = line_tab[1]

      if req_id in expected_results :
        expected_results[req_id] = expected_results[req_id] + [doc_id]
      else :
        expected_results[req_id] = [doc_id]


# Calcul de la précision et du rappel

total_precision = 0
total_rappel = 0

for req_id in expected_results :

    true_positive = 0
    true_positive_and_false_negative = len(expected_results[req_id])
    true_positive_and_false_positive = len(all_results[req_id])

    for doc_id in expected_results[req_id] :
        for doc_id_found in all_results[req_id] :
            if int(doc_id) == int(doc_id_found) :
                true_positive += 1
    
    precision = true_positive / true_positive_and_false_positive
    rappel = true_positive / true_positive_and_false_negative

    total_precision += precision
    total_rappel += rappel

print("Results limit :", results_limit)
# print("Similarity seuil :", similarity_seuil)
print("Mean precision :", total_precision / len(expected_results))
print("Mean rappel :", total_rappel / len(expected_results))