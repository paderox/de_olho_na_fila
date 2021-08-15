import update_raw_data
import json
import sqlite3
import get_geoloc

conn = sqlite3.connect('de_olho_na_fila.sqlite')
cur = conn.cursor()

json_data = json.loads(open('raw_data.json', encoding='utf8').read())

for entry in json_data:
    nome_posto = entry['equipamento']
    endereco = entry['endereco']
    id_posto = entry['id_tb_unidades']
    tipo_posto = entry['tipo_posto']
    id_tipo_posto = entry['id_tipo_posto']
    distrito = entry['distrito']
    id_distrito = entry['id_distrito']
    crs = entry['crs']
    id_crs = entry['id_crs']
    data_hora = entry['data_hora']
    status_posto = entry['status_fila']
    fila = entry['indice_fila']
    coronavac = entry['coronavac']
    astrazeneca = entry['astrazeneca']
    pfizer = entry['pfizer']

    if coronavac == '0' and astrazeneca == '0' and pfizer == '0':
        id_vacina = 1
    elif coronavac == '1' and astrazeneca == '0' and pfizer == '0':
        id_vacina = 2
    elif coronavac == '0' and astrazeneca == '0' and pfizer == '1':
        id_vacina = 3
    elif coronavac == '0' and astrazeneca == '1' and pfizer == '0':
        id_vacina = 4
    elif coronavac == '1' and astrazeneca == '0' and pfizer == '1':
        id_vacina = 5
    elif coronavac == '1' and astrazeneca == '1' and pfizer == '0':
        id_vacina = 6
    elif coronavac == '0' and astrazeneca == '1' and pfizer == '1':
        id_vacina = 7
    elif coronavac == '1' and astrazeneca == '1' and pfizer == '1':
        id_vacina = 8

    if (id_posto is None):
        print('id posto None for', endereco)
        continue
    else:    
        cur.execute('INSERT OR REPLACE INTO CRSs (id, nome) VALUES ( ?, ? )', ( id_crs, crs) )
        cur.execute('INSERT OR REPLACE INTO Distritos (id, distrito) VALUES ( ?, ? )', ( id_distrito, distrito) )
        cur.execute('INSERT OR REPLACE INTO StatusFila (posto_id, atualizado, fila, status_posto, checker) VALUES ( ?, ?, ?, ?, ? )', ( id_posto, data_hora, fila, status_posto, str(id_posto + data_hora + fila + status_posto)) )
        cur.execute('INSERT OR REPLACE INTO TipoPosto (id, tipos) VALUES ( ?, ? )', ( id_tipo_posto, tipo_posto) )
        conn.commit()

        cur.execute('SELECT id FROM StatusFila WHERE atualizado = ? AND fila = ? AND status_posto = ? ORDER BY atualizado DESC LIMIT 1', (data_hora, fila, status_posto))
        id_fila = cur.fetchone()[0]

        cur.execute('SELECT geodata, endereco FROM Postos WHERE id = ?', (id_posto,))
        try:
            response = cur.fetchone()
            geodata = response[0]
            enderecoDB = response[1]
            if geodata is None or geodata == '' or geodata == 'None':
                exists = False
            else:
                exists = True
            if not (enderecoDB is None or enderecoDB == '' or enderecoDB == 'None'):
                endereco = enderecoDB
        except:
            exists = False
        
        if exists == True:
            # como já existe linha, devemos apenas atualizar campos relevantes para fila:
            cur.execute('''
            UPDATE Postos
            SET
                fila_id = ?,
                vacina_id = ?
            WHERE
                id = ?
            ''', ( int(id_fila), int(id_vacina), int(id_posto) ))
            conn.commit()
        elif exists == False:
            # como é uma linha nova devemos buscar o geocoding e depois criar a linha:
            try:
                print('getting geocoding for:', endereco)
                geo = get_geoloc.geocoding(endereco)
                lat = geo["results"][0]["geometry"]["location"]["lat"]
                lng = geo["results"][0]["geometry"]["location"]["lng"]
                endereco = str(geo["results"][0]["formatted_address"])
            except:
                try:
                    print('getting geocoding for:', nome_posto)
                    geo = get_geoloc.geocoding(nome_posto)
                    lat = geo["results"][0]["geometry"]["location"]["lat"]
                    lng = geo["results"][0]["geometry"]["location"]["lng"]
                    endereco = str(geo["results"][0]["formatted_address"])
                except:
                    print('error when getting:', endereco, 'and:', nome_posto)
                    geo = lat = lng = None
            try:
                cur.execute('''
                INSERT OR REPLACE INTO Postos
                    (id, nome, endereco, fila_id, tipo_posto_id, distrito_id, crs_id, vacina_id, geodata, lat, lng)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
                ''', ( id_posto, nome_posto, endereco, id_fila, id_tipo_posto, id_distrito, id_crs, id_vacina, str(geo), lat, lng ))
                conn.commit()
                print('inserted in SQLite:', endereco)
            except:
                print('error when writing address:', endereco)
        else:
            print('error')

conn.close()
print('finished parsing text, getting geocoding and updating vaccine status')