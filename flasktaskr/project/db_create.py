#project/db_create.py

import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

	c = connection.cursor()

	#Cria a tabela
	c.execute("""CREATE TABLE tasks(task_id INTEGER 
		PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
		due_date TEXT NOT NULL, priority INTEGER NOT NULL,
		status INTEGER NOT NULL)""")

	dummy_data = [
		("Terminar este tutorial", "10/12/2016", 10, 1),
		("Terminar o curso Real Python 2", "01/02/2017", 10, 1)]

	c.executemany("""INSERT INTO tasks (name, due_date, priority, status)
		VALUES(?, ?, ?, ?)""", dummy_data)
