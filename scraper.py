from os.path import join
from io import BytesIO
import csv

import requests
import openpyxl

# via https://fts.unocha.org/plan-code-list-iati
r = requests.get('https://fts.unocha.org/download/126339/download')
wb = openpyxl.load_workbook(BytesIO(r.content))
sheet = wb['Export data']
rows = [[cell.value for cell in row] for row in sheet.rows]

# bin the first 2 rows
rows = rows[2:]

with open(join('docs', 'humanitarian-plan.csv'), 'w') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
