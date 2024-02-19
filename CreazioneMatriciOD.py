import pandas as pd

# Funzione per estrarre gli ID dei TAZ dal file XML
def extract_taz_ids_from_xml(xml_file):
    taz_ids = []
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for taz in root.iter('taz'):
        taz_id = taz.attrib.get('id')  # Rimuovi le virgolette dagli ID
        taz_ids.append(taz_id)
    return taz_ids

# Leggi il file CSV della matrice OD
data = pd.read_csv("matriceod_persone_viaggi.csv", delimiter=';')

# Converti la colonna NumViaggi da float a interi
data['NumViaggi'] = data['NumViaggi'].str.replace(',', '.').astype(float).astype(int)

# Leggi il file XML dei TAZ e ottieni gli ID dei TAZ
taz_ids = extract_taz_ids_from_xml("districts.taz.xml")
# Filtra le righe del DataFrame che contengono solo ID dei TAZ presenti nel file XML
filtered_data = data[data['ORIG_COD_ZONA'].astype(str).isin(taz_ids) & data['DEST_COD_ZONA'].astype(str).isin(taz_ids)]
filtered_data
# Salva la matrice OD filtrata
filtered_data.to_csv("matriceod_persone_viaggi_filtrata.csv", index=False)

import pandas as pd

# Leggi il file CSV
data = pd.read_csv("matriceod_persone_viaggi_filtrata.csv", delimiter=',')

# Converti la colonna NumViaggi da float a interi
data['NumViaggi'] = data['NumViaggi'].astype(int)

# Mappa i valori di mezzo aggregato secondo le specifiche
mezzo_mapping = {
    'AUTO': ['AUTO'],
    'BICI': ['BICI'],
    'FURGONE': ['FURGONE'],
    'MOTO': ['MOTO'],
    'PIEDI': ['PIEDI'],
    'TPL FERRO': ['TPL FERRO'],
    'TPL GOMMA': ['TPL GOMMA']
}

# Applica la mappatura al DataFrame
for mezzo_aggregato, tipi_mezzo in mezzo_mapping.items():
    data.loc[data['MEZZO_aggregato'].isin(tipi_mezzo), 'MEZZO_aggregato'] = mezzo_aggregato

# Definizione delle fasce orarie
fascia_oraria_mapping = {
    1: {'from_time': '6.30', 'to_time': '9.00'},
    2: {'from_time': '17.00', 'to_time': '20.00'}
}

# Funzione per ottenere l'intervallo di tempo per una data fascia oraria
def get_time_interval(fascia):
    return fascia_oraria_mapping.get(fascia, {'from_time': '0.00', 'to_time': '0.00'})

# Creazione della matrice OD
def create_od_matrix(df, filename, from_time, to_time):
    with open(filename, 'w') as file:
        # Intestazione
        file.write(f'$OR;D2\n* From-Time To-Time\n{from_time} {to_time}\n*Factor\n1.00\n* some\n* additional\n* comments\n')
        
        # Somma dei viaggi per ogni coppia origine-destinazione
        sum_viaggi = df.groupby(['ORIG_COD_ZONA', 'DEST_COD_ZONA'])['NumViaggi'].sum()
        
        # Dati della matrice
        for (origine, destinazione), num_viaggi in sum_viaggi.items():
            file.write(f"{origine:>4} {destinazione:>4} {num_viaggi:>4}\n")

# Raggruppa i dati per fascia oraria e mezzo aggregato
grouped_data = data.groupby(['FASCIA_ORARIA_VIAGGIO', 'MEZZO_aggregato'])

# Crea la matrice OD per ciascuna combinazione di intervallo di tempo e mezzo aggregato
for (fascia_oraria, mezzo_aggregato), df in grouped_data:
    # Salta la fascia 0
    if fascia_oraria == 0:
        continue
    
    intervallo = get_time_interval(fascia_oraria)
    create_od_matrix(df, f"{mezzo_aggregato}_{fascia_oraria}.od", intervallo['from_time'], intervallo['to_time'])
    
import pandas as pd
import numpy as np

# Leggi il file CSV
data = pd.read_csv("matriceod_persone_viaggi_filtrata.csv", delimiter=',')

# Converti la colonna NumViaggi da float a interi
data['NumViaggi'] = data['NumViaggi'].astype(int)

# Mappa i valori di mezzo aggregato secondo le specifiche
mezzo_mapping = {
    'AUTO': ['AUTO'],
    'BICI': ['BICI'],
    'FURGONE': ['FURGONE'],
    'MOTO': ['MOTO'],
    'PIEDI': ['PIEDI'],
    'TPL FERRO': ['TPL FERRO'],
    'TPL GOMMA': ['TPL GOMMA']
}

# Applica la mappatura al DataFrame
for mezzo_aggregato, tipi_mezzo in mezzo_mapping.items():
    data.loc[data['MEZZO_aggregato'].isin(tipi_mezzo), 'MEZZO_aggregato'] = mezzo_aggregato

# Seleziona solo i dati della fascia oraria 0
data_fascia_0 = data[data['FASCIA_ORARIA_VIAGGIO'] == 0]

# Raggruppa i dati per tipo aggregato di mezzo
grouped_data = data_fascia_0.groupby('MEZZO_aggregato')

# Funzione per dividere proporzionalmente il numero di viaggi in tre liste
def divide_viaggi_proporzionalmente(numeri):
    proporzione_1 = [int(x * 0.25) for x in numeri]  # 25%
    proporzione_2 = [int(x * 0.3) for x in numeri]   # 30%
    proporzione_3 = [x - (proporzione_1[i] + proporzione_2[i]) for i, x in enumerate(numeri)]  # Il resto
    return proporzione_1, proporzione_2, proporzione_3

# Itera attraverso i dati raggruppati
for mezzo_aggregato, df in grouped_data:
    # Calcola il numero totale di viaggi per questo tipo aggregato
    total_trips = df.groupby(['ORIG_COD_ZONA', 'DEST_COD_ZONA'])['NumViaggi'].sum().tolist()
    
    # Dividi il numero totale di viaggi proporzionalmente
    trips_1, trips_2, trips_3 = divide_viaggi_proporzionalmente(total_trips)
    
    # Intestazione per la matrice OD
    header_1 = f"$OR;D2\n* From-Time To-Time\n0.00 6.29\n*Factor\n1.00\n* some\n* additional\n* comments\n"
    header_2 = f"$OR;D2\n* From-Time To-Time\n9.01 16.59\n*Factor\n1.00\n* some\n* additional\n* comments\n"
    header_3 = f"$OR;D2\n* From-Time To-Time\n20.01 23.59\n*Factor\n1.00\n* some\n* additional\n* comments\n"
    
    # Creazione delle matrici OD
    with open(f"{mezzo_aggregato}_0_1.od", 'w') as file1, \
         open(f"{mezzo_aggregato}_0_2.od", 'w') as file2, \
         open(f"{mezzo_aggregato}_0_3.od", 'w') as file3:
        
        # Scrivi l'intestazione in ogni file
        file1.write(header_1)
        file2.write(header_2)
        file3.write(header_3)
        
        # Dati della matrice
        for i, (origine, destinazione) in enumerate(df.groupby(['ORIG_COD_ZONA', 'DEST_COD_ZONA']).groups.keys()):
            file1.write(f"{origine:>4} {destinazione:>4} {trips_1[i]:>4}\n")
            file2.write(f"{origine:>4} {destinazione:>4} {trips_2[i]:>4}\n")
            file3.write(f"{origine:>4} {destinazione:>4} {trips_3[i]:>4}\n")
