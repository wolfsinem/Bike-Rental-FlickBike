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

De URL's op de KNMI website:
- data per uur http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi
- data per dag http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi  
--------------------------------------------------------------------------------------------------------------------------------
"""
import requests
from io import StringIO
import pandas as pd

def weather_temp_HH():
    """ Weather data for each hour of a day 

    STN = Station
    HH = Uur van de dag
    T = Temperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming
    T10N = Minimumtemperatuur (in 0.1 graden Celsius) op 10 cm hoogte in de afgelopen 6 uur
    TD = Dauwpuntstemperatuur (in 0.1 graden Celsius) op 1.50 m hoogte tijdens de waarneming
    """
    url = "http://projects.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi"
    parameters = {'start': '2019010100', 'end': '2019120923', 'vars': 'TEMP', 'stns': '240'}
    response = requests.get(url, params=parameters)
    columnnames = [column.strip() for column in StringIO(response.text).read().split("#")[-2].split(',')] 
    file_data = pd.read_csv(StringIO(response.text), comment='#', sep=',', names=columnnames, parse_dates=[1], index_col=[1])
    return file_data

def weather_temp_DD():
    """ Weather data for each day

    STN = Station
    TG = Etmaalgemiddelde temperatuur (in 0.1 graden Celsius)
    TN = Minimum temperatuur (in 0.1 graden Celsius)
    TNH = Uurvak waarin TN is gemeten
    TX = Maximum temperatuur (in 0.1 graden Celsius)
    TXH = Uurvak waarin TX is gemeten
    T10N = Minimum temperatuur op 10 cm hoogte (in 0.1 graden Celsius)
    T10NH = 6-uurs tijdvak waarin T10N is gemeten
    """
    url = "http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi"
    parameters = {'start': '20190101', 'end': '20200131', 'vars': 'TEMP', 'stns': '240'}
    response = requests.get(url, params=parameters)
    columnnames = [column.strip() for column in StringIO(response.text).read().split("#")[-2].split(',')] 
    file_data = pd.read_csv(StringIO(response.text), comment='#', sep=',', names=columnnames, parse_dates=[1], index_col=[1])
    return file_data

def weather_wind_DD():
    """ Weather data for each day

    STN = Station
    DDVEC = Vectorgemiddelde windrichting in graden (360=noord, 90=oost, 180=zuid, 270=west, 0=windstil/variabel)
    FHVEC = Vectorgemiddelde windsnelheid (in 0.1 m/s)
    FG = Etmaalgemiddelde windsnelheid (in 0.1 m/s)
    FHX	= Hoogste uurgemiddelde windsnelheid (in 0.1 m/s)
    FHXH = Uurvak waarin FHX is gemeten
    FHN	= Laagste uurgemiddelde windsnelheid (in 0.1 m/s)
    FHNH = Uurvak waarin FHN is gemeten
    FXX	= Hoogste windstoot (in 0.1 m/s)
    FXXH = Uurvak waarin FXX is gemeten
    """
    url = "http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi"
    parameters = {'start': '20190101', 'end': '20200131', 'vars': 'WIND', 'stns': '240'}
    response = requests.get(url, params=parameters)
    columnnames = [column.strip() for column in StringIO(response.text).read().split("#")[-2].split(',')] 
    file_data = pd.read_csv(StringIO(response.text), comment='#', sep=',', names=columnnames, parse_dates=[1], index_col=[1])
    return file_data

def weather_PRCP_DD():
    """ Weather data for each day

    DR = Duur van de neerslag (in 0.1 uur)
    RH = Etmaalsom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm)
    RHX	= Hoogste uursom van de neerslag (in 0.1 mm) (-1 voor <0.05 mm)
    RHXH = Uurvak waarin RHX is gemeten
    EV24 = Referentiegewasverdamping (Makkink) (in 0.1 mm)
    """
    url = "http://projects.knmi.nl/klimatologie/daggegevens/getdata_dag.cgi"
    parameters = {'start': '20190101', 'end': '20200131', 'vars': 'PRCP', 'stns': '240'}
    response = requests.get(url, params=parameters)
    columnnames = [column.strip() for column in StringIO(response.text).read().split("#")[-2].split(',')] 
    file_data = pd.read_csv(StringIO(response.text), comment='#', sep=',', names=columnnames, parse_dates=[1], index_col=[1])
    return file_data
