while true
do
  python3 ../lib/mfa_get_status.py ../data/mfa_ids.csv > ../data/mfa_status.csv && break

  echo 'Retrying in 5 seconds'  
  sleep 5
done