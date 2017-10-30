import sys
import csv
import json
from collections import defaultdict

mfa_status_csv = sys.argv[1]
mfa_visa_list_csv = sys.argv[2]

countries_map = defaultdict(lambda:{}, {})

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
      country_data['requires_visa'] = not bool(int(row['is_without_visa'])) if row['is_without_visa'] != '' else None
      country_data['requires_passport'] = not bool(int(row['is_id_card_only'])) if row['is_id_card_only'] != '' else None


geojson = json.load(sys.stdin)

for f in geojson['features']:
  f['properties'] = {
    **f['properties'],
    **countries_map[ f['properties']['iso_a3'] ]
  }

  if f['properties']['iso_a3'] == 'BGR':
    f['properties']['home_country'] = True

print(json.dumps(geojson))