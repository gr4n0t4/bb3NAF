import os
import datetime
import requests
import json

import os
import datetime
import requests
import json

input = '2025-06-10'
format = '%Y-%m-%d'
 
start = datetime.datetime.strptime(input, format)
end = datetime.datetime.now()

delta = end - start
headers = {'Accept': 'application/json'}

KEY = os.getenv('KEY')
ID = os.getenv('ID')
root_path = os.getenv("ROOT_PATH","/home/gr4n0t4/pdm")

all_teams = {}
teams = {}
matches = {'matches' :[]}

for i in range(delta.days + 1):

    day = start + datetime.timedelta(days=i)
    print(day.date())

    r1 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-00:00&end={day.date()}-08:00", headers=headers)
    if r1.json()['matches'] == 1000:
        print("Posible missing matches in r1")
    r2 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-08:00&end={day.date()}-12:00", headers=headers)
    if r2.json()['matches'] == 1000:
        print("Posible missing matches in r2")
    r3 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-12:00&end={day.date()}-15:00", headers=headers)    
    if r3.json()['matches'] == 1000:
        print("Posible missing matches in r3")
    r4 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-15:00&end={day.date()}-18:00", headers=headers)
    if r4.json()['matches'] == 1000:
        print("Posible missing matches in r4")
    r5 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-18:00&end={day.date()}-21:00", headers=headers)
    if r5.json()['matches'] == 1000:
        print("Posible missing matches in r5")
    r6 = requests.get(f"https://web.cyanide-studio.com/ws/bb3/matches/?key={KEY}&competition_id={ID}&limit=1000&start={day.date()}-21:00&end={day.date()}-23:59:59", headers=headers)
    if r6.json()['matches'] == 1000:
        print("Posible missing matches in r6")
    all_matches = r1.json()['matches'] + r2.json()['matches'] + r3.json()['matches'] + r4.json()['matches'] + r5.json()['matches'] + r6.json()['matches']
    all_matches = sorted(all_matches, key=lambda x: x['started'])
    print(f"Matches on {day.date()}: {len(all_matches)}")
    for match in all_matches:

        if 'pdm' not in str(match['teams'][0]['teamname']).lower() and 'pdm' not in str(match['teams'][1]['teamname']).lower():
            continue

        entrenador_casa = match['teams'][0]['idteamlisting']
        entrenador_fuera = match['teams'][1]['idteamlisting']        
        # Home
        if match['teams'][0]['idteamlisting'] not in all_teams:
            all_teams[entrenador_casa] = {'nombre': str(match['teams'][0]['teamname']),
                                                'entrenador' : str(match['coaches'][0]['coachname']),
                                                'victorias': 0,
                                                'empates': 0,
                                                'derrotas': 0,
                                                'puntos': 150,
                                                'td_favor': 0,
                                                'td_contra': 0,
                                                'cas_favor': 0,
                                                'cas_contra': 0,
                                                'raza': 0
                                                }
        # Away
        if match['teams'][1]['idteamlisting'] not in all_teams:
            all_teams[entrenador_fuera] = {'nombre': str(match['teams'][1]['teamname']),
                                                'entrenador' : str(match['coaches'][1]['coachname']),
                                                'victorias': 0,
                                                'empates': 0,
                                                'derrotas': 0,
                                                'puntos': 150,
                                                'td_favor': 0,
                                                'td_contra': 0,
                                                'cas_favor': 0,
                                                'cas_contra': 0,
                                                'raza': 0
                                                }
        all_teams[entrenador_casa]['raza'] = match['teams'][0]['idraces']

        all_teams[entrenador_casa]['td_favor']+=match['teams'][0]['score']
        all_teams[entrenador_casa]['td_contra']+=match['teams'][1]['score']
        try:
            all_teams[entrenador_casa]['cas_favor']+=match['teams'][0]['inflictedcasualties']
        except TypeError:
            print("inflictedcasualties is none")
        try:
            all_teams[entrenador_casa]['cas_contra']+=match['teams'][1]['inflictedcasualties']
        except TypeError:
            print("inflictedcasualties is none")
        scoring_points_casa = 0
        if match['teams'][0]['score'] == match['teams'][1]['score']:
            all_teams[entrenador_casa]['empates']+=1
            scoring_points_casa = 0.5
        if  match['teams'][0]['score'] < match['teams'][1]['score']:
            all_teams[entrenador_casa]['derrotas']+=1
        if  match['teams'][0]['score'] > match['teams'][1]['score']:
            all_teams[entrenador_casa]['victorias']+=1
            scoring_points_casa = 1



        all_teams[entrenador_fuera]['raza'] = match['teams'][1]['idraces']

        all_teams[entrenador_fuera]['td_favor']+=match['teams'][1]['score']
        all_teams[entrenador_fuera]['td_contra']+=match['teams'][0]['score']

        try:
            all_teams[entrenador_fuera]['cas_favor']+=match['teams'][1]['inflictedcasualties']
        except TypeError:
            print("inflictedcasualties is none")
        try:
            all_teams[entrenador_fuera]['cas_contra']+=match['teams'][0]['inflictedcasualties'] 
        except TypeError:
            print("inflictedcasualties is none")            
        scoring_points_fuera = 0
        if match['teams'][1]['score'] ==  match['teams'][0]['score']:
            all_teams[entrenador_fuera]['empates']+=1
            scoring_points_fuera = 0.5
        if match['teams'][1]['score'] <  match['teams'][0]['score']:
            all_teams[entrenador_fuera]['derrotas']+=1
        if match['teams'][1]['score'] >  match['teams'][0]['score']:
            all_teams[entrenador_fuera]['victorias']+=1
            scoring_points_fuera = 1

        if 'pdm' in str(match['teams'][0]['teamname']).lower():
            teams[entrenador_casa] = all_teams[entrenador_casa]
        if 'pdm' in str(match['teams'][1]['teamname']).lower():
            teams[entrenador_fuera] = all_teams[entrenador_fuera]

baseDir = f"{root_path}/arena/"

with open(f"{baseDir}{ID}.json", 'w', encoding='utf-8') as f:
    json.dump(teams, f, ensure_ascii=False, indent=4)


