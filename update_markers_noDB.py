import parse_text_noDB
import json
import codecs

count = 0

parsed_data = json.loads(open('parsed_data.json', encoding='utf8').read())

fhand1 = codecs.open('markers_noDB.js', 'w', "utf-8")
fhand2 = codecs.open('C:/Users/lucas.padeiro/Desktop/Personal/Code/paderox.github.io/markers.js', 'w', "utf-8")

fhand1.write("markersList = [\n")
fhand2.write("markersList = [\n")

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
			fhand1.write(",\n")
			fhand2.write(",\n")
		output = "[{lat:" + str(lat) + ",lng:" + str(lng) + "}, '" + str(status_id) + "', '" + posto + "', '" + atualizado + "', '" + status + "', '" + disponibilidade + "', '" + tipo_posto + "']"
		fhand1.write(output)
		fhand2.write(output)
	except:
		continue

fhand1.write("\n];\n")
fhand2.write("\n];\n")
fhand1.close()
fhand2.close()

print(count, "records written to markers.js")
print(count, "records written to markers.js in website DB")

# markers = [ 
# [{lat,lng}, 'status_id', 'posto', 'atualizado', 'status', 'disponibilidade', 'tipo_posto'],...]
