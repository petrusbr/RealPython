import sqlite3

conn = sqlite3.connect("novo.db")

cursor = conn.cursor()

cursor.execute("""INSERT INTO population VALUES
	     ('Rio de Janeiro', 'RJ', 9000000)
	      """)

cursor.execute("""INSERT INTO population VALUES
	     ('Sao Paulo', 'SP', 16000000)
	      """)

conn.commit()
conn.close()