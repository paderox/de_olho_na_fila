import parse_text_noDB
import json
import codecs

count = 0

parsed_data = json.loads(open('parsed_data.json', encoding='utf8').read())

fhand = codecs.open('markers_noDB.js', 'w', "utf-8")

fhand.write("markersList = [\n")

for entry in parsed_data:
	posto = entry['nome']
	endereco = entry['endereco']
	tipo_posto = entry['tipo_posto']
	lat = entry['coords']['lat']
	lng = entry['coords']['lng']
	atualizado = entry['atualizado']
	status_id = entry['status_id']
	status = entry['status_fila']
	disponibilidade = entry['disponibilidade']

	try:
		count = count + 1
		if count > 1:
			fhand.write(",\n")
		
		output = "[{lat:" + str(lat) + ",lng:" + str(lng) + "}, '" + str(status_id) + "', '" + posto + "', '" + atualizado + "', '" + status + "', '" + disponibilidade + "', '" + tipo_posto + "']"
		fhand.write(output)
	
	except:
		continue

fhand.write("\n];\n")
fhand.close()

print(count, "records written to markers_noDB.js")

# markers = [ 
# [{lat,lng}, 'status_id', 'posto', 'atualizado', 'status', 'disponibilidade', 'tipo_posto'],...]
