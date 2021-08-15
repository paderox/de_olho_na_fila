import update_raw_data
import json
import get_geoloc

json_data = json.loads(open('raw_data.json', encoding='utf8').read())
parsed_data = json.loads(open('parsed_data.json', encoding='utf8').read())

for entry in json_data:
    old = False
    nome_posto = entry['equipamento']
    endereco = entry['endereco']
    id_posto = entry['id_tb_unidades']
    tipo_posto = entry['tipo_posto']
    data_hora = entry['data_hora']
    status_posto = entry['status_fila']
    status_id = entry['indice_fila']
    coronavac = entry['coronavac']
    astrazeneca = entry['astrazeneca']
    pfizer = entry['pfizer']

    if coronavac == '1':
        disponibilidade = 'coronavac'
        if pfizer == '1':
            disponibilidade = disponibilidade + ' + pfizer'
            if astrazeneca == '1':
                disponibilidade = disponibilidade + ' + astrazeneca'
    elif pfizer == '1':
        disponibilidade = 'pfizer'
        if astrazeneca == '1':
            disponibilidade = disponibilidade + ' + astrazeneca'
    elif astrazeneca == '1':
        disponibilidade = 'astrazeneca'
    else:
        disponibilidade = 'nenhuma'
    
    if (id_posto is None):
        print('id posto None for', endereco)
        continue
    else:
        postoInfo = {
            'id_posto': id_posto,
            'nome': nome_posto,
            'endereco': endereco,
            'status_id': status_id,
            'atualizado': data_hora,
            'status_fila': status_posto,
            'disponibilidade': disponibilidade,
            'tipo_posto': tipo_posto
        }

        
        # search in parsed_data for this 'posto'
        # if it is there, update 'fila' info
        # if it is not there, search for geocoding and add to postoInfo
        try:
            for record in parsed_data:
                if record['id_posto'] == postoInfo['id_posto']:
                    record['status_id'] = postoInfo['status_id']
                    record['atualizado'] = postoInfo['atualizado']
                    record['status_fila'] = postoInfo['status_fila']
                    record['disponibilidade'] = postoInfo['disponibilidade']
                    old = True
                    break
        except:
            continue

        if old is False:
            # enrich postoInfo with lat and lng and update address entry:
            try:
                print('getting geocoding from:', endereco)
                geo = get_geoloc.geocoding(endereco)
                lat = geo["results"][0]["geometry"]["location"]["lat"]
                lng = geo["results"][0]["geometry"]["location"]["lng"]
                endereco = str(geo["results"][0]["formatted_address"])
            except:
                print('error getting geocoding from:', endereco)
                try:
                    print('getting geocoding from:', nome_posto)
                    geo = get_geoloc.geocoding(nome_posto)
                    lat = geo["results"][0]["geometry"]["location"]["lat"]
                    lng = geo["results"][0]["geometry"]["location"]["lng"]
                    endereco = str(geo["results"][0]["formatted_address"])
                except:
                    print('error when getting geocoding from:', endereco, 'and:', nome_posto)
                    geo = lat = lng = None
            updt = {
                'endereco': endereco,
                'coords':{
                    'lat': lat,
                    'lng': lng
                }
            }
            postoInfo.update(updt)

            # append postoInfo to record:
            parsed_data.append(postoInfo)

with open('parsed_data.json', 'w', encoding='utf8') as outfile:
    json.dump(parsed_data, outfile, ensure_ascii=False)

print('finished parsing text, getting geocoding and updating vaccine status')