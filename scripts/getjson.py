import os
import datetime
import requests
import json

today = datetime.datetime.now().strftime('%Y-%m-%d')
yesterday = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(1), '%Y-%m-%d')

headers = {'Accept': 'application/json'}

KEY = os.getenv('KEY')
ID = os.getenv('ID')
root_path = os.getenv("ROOT_PATH","/home/gr4n0t4/pdm")

r1 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={yesterday}-23:00&end={today}-08:00", headers=headers)
r2 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={today}-08:00&end={today}-12:00", headers=headers)
r3 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={today}-12:00&end={today}-15:00", headers=headers)    
r4 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={today}-15:00&end={today}-18:00", headers=headers)
r5 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={today}-18:00&end={today}-21:00", headers=headers)
r6 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={today}-21:00&end={today}-23:00", headers=headers)
matches = {'matches' :[]}
all_matches = r1.json()['matches'] + r2.json()['matches'] + r3.json()['matches'] + r4.json()['matches'] + r5.json()['matches'] + r6.json()['matches']
print(f"Matches on {today}: {len(all_matches)}")
for match in all_matches:
    if 'pdm' not in str(match['teams'][0]['teamname']).lower() and 'pdm' not in str(match['teams'][1]['teamname']).lower():
        continue
    matches['matches'].append(match) 
with open(f"{root_path}/data/{ID}-{today}.json", 'w', encoding='utf-8') as f:
    json.dump(matches, f, ensure_ascii=False, indent=4)
