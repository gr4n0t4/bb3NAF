 
import json
import pprint
import os
from flask import Flask, send_file, render_template
import math
from flask_caching import Cache
config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)

root_path = os.getenv("ROOT_PATH","/home/gr4n0t4/pdm")



@app.context_processor
def utility_processor():
    def get_race(id_race):
        razas = {
            1: "Humanos",
            2: "Enanos",
            3: "Skaven",
            4: "Orcos",
            5: "Hombres Lagarto",
            7: "Elfos Silvanos",
            8: "Caos",
            9: "Elfos Oscuros",
            10: "No muertos",
            14: "Union Elfica",
            17: "Nigromanticos",
            18: "Nurgle",
            22: "Underworld",
            24: "Nobleza Imperial",
            1000: "Orcos Negros",
            1001: "Renegados del Caos",
            1002: "Alianza del Viejo Mundo",
        }
        raza = "Desconocida"        
        try:
            raza = razas[id_race]
        except:
            pass
        return raza
    return dict(get_race=get_race)

@app.route("/pdm")
def naf_pdm():
    min_partidos = 10
    base_dir = f'{root_path}/data/naf'
    matches = []
    for file in os.listdir(f"{base_dir}/partidos"):
        if file.endswith('json'):
            json_path = os.path.join(f"{base_dir}/partidos", file)
            file = open(json_path)
            data = json.load(file)
            matches += data['matches']
            file.close()
    matches = sorted(matches, key=lambda x: x['started'], reverse=True)
    resultados = []
    for match in matches:       
        resultado = {}
        resultado['entrenador_casa'] = str(match['teams'][0]['teamname']) + " (" + str(match['coaches'][0]['coachname'])+ ")"
        resultado['entrenador_fuera'] =  str(match['teams'][1]['teamname']) + " (" + str(match['coaches'][1]['coachname'])+ ")"
        resultado['td_casa'] = match['teams'][0]['score']
        resultado['td_fuera'] = match['teams'][1]['score']
        resultado['cas_casa'] = match['teams'][0]['inflictedcasualties']
        resultado['cas_fuera'] = match['teams'][1]['inflictedcasualties']
        resultados.append(resultado)

    entrenadores = {}
    for file in os.listdir(f"{base_dir}/clasificacion"):
        if file.endswith('json'):
            json_path = os.path.join(f"{base_dir}/clasificacion", file)
            file = open(json_path)
            entrenadores = json.load(file)
            file.close()
        
    entrenadores_array = []
    num_entrenadores = []
    for key, value in entrenadores.items():
        entrenadores_array.append(value)
        if value['entrenador'] not in num_entrenadores and ((value['victorias'] + value['empates'] + value['derrotas']) >= min_partidos):
            num_entrenadores.append(value['entrenador'])
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['cas_contra'])
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['cas_favor'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['td_contra'])
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['td_favor'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['victorias'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: (x['victorias'] + x['empates'] + x['derrotas']))
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['puntos'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: (x['victorias'] + x['empates'] + x['derrotas']) >= min_partidos, reverse=True)


    n_clasificados = 4 
    if len(num_entrenadores) > 16:
        n_clasificados = 8
    if len(num_entrenadores) > 32:
        n_clasificados = 16
    clasificados = []
    elegibles = []
    for entrenador in entrenadores_array:
        if (entrenador['victorias'] + entrenador['empates'] + entrenador['derrotas']) >= min_partidos:
            if entrenador['entrenador'] not in clasificados and n_clasificados > 0:
                clasificados.append(entrenador['entrenador'])
                elegibles.append(entrenador['entrenador'])
                entrenador['clase'] = 'clasificado'
                n_clasificados -= 1
            elif entrenador['entrenador'] not in elegibles:
                elegibles.append(entrenador['entrenador'])
                entrenador['clase'] = 'elegible'
                

    return render_template('index.html', resultados=resultados, entrenadores=entrenadores_array, titulo="Open season 5", num_entrenadores=len(num_entrenadores), page=0, total=0)

@app.route("/pdm/csv")
def download_csv():
    base_dir = f'{root_path}/data/naf/partidos'
    matches = []
    for file in os.listdir(base_dir):
        if file.endswith('json'):
            json_path = os.path.join(base_dir, file)
            file = open(json_path)
            data = json.load(file)
            matches += data['matches']
            file.close()
    # Create a CSV string from the user data
    csv_data = "Entrenador Casa,Entrenador Visitante, TD Casa, TD Visitante, CAS Casa, CAS Visitante\n"
    for match in matches:
        if 'pdm' not in str(match['teams'][0]['teamname']).lower() and 'pdm' not in str(match['teams'][1]['teamname']).lower():
            continue
        csv_data += "{},{},{},{},{},{},\n".format(match['coaches'][0]['coachname'],match['coaches'][1]['coachname'],match['teams'][0]['score'],match['teams'][1]['score'],match['teams'][0]['inflictedcasualties'],match['teams'][1]['inflictedcasualties'])
 
    # Create a temporary CSV file and serve it for download
    with open("resultados.csv", "w") as csv_file:
        csv_file.write(csv_data)
     
    return send_file("resultados.csv", as_attachment=True)


@app.route("/pdm/all")
@cache.cached(timeout=3600)
def naf_all_root():
    return naf_all(page=0)

@app.route("/pdm/all/<page>")
@cache.cached(timeout=3600)
def naf_all(page=0):
    length = 1000
    base_dir = f'{root_path}/data/all'
    try:
        page=int(page)
    except ValueError:
        page = 0        
    entrenadores = {}
    for file in os.listdir(base_dir):
        if file.endswith('json'):
            json_path = os.path.join(base_dir, file)
            file = open(json_path)
            entrenadores = json.load(file)
            file.close()
        
    entrenadores_array = []
    num_entrenadores = []
    for key, value in entrenadores.items():
        entrenadores_array.append(value)
        if value['entrenador'] not in num_entrenadores:
            num_entrenadores.append(value['entrenador'])
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['cas_contra'])
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['cas_favor'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['td_contra'])
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['td_favor'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['victorias'], reverse=True)
    entrenadores_array=sorted(entrenadores_array, key=lambda x: (x['victorias'] + x['empates'] + x['derrotas']))
    entrenadores_array=sorted(entrenadores_array, key=lambda x: x['puntos'], reverse=True)
    total = math.floor(len(entrenadores_array)/length)

    return render_template('naf.html', resultados=[], entrenadores=entrenadores_array[page*length:][:length], titulo="Open season 5", num_entrenadores=len(num_entrenadores), page=page, total=total)
