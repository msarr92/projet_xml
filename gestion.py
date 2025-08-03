import xml.etree.ElementTree as ET
from datetime import date

tree = ET.parse("bibliotheque.xml")
root = tree.getroot()

### LIVRES ###
def ajouter_livre():
    id = input("ID du livre : ")
    if root.find(f"./livres/livre[@id='{id}']") is not None:
        print("Un livre avec cet ID existe déjà.")
        return
    titre = input("Titre : ")
    auteur = input("Auteur : ")
    genre = input("Genre : ")
    annee = input("Année : ")

    livres = root.find("livres")
    livre = ET.SubElement(livres, "livre", id=id)
    ET.SubElement(livre, "titre").text = titre
    ET.SubElement(livre, "auteur").text = auteur
    ET.SubElement(livre, "genre").text = genre
    ET.SubElement(livre, "annee").text = annee
    sauvegarder()
    print(f"✅ Livre '{titre}' ajouté.")

def lister_livres():
    print("\n📚 Liste des livres :")
    for livre in root.findall("./livres/livre"):
        print(f"- {livre.attrib['id']}: {livre.find('titre').text} ({livre.find('auteur').text})")

def supprimer_livre():
    id = input("ID du livre à supprimer : ")
    livres = root.find("livres")
    for livre in livres.findall("livre"):
        if livre.attrib["id"] == id:
            livres.remove(livre)
            sauvegarder()
            print("✅ Livre supprimé.")
            return
    print("❌ Livre non trouvé.")

def modifier_livre():
    id = input("ID du livre à modifier : ")
    livre = root.find(f"./livres/livre[@id='{id}']")
    if livre is not None:
        livre.find("titre").text = input("Nouveau titre : ")
        livre.find("auteur").text = input("Nouvel auteur : ")
        livre.find("genre").text = input("Nouveau genre : ")
        livre.find("annee").text = input("Nouvelle année : ")
        sauvegarder()
        print("✅ Livre modifié.")
    else:
        print("❌ Livre non trouvé.")

### UTILISATEURS ###
def ajouter_utilisateur():
    id = input("ID utilisateur : ")
    if root.find(f"./utilisateurs/utilisateur[@id='{id}']") is not None:
        print("❌ Un utilisateur avec cet ID existe déjà.")
        return
    nom = input("Nom : ")
    prenom = input("Prénom : ")

    utilisateurs = root.find("utilisateurs")
    utilisateur = ET.SubElement(utilisateurs, "utilisateur", id=id)
    ET.SubElement(utilisateur, "nom").text = nom
    ET.SubElement(utilisateur, "prenom").text = prenom
    sauvegarder()
    print(f"✅ Utilisateur '{prenom} {nom}' ajouté.")

def lister_utilisateurs():
    print("\n👤 Liste des utilisateurs :")
    for utilisateur in root.findall("./utilisateurs/utilisateur"):
        id_utilisateur = utilisateur.attrib.get('id', '??')
        prenom_elt = utilisateur.find('prenom')
        nom_elt = utilisateur.find('nom')

        prenom = prenom_elt.text if prenom_elt is not None else "(Prénom manquant)"
        nom = nom_elt.text if nom_elt is not None else "(Nom manquant)"

        print(f"- {id_utilisateur}: {prenom} {nom}")

def supprimer_utilisateur():
    id = input("ID utilisateur à supprimer : ")
    utilisateurs = root.find("utilisateurs")
    for utilisateur in utilisateurs.findall("utilisateur"):
        if utilisateur.attrib["id"] == id:
            utilisateurs.remove(utilisateur)
            sauvegarder()
            print("✅ Utilisateur supprimé.")
            return
    print("❌ Utilisateur non trouvé.")

def modifier_utilisateur():
    id = input("ID utilisateur à modifier : ")
    utilisateur = root.find(f"./utilisateurs/utilisateur[@id='{id}']")
    if utilisateur is not None:
        utilisateur.find("nom").text = input("Nouveau nom : ")
        utilisateur.find("prenom").text = input("Nouveau prénom : ")
        sauvegarder()
        print("✅ Utilisateur modifié.")
    else:
        print("❌ Utilisateur non trouvé.")

