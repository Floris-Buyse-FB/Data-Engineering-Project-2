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

## 2 De database

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

Met streamlit kunnen we een webapplicatie maken. Deze webapplicatie zal de data visualiseren. Om deze webapplicatie te runnen voeren we volgende commando uit:

```Bash
streamlit run ./Hello.py
```
