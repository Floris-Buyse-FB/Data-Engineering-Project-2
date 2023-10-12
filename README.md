# Data-Engineering-Project-2

## 1 De data

De data is te groot voor op github te zetten dus die moet reeds lokaal staan. Je dient zelf een map `data` en een map `data_clean` aan te maken. In de map data staan de ruwe data dat we gekregen hebben van Voka. In de map data_clean zal de opgeschoonde data komen.

Vervolgens gaan we via het script `cleanup_script.py` de data opschonen. Dit script zal de data uit de map data halen en opschonen en in de map data_clean steken.

```
python cleanup_script.py [SUBCOMMAND]
```

Als laatste runnen we het script `change_col_name.ipynb` om de kolomnamen te veranderen naar een meer leesbare naam.

## 2 De database

Alvorens we de databank kunnen vullen moeten we eerst de database maken. Dit doen we door het script `create_db.sql` uit te voeren in SSMS. Dit script zal de database en de tabellen aanmaken.

Vervolgens gaan we de data in de database steken. Momenteel is er nog geen script dat dit doet. Dit zal in de toekomst nog gebeuren. Wel hebben we een test script voor Account `AA_test_ORM.ipynb`.

## 3 De API

To be continued...

## 4 Python virtual environment

In deze stap installeren we virtualenv. Dit is een geisolleerde python omgeving. Hierin installeren we de nodige packages.

Voer volgende commandos uit:

```
$ pip install virtualenv
$ python3 -m venv .venv

$ source .venv/bin/activate // In Linux en mac
$ env/Scripts/activate.bat //In CMD
$ env/Scripts/Activate.ps1 //In Powershel

$ pip install -r ./data_info/requirements.txt
```

## 5 streamlit

Met streamlit kunnen we een webapplicatie maken. Deze webapplicatie zal de data visualiseren. Om deze webapplicatie te runnen voeren we volgende commando uit:

```
streamlit run ./Hello.py
```
