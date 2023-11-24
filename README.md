# Data-Engineering-Project-2

## 1 De data

De data is te groot voor op github te zetten dus die moet reeds lokaal staan. Je dient zelf een map `data` en een map `data_clean` aan te maken. In de map data staan de ruwe data dat we gekregen hebben van Voka. In de map data_clean zal de opgeschoonde data komen.

Vervolgens gaan we via het script `cleanup_script.py` de data opschonen. Dit script zal de data uit de map data halen en opschonen en in de map data_clean steken.

Om het script te runnen moeten we eerst in de map `scripts` zitten.
Vervolgens voeren we volgende commando uit:

```Bash
python cleanup_script.py [SUBCOMMAND]
```

Gebruik `'all'` als subcommando om alle data op te schonen.
Voor de andere subcommandos ga je best eens kijken in het script zelf. Deze staan onderaan het script.

## 2 De database en DWH

Alvorens we de databank kunnen vullen moeten we eerst de database maken. Dit doen we door het script `create_db.sql` uit te voeren in SSMS. Dit script zal de database en de tabellen aanmaken.

Vervolgens gaan we de data in de database steken. Dit doet het script `AA_ORM_PUSH_DATA.py`. Dit script is nog onder constructie maar je kan al enkele tabellen vullen (zie commentaar in het script zelf)

## 3 De API

To be continued...

## 4 Python virtual environment

In deze stap installeren we virtualenv. Dit is een geisolleerde python omgeving. Hierin installeren we de nodige packages.

Voer volgende commandos uit:

```Bash
$ pip install virtualenv
$ python3 -m venv .venv

# Activate virtual environment in Linux and macOS
$ source .venv/bin/activate

# Activate virtual environment in Windows CMD
$ .venv\Scripts\activate.bat

# Activate virtual environment in PowerShell
$ .venv\Scripts\Activate.ps1

$ pip install -r ./data_info/requirements.txt
```

## 5 streamlit

Met streamlit kunnen we een webapplicatie maken. Deze webapplicatie zal de data visualiseren.

Maak een folder `.streamlit` aan.
In deze folder zet je vervolgens het bestand `config.toml`. Dit bestand bevat de configuratie van de webapplicatie, dus `DB_NAME` en `SERVER_NAME`.

Om deze webapplicatie te runnen gaan we eerst naar de map `app` en voeren we vervolgens onderstaand commando uit:

```Bash
streamlit run ./Hello.py
```

Dit platform biedt een gestructureerde set tabbladen aan: `add_data`, `recommendations`, `lookalikes`, en `view_data`.
### 5.1 add_data
Dit tabblad is gewijd aan het systematisch toevoegen van gegevens aan het datawarehouse. Door middel van `online learning` ondergaan onze modellen consequent hertraining.

### 5.2 recommendations
Binnen deze sectie bevinden zich extra tabbladen met de labels `Instellingen` en `Aanbevelingen`
. In het tabblad Instellingen hebben gebruikers de mogelijkheid om de marketingdruk zelf te bepalen aan de hand van specifieke configuraties. Vervolgens worden er aanbevelingen gegenereerd op basis van de ingevoerde individuele gegevens. De daaruit voortvloeiende output is tevens downloadbaar.

### 5.3 lookalikes
In dit tabblad voert de gebruiker een contactpersoon in en verkrijgt vervolgens het gewenste aantal 'lookalikes'. Deze 'lookalikes' kunnen direct en accuraat worden geverifieerd.

### 5.4 view_data
Dit tabblad vereenvoudigt het proces van het kiezen en tonen van specifieke tabellen door gebruikers.



