import config, requests, json

minute_bars_url = config.BARS_URL + '/1Min?symbols=MSFT&limit=50'
r = requests.get(minute_bars_url, headers=config.HEADERS)
rData = r.json()
print(rData['MSFT'][0]['t'])

print(json.dumps(r.json(), indent=4))

