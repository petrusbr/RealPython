import sqlite3

with sqlite3.connect("cars.db") as connection:
    
    connection.execute("""CREATE TABLE inventory (make TEXT, model TEXT, quantity INTEGER) """)

"""
Outra opção é fazer a conexão com o banco sem a cláusula WITH
conn = sqlite3.connect("DB.db")
cursor = conn.cursor()
cursor.execute("QUERY")
"""
