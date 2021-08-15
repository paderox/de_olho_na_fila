import requests
import json

url = 'https://deolhonafila.prefeitura.sp.gov.br/processadores/dados.php'

payload = 'dados=dados'
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request('POST', url, headers=headers, data=payload)
data = json.loads(response.text)

with open('raw_data.json', 'w', encoding='utf8') as outfile:
  json.dump(data, outfile, ensure_ascii=False)

print("updated raw data")