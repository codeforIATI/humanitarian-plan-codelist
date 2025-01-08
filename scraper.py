from os.path import join
import csv
from operator import itemgetter

import requests

url = 'https://api.hpc.tools/v2/public/plan'
headers = ['Plan name', 'Plan code', 'Plan type', 'Plan year', 'Start date', 'End date']

r = requests.get(url)
data = r.json()
rows = []

# fix the dates
for item in data['data']:
    rows.append({
        'Plan name': item['planVersion']['name'],
        'Plan code': item['planVersion']['code'],
        'Plan type': ",".join([it['name'] for it in item['categories'] if it['group'] == 'planType']),
        'Plan year': ",".join([it['year'] for it in item['years']]),
        'Start date': item['planVersion']['startDate'],
        'End date': item['planVersion']['endDate'],
    })


rows.sort(key=itemgetter('Plan name'))
rows.sort(key=itemgetter('Plan year'), reverse=True)

with open(join('output', 'humanitarian-plan.csv'), 'w') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(rows)
