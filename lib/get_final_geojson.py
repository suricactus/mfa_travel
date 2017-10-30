import sys
import csv
import json
from collections import defaultdict

mfa_status_csv = sys.argv[1]
mfa_visa_list_csv = sys.argv[2]
passport_index_csv = sys.argv[3]

countries_map = defaultdict(lambda:{}, {})
passport_map = defaultdict(lambda:{}, {})

VISA_ID_CARD = 'VISA_ID_CARD'
VISA_FREE = 'VISA_FREE'
VISA_ON_ARRIVAL = 'VISA_ON_ARRIVAL'
VISA_E = 'VISA_E'
VISA_REQUIRED = 'VISA_REQUIRED'

with open(passport_index_csv, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
      passport_map[ row['iso_a2'] ]['visa_free'] = bool(int(row['visa_free']))
      passport_map[ row['iso_a2'] ]['evisa'] = bool(int(row['evisa']))
      passport_map[ row['iso_a2'] ]['visa_on_arrival'] = bool(int(row['visa_on_arrival']))

      if int(row['visa_free']):
        passport_map[ row['iso_a2'] ]['visa'] = VISA_FREE
      elif int(row['evisa']): 
        passport_map[ row['iso_a2'] ]['visa'] = VISA_E
      elif int(row['visa_on_arrival']): 
        passport_map[ row['iso_a2'] ]['visa'] = VISA_ON_ARRIVAL
      else:
        passport_map[ row['iso_a2'] ]['visa'] = VISA_REQUIRED


with open(mfa_status_csv, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
      countries_map[ row['iso_a3'] ]['status'] = int(row['status'])
      countries_map[ row['iso_a3'] ]['url'] = row['url']

with open(mfa_visa_list_csv, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:      
      country_data = countries_map[ row['iso_a3'] ]

      country_data['notes'] = row['notes'];
      country_data['requires_passport'] = not bool(int(row['is_id_card_only'])) if row['is_id_card_only'] != '' else None
      country_data['requires_visa'] = not bool(int(row['is_without_visa'])) if row['is_without_visa'] != '' else None


geojson = json.load(sys.stdin)

for f in geojson['features']:
  f['properties'] = {
    **f['properties'],
    **countries_map[ f['properties']['iso_a3'] ],
  }

  if 'visa' in passport_map[ f['properties']['iso_a2'] ]:
    if f['properties']['requires_passport'] == False:
      f['properties']['visa'] = VISA_ID_CARD
    else:
      if f['properties']['requires_visa'] == True and passport_map[ f['properties']['iso_a2'] ]['visa'] == VISA_FREE:
        f['properties']['visa'] = VISA_REQUIRED
      else:
        f['properties']['visa'] = passport_map[ f['properties']['iso_a2'] ]['visa']


  if f['properties']['iso_a3'] == 'BGR':
    f['properties']['home_country'] = True



print(json.dumps(geojson))