### PRETS ###

def generer_id_pret():
    prets = root.findall("./prets/pret")
    if not prets:
        return "p1"
    derniers_ids = [int(pret.attrib.get("id", "p0")[1:]) for pret in prets if pret.attrib.get("id", "").startswith("p")]
    max_id = max(derniers_ids) if derniers_ids else 0
    return f"p{max_id + 1}"



def ajouter_pret():
    id_livre = input("ID du livre : ")
    id_utilisateur = input("ID de l'utilisateur : ")
    date_pret = input("Date du prêt (YYYY-MM-DD, vide pour aujourd’hui) : ") or date.today().isoformat()

    # Vérifier que le livre existe
    if root.find(f"./livres/livre[@id='{id_livre}']") is None:
        print("❌ Livre introuvable.")
        return
    # Vérifier que l'utilisateur existe
    if root.find(f"./utilisateurs/utilisateur[@id='{id_utilisateur}']") is None:
        print("❌ Utilisateur introuvable.")
        return
    # Vérifier si le livre est déjà prêté et non retourné
    prets = root.findall(f"./prets/pret[id_livre='{id_livre}']")
    prets_actifs = [pret for pret in prets if pret.find('date_retour') is None or not pret.find('date_retour').text or pret.find('date_retour').text.strip() == '']
    if prets_actifs:
        print("❌ Ce livre est déjà prêté et non retourné.")
        return

    id_pret = generer_id_pret()

    prets = root.find("prets")
    pret = ET.SubElement(prets, "pret", id=id_pret)
    ET.SubElement(pret, "id_livre").text = id_livre
    ET.SubElement(pret, "id_utilisateur").text = id_utilisateur
    ET.SubElement(pret, "date_pret").text = date_pret
    ET.SubElement(pret, "date_retour").text = ""  # vide au début
    sauvegarder()
    print(f"✅ Prêt enregistré avec ID : {id_pret}.")


def lister_prets():
    tree = ET.parse("bibliotheque.xml")
    root = tree.getroot()

    print("\n📚 Liste détaillée des prêts :")

    for pret in root.findall("./prets/pret"):
        id_pret = pret.attrib.get("id", "(ID manquant)")
        id_livre = pret.find("id_livre").text
        id_user = pret.find("id_utilisateur").text
        date_pret = pret.find("date_pret").text
        date_retour = pret.find("date_retour").text

        livre = root.find(f"./livres/livre[@id='{id_livre}']")
        user = root.find(f"./utilisateurs/utilisateur[@id='{id_user}']")

        titre_livre = livre.find("titre").text if livre is not None and livre.find("titre") is not None else f"(ID: {id_livre})"
        if user is not None:
            prenom = user.find("prenom").text if user.find("prenom") is not None else ""
            nom = user.find("nom").text if user.find("nom") is not None else ""
            nom_user = f"{prenom} {nom}".strip()
        else:
            nom_user = f"(ID: {id_user})"

        print(f"- Prêt {id_pret} | Livre : {titre_livre} | Utilisateur : {nom_user} | Date Prêt : {date_pret} | Date Retour : {date_retour or 'non retourné'}")

    print("\n📦 Statut des prêts :")
    for pret in root.findall("./prets/pret"):
        id_pret = pret.attrib.get("id", "(ID manquant)")
        id_livre = pret.find("id_livre").text
        id_user = pret.find("id_utilisateur").text
        date_pret = pret.find("date_pret").text
        date_retour = pret.find("date_retour").text

        livre = root.find(f"./livres/livre[@id='{id_livre}']")
        titre_livre = livre.find("titre").text if livre is not None and livre.find("titre") is not None else f"(ID: {id_livre})"

        user = root.find(f"./utilisateurs/utilisateur[@id='{id_user}']")
        if user is not None:
            prenom = user.find("prenom").text if user.find("prenom") is not None else ""
            nom = user.find("nom").text if user.find("nom") is not None else ""
            nom_user = f"{prenom} {nom}".strip()
        else:
            nom_user = f"(ID: {id_user})"

        etat = "✅ retourné" if date_retour and date_retour.strip() else "📌 en prêt"
        print(f"- [{id_pret}] {titre_livre} prêté à {nom_user} le {date_pret} [{etat}]")



