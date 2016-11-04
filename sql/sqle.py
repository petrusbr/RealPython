# Updating and Deleting

import sqlite3

conn = sqlite3.connect("novo.db")
c = conn.cursor()

c.execute("UPDATE population SET population=1234905 WHERE city='Vitoria'")
conn.commit()

c.execute("DELETE from population WHERE city='Rio de Janeiro'")
conn.commit()

print "\nDados atualizados da tabela\n"

c.execute("SELECT * from population")
rows = c.fetchall()

for r in rows:
    print r[0], r[1], r[2]