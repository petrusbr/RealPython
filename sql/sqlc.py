import sqlite3

with sqlite3.connect("novo.db") as conn:
	c = conn.cursor()

	cidades = [
	           ('Belo Horizonte', 'MG', 4567899),
	           ('Curitiba', 'PR', 3200145),
	           ('Porto Alegre', 'RS', 2604123),
	           ('Vitoria', 'ES', 1400000)]
	c.executemany('INSERT INTO population VALUES(?, ?, ?)', cidades)
