# Eindrapport Data-Engineering-Project 2 -- Groep 2

## Epic 1

`Korte uitleg van de epic`

We hebben een relationele databank opgezet waarin de aangeleverde data wordt bijgehouden. Deze data hebben we eerst gecleaned en enkel de data van Oost-Vlaanderen behouden. Vervolgens hebben we de data in een relationele databank gestoken en een User Interface gemaakt waarop bepaalde queries kunnen uitgevoerd worden. Deze queries kunnen zelf geschreven worden en er zijn ook enkele voorgemaakte queries beschikbaar.

`Beperkingen en uitdagingen`

Het cleanen van de data was een lastige taak. Er was veel data die niet bruikbaar was (NaN waarden) en er waren ook veel verschillende formaten. Er zat weinig structuur in de data en die hebben we zelf moeten toevoegen wat veel tijd in beslag nam. Ook waren er veel problemen met de Foreign Keys en Primary Keys (niet bestaande primary key waarvan er wel een foreign key was bijvoorbeeld). De data types klopten ook niet altijd en moesten we zelf aanpassen.

`Bepaalde keuzes door beperkingen`

Soms hebben we enkele rijen data moeten laten vallen aangezien er hier weinig tot geen nuttige informatie in stond (veel NaN waarden). Dit heeft misschien tot gevolg dat er sommige bedrijven die wel in de data zitten niet meer in de databank zitten.

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

Eerst en vooral algemene cleanups doen zoals het verwijderen van / opvullen van NaN waarden. Ook hebben we de kolomnamen aangepast zodat deze leesbaarder waren en allemaal hetzelfde formaat hebben. Daarnaast hebben we rijen moeten verwijderen die data hadden met Foreign Keys die verwezen naar niet bestaande Primary Keys om geen problemen te krijgen met de databank. Als laatste hebben we ook nog de juiste data types moeten toekennen aan sommige kolommen (Bijvoorbeeld Float getallen of datums die als String in de data zaten).

De databank maken hebben we gedaan door het meegeven ERD goed te analyseren en zo hebben we ons eigen ERD kunnen maken, aangepast aan onze doorgevoerde wijzigingen. Dan hebben we met behulp van een Object Relational Mapper (ORM) de data in de database gestoken.

## Epic 2

`Korte uitleg van de epic`

`Beperkingen en uitdagingen`

`Bepaalde keuzes door beperkingen`

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

`Welke data / parameters zijn er gebruikt`

`Waarvan is er te weinig data`

## Epic 3

`Korte uitleg van de epic`

`Beperkingen en uitdagingen`

`Bepaalde keuzes door beperkingen`

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

`Welke data / parameters zijn er gebruikt`

`Waarvan is er te weinig data`

## Epic 4

`Korte uitleg van de epic`

`Beperkingen en uitdagingen`

`Bepaalde keuzes door beperkingen`

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

`Welke data / parameters zijn er gebruikt`

`Waarvan is er te weinig data`

## Epic 5

`Korte uitleg van de epic`

Op basis van een gegeven CampagneID, een aantal contactpersonen aanbevelen die het meest geschikt zouden zijn voor deze bepaalde campagne. Deze contactpersonen worden dan gesorteerd, van weinig naar veel, op basis van de Marketing Pressure die ze hebben.

`Beperkingen en uitdagingen`

Er was niet superveel data om een goed model mee te trainen. Ook zijn er soms meerdere contactpersonen per bedrijf wat het een extra uitdaging maakte om de data voor te bereiden voor het aanbevelingssysteem.

`Bepaalde keuzes door beperkingen`

Aangezien er weinig data was hebben we gekozen om gebruik te maken van cosinus similariteit van de keyphrases van de contactpersonen. Dit is een eenvoudige manier om de contactpersonen te vergelijken met elkaar en zo de meest geschikte te vinden zonder dat we een model moeten trainen.

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

Na eerst te hebben geprobeerd met Clustering models en de Surprise library hebben we uiteindelijk gekozen om gebruik te maken van TFIDF-Vectorization en Cosinus Similariteit.

`Welke data / parameters zijn er gebruikt`

```Text
De gebruikte Machine Learning technieken zijn:
```

- TFIDF-Vectorization
- Cosinus Similariteit

Voor beide technieken hebben we gebruik gemaakt van de Scikit-Learn library.

```Text
Om de keyphrases te maken hebben we volgende kolommen gebruikt:
```

- Account
  - plaats, subregio, ondernemingstype, ondernemingsaard
- Activiteit
  - activiteitNaam
- Functie
  - functietitel
- Afspraak
  - thema, onderwerp, keyphrases, afspraak_betreft
- Campagne
  - naam, type, soort
- Mailing
  - naam, onderwerp
- Sessie
  - thema_naam

```Text
Om de marketing pressure te bereken hebben we volgende kolommen gebruikt:
(In de user interface kan je zelf kiezen welke kolommen je wilt gebruiken)
```

- Persoon
  - alle kolommen met mail_thema en mail_type, marketingcommunicatie
- CDI_Visit
  - bron, visit_first_page, visit_total_pages
- Mailing
  - bij mailing hebben we de mail_click_frequency berekend per account

`Waarvan is er te weinig data`

Er zijn te weining campagnes en accounts van Oost-Vlaanderen.

## Epic 7

`Korte uitleg van de epic`

`Beperkingen en uitdagingen`

`Bepaalde keuzes door beperkingen`

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

`Welke data / parameters zijn er gebruikt`

`Waarvan is er te weinig data`

## Epic 8

`Korte uitleg van de epic`

`Beperkingen en uitdagingen`

`Bepaalde keuzes door beperkingen`

`Gedachtengang / Hoe zijn we tot de oplossingen zijn gekomen`

`Welke data / parameters zijn er gebruikt`

`Waarvan is er te weinig data`

## Algemene reflectie

`Aangeleverde data`

`Datakwaliiteit`

`Mogelijkheden / beperkingen om inzichten te verkrijgen`
