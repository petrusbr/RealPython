# sql.py  - Cria uma tabela no banco de dados SQLite3 e a popula com dados aleatorios

import sqlite3

with sqlite3.connect("blog.db") as connection:
    
    c = connection.cursor()
    
    c.execute("""CREATE TABLE posts
             (title TEXT, post TEXT)
             """)
    
    # Insere dados dummy nas tabelas
    c.execute('INSERT INTO posts VALUES("Good", "I\'m good.")')
    c.execute('INSERT INTO posts VALUES("Bem", "I\'m well")')
    c.execute('INSERT INTO posts VALUES("Excelente", "Sinto-me excelente!")')
    c.execute('INSERT INTO posts VALUES("Okay", "Estou bao")')