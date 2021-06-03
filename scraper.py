from os.path import join
from io import BytesIO
import csv

import requests
import openpyxl

# via https://fts.unocha.org/plan-code-list-iati
url = 'https://fts.unocha.org/download/initiate/views_executable/xlsx?uri=/plan-code-list-iati&query%5Buri%5D=/plan-code-list-iati&query%5Bview_id%5D=plan_code_list_for_iati&query%5Bview_display%5D=page&query%5B_wrapper_format%5D=drupal_modal&view_id=plan_code_list_for_iati&view_display=page'
r = requests.get(url)
download_id = r.json()[0].get('download_id')

r = requests.get(f'https://fts.unocha.org/download/{download_id}/download')
wb = openpyxl.load_workbook(BytesIO(r.content))
sheet = wb['Export data']
rows = [[cell.value for cell in row] for row in sheet.rows]

# bin the first 2 rows
rows = rows[2:]

with open(join('docs', 'humanitarian-plan.csv'), 'w') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
