Documentation du Projet de Bibliothèque XML
1. Présentation Générale
Ce projet est une application de gestion d’une bibliothèque basée sur un système de fichiers XML. Il combine deux interfaces distinctes et complémentaires :
•	Une interface graphique web (HTML/CSS/JS) qui permet une visualisation interactive et esthétique des données.
•	Une interface console Python qui permet une gestion complète des données de la bibliothèque en mode texte.
Toutes les données sont centralisées dans un fichier XML unique appelé bibliotheque.xml. Celui-ci regroupe les informations relatives aux livres, aux utilisateurs de la bibliothèque ainsi qu’à leurs prêts.

2. Fonctionnalités
 Interface Web (index.html)
L’interface web est conçue pour une consultation conviviale des données XML. Elle permet d’afficher en lecture seule :
•	La liste détaillée des livres disponibles dans la bibliothèque, accompagnée des informations telles que le titre, l’auteur, le genre et l’année de publication.
•	La liste des utilisateurs inscrits dans le système, avec leur identifiant, nom et prénom si disponible.
•	L’historique des prêts effectués avec les dates de prêt et de retour, en reliant les identifiants aux noms réels des livres et des utilisateurs.
Cette interface s’appuie sur JavaScript pour charger et parser dynamiquement le contenu XML via la méthode fetch et l’objet DOMParser, ce qui permet de mettre à jour automatiquement les données affichées sans rafraîchissement manuel.

Interface Console Python (gestion.py)
L’interface Python propose une gestion complète des éléments de la bibliothèque via un système de menus intuitifs :
Gestion des Livres
•	Création de nouveaux livres avec génération manuelle d’identifiants.
•	Affichage en console de la liste des livres enregistrés.
•	Modification de n’importe quelle information d’un livre.
•	Suppression d’un livre par son identifiant.
•	Moteur de recherche par auteur, genre ou titre pour retrouver rapidement un ouvrage.
Gestion des Utilisateurs
•	Ajout de nouveaux utilisateurs avec nom et prénom (facultatif).
•	Liste des utilisateurs avec gestion des champs manquants.
•	Modification des informations personnelles.
•	Suppression d’utilisateurs du fichier XML.
 Gestion des Prêts
•	Création d’un prêt avec vérification de disponibilité.
•	Affichage des prêts actifs ou passés avec statut (retourné ou non).
•	Mise à jour de la date de retour (fonction “retourner un livre”).
•	Suppression d’un enregistrement de prêt.
•	Recherche des prêts effectués après une certaine date.

3. Structure du Fichier XML (bibliotheque.xml)
Ce fichier centralise toutes les données relatives à la bibliothèque dans une structure hiérarchique XML bien définie :
<bibliotheque>
  <livres>
    <livre id="L1">
      <titre>1984</titre>
      <auteur>George Orwell</auteur>
      <genre>Science-Fiction</genre>
      <annee>1949</annee>
    </livre>
    ...
  </livres>
  <utilisateurs>
    <utilisateur id="U1">
      <prenom>Jean</prenom>
      <nom>Dupont</nom>
    </utilisateur>
    ...
  </utilisateurs>
  <prets>
    <pret id="P1">
      <id_utilisateur>U1</id_utilisateur>
      <id_livre>L1</id_livre>
      <date_pret>2025-06-20</date_pret>
      <date_retour>2025-07-05</date_retour>
    </pret>
    ...
  </prets>
</bibliotheque>
Chaque balise enfant est clairement identifiée et structurée, facilitant ainsi la lecture et le traitement automatique.

4. Détails Techniques
a. Technologies Utilisées
Élément	Technologie
Données	XML
Traitement	Python (xml.etree)
Interface Web	HTML5 + CSS + JS
Affichage Web	Tableaux dynamiques JS
Interface Console	Menus via input()

b. Organisation des Fichiers
Fichier	Rôle
index.html	Interface graphique web, chargement du XML
gestion.py	Script Python pour gestion CRUD XML
bibliotheque.xml	Fichier de données central (livres, utilisateurs, prêts)
requetes.xq	(optionnel) Script XQuery pour requêtes avancées

c. Sécurité & Validations
Le projet inclut plusieurs mécanismes de validation :
•	Le script Python empêche les doublons grâce à une vérification de l’unicité des identifiants.
•	Il vérifie que les livres et utilisateurs existent avant d’enregistrer un prêt.
•	Il interdit les prêts multiples pour un livre déjà emprunté et non retourné.
•	La fonction retourner_livre() évite de modifier un prêt déjà clôturé.
•	Chaque modification est sauvegardée immédiatement via tree.write(...).

d. Limites actuelles
•	Le fichier XML n’est pas encore validé par un XSD (schéma).
•	Le script JS ne prévoit pas de traitement d’erreur si le fichier XML est absent.
•	Il n’y a pas encore de système de journalisation ou d’historique des opérations.

5. Instructions d’Utilisation
 Lancer l’interface web :
1.	Placer les fichiers index.html et bibliotheque.xml dans le même dossier.
2.	Ouvrir index.html dans votre navigateur préféré.
Conseil : Pour éviter des erreurs CORS, utiliser un petit serveur local (ex. Python http.server).
 Lancer le gestionnaire Python :
python gestion.py
Suivez les menus pour ajouter, modifier ou consulter les données.

6. Capture d’écran (exemple les livres)
Ajouter un livre
 <img width="980" height="290" alt="image" src="https://github.com/user-attachments/assets/a32014c0-63f7-48e6-8697-1bf0ce2b6414" />

 
Lister les livres

<img width="980" height="308" alt="image" src="https://github.com/user-attachments/assets/42e06e64-f612-40f4-9805-23898619e476" />

 
Recherche de livre par autre

<img width="980" height="265" alt="image" src="https://github.com/user-attachments/assets/b6e9265b-0b2e-4433-81a6-b5a736dc8d89" />

 
7. Suggestions d’Améliorations Futures
Idée	Description
Export PDF	Générer un rapport PDF des livres/prêts
Authentification	Ajouter un système de login admin
Validation XSD	Vérifier que le fichier XML respecte un schéma
Interface Web enrichie	Ajouter formulaires HTML pour ajouter/modifier les données
Sauvegarde JSON	Ajouter export/import JSON
Recherche avancée	Intégrer XQuery/XPath pour filtrage multi-critères
Statistiques	Afficher stats : livres les plus empruntés, utilisateurs actifs


