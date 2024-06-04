import os
import datetime
import requests
import json

input = '2024-03-13'
format = '%Y-%m-%d'
 
start = datetime.datetime.strptime(input, format)
end = datetime.datetime.now()

delta = end - start
headers = {'Accept': 'application/json'}

KEY = os.getenv('KEY')
ID = os.getenv('ID')
root_path = os.getenv("ROOT_PATH","/home/gr4n0t4/pdm")

for i in range(delta.days + 1):

    day = start + datetime.timedelta(days=i)
    print(day.date())

    r1 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-00:00&end={day.date()}-08:00", headers=headers)
    r2 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-08:00&end={day.date()}-12:00", headers=headers)
    r3 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-12:00&end={day.date()}-15:00", headers=headers)    
    r4 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-15:00&end={day.date()}-18:00", headers=headers)
    r5 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-18:00&end={day.date()}-21:00", headers=headers)
    r6 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-21:00&end={day.date()}-23:59:59", headers=headers)
    matches = {'matches' :[]}
    all_matches = r1.json()['matches'] + r2.json()['matches'] + r3.json()['matches'] + r4.json()['matches'] + r5.json()['matches'] + r6.json()['matches']
    print(f"Matches on {day.date()}: {len(all_matches)}")
    for match in all_matches:
        if 'pdm' not in str(match['teams'][0]['teamname']).lower() and 'pdm' not in str(match['teams'][1]['teamname']).lower():
            continue
        matches['matches'].append(match) 
    with open(f"{root_path}/test/{ID}-{day.date()}.json", 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=4)
