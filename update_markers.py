import parse_text
import sqlite3
import codecs

count = 0

fhand = codecs.open('markers.js', 'w', "utf-8")
fhand.write("markersList = [\n")

conn = sqlite3.connect('de_olho_na_fila.sqlite')
cur = conn.cursor()

cur.execute('''
SELECT
 	Postos.nome,
 	Postos.endereco,
	TipoPosto.tipos,
	Postos.lat,
	Postos.lng,
 	StatusFila.atualizado,
	StatusFila.fila,
	StatusFila.status_posto,
	Vacinas.disponibilidade
FROM Postos JOIN StatusFila JOIN Vacinas JOIN TipoPosto
ON Postos.fila_id = StatusFila.id
AND Postos.vacina_id = Vacinas.id
AND Postos.tipo_posto_id = TipoPosto.id
''')
conn.commit()
dbstatus = cur.fetchall()

for row in dbstatus:
	posto = row[0]
	endereco = row[1]
	tipo_posto = row[2]
	lat = row[3]
	lng = row[4]
	atualizado = row[5]
	status_id = row[6]
	status = row[7]
	disponibilidade = row[8]

	try:
		count = count + 1
		if count > 1:
			fhand.write(",\n")
		output = "[{lat:" + str(lat) + ",lng:" + str(lng) + "}, '" + str(status_id) + "', '" + posto + "', '" + atualizado + "', '" + status + "', '" + disponibilidade + "', '" + tipo_posto + "']"
		fhand.write(output)
	except:
		continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to markers.js")

# markers = [ 
# [{lat,lng}, 'status_id', 'posto', 'atualizado', 'status', 'disponibilidade', 'tipo_posto'],...]
