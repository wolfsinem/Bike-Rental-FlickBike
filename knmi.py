"""
KNMI documentatie: parameters
--------------------------------------------------------------------------------------------------------------------------------
start       = De volledige datum (start) in format YYYYMMDD. Default is de eerste dag van de huidige maand.
end         = De volledige datum (end) in format YYYYMMDD. Default is de huidige dag (of de laatste dag waarvoor 
              data aanwezig is).
inseason    = Wanneer deze variabele ingevuld is, worden van elk jaar tussen begin- en einddatum alleen de dagen 
              geselecteerd die binnen het seizoen (bday,bmonth)-(eday,emonth) vallen. Bijvoorbeeld, als inseason=Y 
              en de begin- en einddatum zijn respectievelijk 19731101 en 20030303, dan bevat de uitvoer alleen de dagen 
              tussen deze twee data die in de periode 1 november t/m 3 maart vallen, terwijl 19730406 en 20080406 alle 
              6-aprils in de jaren 1973 t/m 2008 opleveren.
vars        = Lijst van gewenste variabelen in willekeurige volgorde, aangeduid met hun acroniemen (zoals op de selectiepagina)
              gescheiden door ':', bijvoorbeeld 'TG:TN:EV24'. Hierin zijn de volgende acroniemen gedefiniëerd om groepen van 
              variabelen aan te duiden:
                                        -   WIND   DDVEC:FG:FHX:FHX:FX wind
                                        -   TEMP   TG:TN:TX:T10N temperatuur
                                        -   SUNR   SQ:SP:Q Zonneschijnduur en globale straling
                                        -   PRCP   DR:RH:EV24 neerslag en potentiële verdamping
                                        -   PRES   PG:PGX:PGN druk op zeeniveau
                                        -   VICL   VVN:VVX:NG zicht en bewolking
                                        -   MSTR   UG:UX:UN luchtvochtigheid
                                        -   ALL alle variabelen (default)
stns        = Lijst van gewenste stations (nummers) in willekeurige volgorde, gescheiden door ':'. Geen default waarde; Stations 
              móeten zijn gespecificeerd. ALL staat voor álle stations.

Per dag: 
start = YYYYMMDDHH
end = YYYYMMDDHH
HH = eerste en laatste uur

De URL's op de KNMI website:
- data per uur http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi
- data per dag http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi  
--------------------------------------------------------------------------------------------------------------------------------
"""
import requests
from io import StringIO
import pandas as pd

def weather_data():
    url = "http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi"
    parameters = {'start': '20190101', 'vars': 'TEMP', 'stns': '240'}
    response = requests.get(url, params=parameters)
    columnnames = [column.strip() for column in StringIO(response.text).read().split("#")[-2].split(',')] 
    file_data = pd.read_csv(StringIO(response.text), comment='#', sep=',', names=columnnames, parse_dates=[1], index_col=[1])
    return file_data