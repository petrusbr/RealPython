import sqlite3

conn = sqlite3.connect("novo.db")

cursor = conn.cursor()

for r in cursor.execute("""SELECT * from population"""):
    # Imprime com o caractere 'u' de UNICODE
    print r

cursor.execute("""SELECT * from population""")
result = cursor.fetchall()

for r in result:
    # Imprime somente os valores, removendo o 'u' do UNICODE
    print r[0], r[1]

conn.close()