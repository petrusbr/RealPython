import sqlite3

conn = sqlite3.connect("novo.db")

cursor = conn.cursor()

try:
	cursor.execute("""INSERT INTO populations VALUES
	     ('Rio de Janeiro', 'RJ', 9000000)
	      """)

	cursor.execute("""INSERT INTO populations VALUES
	     ('Sao Paulo', 'SP', 16000000)
	      """)
except sqlite3.OperationalError as e:
	print "Oops!"
	print "SQL error: {}".format(e.args)
finally:
	print "Encerrando a conexao..."
	conn.close()
	print "Conexao encerrada. Adeus."