xquery version "3.1";

declare variable $auteur as xs:string external;
declare variable $genre as xs:string external;
declare variable $id_user as xs:string external;
declare variable $date_limite as xs:date external;




<resultat>

  <!-- Tous les livres -->
  <listeLivres>
  {
    for $livre in doc("bibliotheque.xml")//livre
    return $livre
  }
  </listeLivres>

  <!-- Livres par auteur -->
  <livresParAuteur>
  {
    for $livre in doc("bibliotheque.xml")//livre[auteur = $auteur]
    return $livre
  }
  </livresParAuteur>

  <!-- Livres par genre -->
  <livresParGenre>
  {
    for $livre in doc("bibliotheque.xml")//livre[genre = $genre]
    return $livre
  }
  </livresParGenre>

  <!-- Livres empruntés par un utilisateur -->
  <livresEmpruntesParUtilisateur>
  {
    for $pret in doc("bibliotheque.xml")//pret[id_utilisateur = $id_user]
    let $livre := doc("bibliotheque.xml")//livre[@id = $pret/id_livre]
    return <livreEmprunte>
      <titre>{$livre/titre/text()}</titre>
    </livreEmprunte>
  }
  </livresEmpruntesParUtilisateur>

  <!-- Prêts après une certaine date -->
  <livresPretesApresDate>
  {
    for $pret in doc("bibliotheque.xml")//pret[xs:date(date_pret) > $date_limite]
    let $livre := doc("bibliotheque.xml")//livre[@id = $pret/id_livre]
    return <livre>
      <titre>{$livre/titre/text()}</titre>
      <datePret>{$pret/date_pret/text()}</datePret>
    </livre>
  }
  </livresPretesApresDate>

  <!-- Prêts actifs (livres non encore retournés) -->
  <pretsActifs>
  {
    for $pret in doc("bibliotheque.xml")//pret[not(date_retour) or normalize-space(date_retour) = ""]
    let $livre := doc("bibliotheque.xml")//livre[@id = $pret/id_livre]
    let $utilisateur := doc("bibliotheque.xml")//utilisateur[@id = $pret/id_utilisateur]
    return <pretActif>
      <livre>{$livre/titre/text()}</livre>
      <utilisateur>{$utilisateur/nom/text()}</utilisateur>
      <datePret>{$pret/date_pret}</datePret>
    </pretActif>
  }
  </pretsActifs>

  <!-- Prêts retournés -->
  <pretsRetournes>
  {
    for $pret in doc("bibliotheque.xml")//pret[normalize-space(date_retour) != ""]
    let $livre := doc("bibliotheque.xml")//livre[@id = $pret/id_livre]
    let $utilisateur := doc("bibliotheque.xml")//utilisateur[@id = $pret/id_utilisateur]
    return <pretRetourne>
      <livre>{$livre/titre/text()}</livre>
      <utilisateur>{$utilisateur/nom/text()}</utilisateur>
      <datePret>{$pret/date_pret}</datePret>
      <dateRetour>{$pret/date_retour}</dateRetour>
    </pretRetourne>
  }
  </pretsRetournes>

</resultat>
