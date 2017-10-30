cat ../data/countries.geo.json |
python3 ../lib/get_final_geojson.py ../data/mfa_status.csv ../data/mfa_visa_list.csv > ../data/countries_final.geo.json