def retourner_livre():
    tree = ET.parse("bibliotheque.xml")
    root = tree.getroot()

    id_livre = input("ID du livre retourné : ")
    id_user = input("ID de l'utilisateur : ")
    date_retour = input("Date de retour (YYYY-MM-DD, vide pour aujourd’hui) : ") or date.today().isoformat()

    for pret in root.findall("./prets/pret"):
        livre_elt = pret.find("id_livre")
        user_elt = pret.find("id_utilisateur")
        retour_elt = pret.find("date_retour")

        if livre_elt is not None and user_elt is not None and livre_elt.text == id_livre and user_elt.text == id_user:
            if retour_elt is not None and retour_elt.text and retour_elt.text.strip():
                print("❌ Ce livre a déjà été retourné.")
                return
            elif retour_elt is not None:
                retour_elt.text = date_retour
            else:
                # Si la balise <date_retour> n’existe pas du tout, on la crée
                ET.SubElement(pret, "date_retour").text = date_retour

            tree.write("bibliotheque.xml", encoding="utf-8", xml_declaration=True)
            print("✅ Date de retour mise à jour.")
            return

    print("❌ Prêt non trouvé.")



def supprimer_pret():
    id_livre = input("ID du livre à annuler : ")
    id_user = input("ID de l'utilisateur : ")
    prets = root.find("prets")
    for pret in prets.findall("pret"):
        if pret.find("id_livre").text == id_livre and pret.find("id_utilisateur").text == id_user:
            prets.remove(pret)
            sauvegarder()
            print("✅ Prêt supprimé.")
            return
    print("❌ Prêt non trouvé.")

### SAUVEGARDE ###
def sauvegarder():
    tree.write("bibliotheque.xml", encoding="utf-8", xml_declaration=True)

### MENUS ###
def menu():
    while True:
        print("\n📚 MENU PRINCIPAL")
        print("1. Gérer les livres")
        print("2. Gérer les utilisateurs")
        print("3. Gérer les prêts")
        print("0. Quitter")
        choix = input("Choix : ")

        if choix == "1":
            menu_livres()
        elif choix == "2":
            menu_utilisateurs()
        elif choix == "3":
            menu_prets()
        elif choix == "0":
            break
        else:
            print("❌ Choix invalide")

def menu_livres():
    while True:
        print("\n📘 GESTION DES LIVRES")
        print("1. Ajouter un livre")
        print("2. Lister les livres")
        print("3. Modifier un livre")
        print("4. Supprimer un livre")
        print("0. Retour")
        choix = input("Choix : ")

        if choix == "1":
            ajouter_livre()
        elif choix == "2":
            lister_livres()
        elif choix == "3":
            modifier_livre()
        elif choix == "4":
            supprimer_livre()
        elif choix == "0":
            break

def menu_utilisateurs():
    while True:
        print("\n👥 GESTION DES UTILISATEURS")
        print("1. Ajouter un utilisateur")
        print("2. Lister les utilisateurs")
        print("3. Modifier un utilisateur")
        print("4. Supprimer un utilisateur")
        print("0. Retour")
        choix = input("Choix : ")

        if choix == "1":
            ajouter_utilisateur()
        elif choix == "2":
            lister_utilisateurs()
        elif choix == "3":
            modifier_utilisateur()
        elif choix == "4":
            supprimer_utilisateur()
        elif choix == "0":
            break

def menu_prets():
    while True:
        print("\n📦 GESTION DES PRÊTS")
        print("1. Ajouter un prêt")
        print("2. Lister les prêts")
        print("3. Retourner un livre (mise à jour date retour)")
        print("4. Supprimer un prêt")
        print("0. Retour")
        choix = input("Choix : ")

        if choix == "1":
            ajouter_pret()
        elif choix == "2":
            lister_prets()
        elif choix == "3":
            retourner_livre()
        elif choix == "4":
            supprimer_pret()
        elif choix == "0":
            break

if __name__ == "__main__":
    menu()
