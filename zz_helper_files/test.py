import sqlite3

con = sqlite3.connect('C:/Users/civy/Music/GitHub/jBeam/db.sqlite3')
cur = con.cursor()

cur.execute('SELECT * FROM beam_jBeamObject')
print(cur.fetchall())