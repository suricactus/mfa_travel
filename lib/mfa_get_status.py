'''
Целта на този скрипт е да проверява препоръката на Министерството на външните работи относно пътуване до чужди държави.
Работи по изключително елементарен начин, като проверява картинката, която са сложили от министерството със съответната препоръка.

Първият и единствен аргумент e пътят до csv файла, в който са записани id-тата на отделните държави според сайта на Министерството
'''

import sys
import csv
import urllib.request
import re

MFA_URL = 'http://www.mfa.bg/index.php?page=120&staticpage=findanembassy&posolstvo='
STATUS_REGEX = r'src="/uploads/images/risk-(\d).jpg"'
INLINE_IMG_REGEX = {
  '2': [r'src="data:image/jpeg;base64,/9j/4QtSRXhpZgAATU0AKgAAAAgABwESAAMAAAABAAEAAAEaAAUAAAABAAAAYgEbAAUAAAABAAAAagEoAAMAAAABAAIAAAExAAIAAAAeAAAAcgEyAAIAAAAUAAAAkIdpAAQAAAABAAAApAAAANAACvyAAAAnEAAK'],
  '3': [
    r'src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAcsAAABQCAIAAAD5tskkAAAgAElEQVR4nNS9d1hUSdY',
    r'src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAcwAAABQCAIAAAAbatJdAAAgAElEQVR4nO293VccV5Yn'
  ],
  '4': [r'src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAcwAAABQCAIAAAAbatJdAAAgAElEQVR4nO29W3McV3Yu']
}

mfa_csv = sys.argv[1]

print("iso_a3,status,url")

with open(mfa_csv, 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
      # in case there is no ISO code for the country
      if row['iso_a3'] == '':
        continue

      url = MFA_URL + row['mfa_id']
      html = urllib.request.urlopen(url).read().decode('utf-8')

      m = re.search(STATUS_REGEX, html)

      status = -1

      if m is None:
        for potential_status, regex_arr in INLINE_IMG_REGEX.items():
          for regex in regex_arr:
            if re.search(regex, html) is not None:
              status = int(potential_status)
      else:
        status = m.group(1)

      print("{},{},{}".format(row['iso_a3'], status, url))
