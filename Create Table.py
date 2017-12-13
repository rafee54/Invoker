import sqlite3

conn = sqlite3.connect('spell.db')

c = conn.cursor()

c.execute('SELECT * FROM spells')

print(c.fetchall())
