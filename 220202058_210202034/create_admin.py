import sqlite3

c = sqlite3.connect("mydatabase.db")
cur = c.cursor()

cur.execute("INSERT INTO admins(name,surname,email,password,birthdate,gender,phone,address) VALUES (?,?,?,?,?,?,?,?)",("admin","admin","admin@test.com","admin","admin","admin","admin","admin"))
c.commit()
c.close()
    