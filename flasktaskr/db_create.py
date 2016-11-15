#project/db_create.py

#import sqlite3
#from _config import DATABASE_PATH

from project import db, bcrypt
from project.models import Task, User
from datetime import date

# Create the DB and the db table
db.create_all()

db.session.add(
	User(
		"admin", "admin@gov.us", 
		 bcrypt.generate_password_hash("admin"), 
		 "admin"
	)
)

# Insert dummy data
#db.session.add(Task("Terminar este tutorial", date(2017, 2, 1), 10, 
#                     date(2016, 11, 14), 1, 1))
#db.session.add(Task("Terminar Real Python 2", date(2017, 6, 30), 10, 
#                     date(2016, 11, 14), 1, 1))

db.session.commit()
