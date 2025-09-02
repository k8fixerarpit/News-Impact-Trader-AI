import csv, datetime
rows = [
  {'time': datetime.datetime.utcnow().isoformat(), 'title':'Reliance profit rises','source':'ET','ticker':'RELIANCE.NS'}]
with open('backend/data/sample_headlines.csv','w',newline='') as f:
  writer = csv.DictWriter(f, fieldnames=rows[0].keys())
  writer.writeheader()
  writer.writerows(rows)
print('Seeded sample news.')
