import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class SquirrelDB:

    def __init__(self):
        self.connection = sqlite3.connect("system_tests/squirrel_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def getSquirrels(self):
        self.cursor.execute("SELECT * FROM squirrels ORDER BY id")
        return self.cursor.fetchall()

    def getSquirrel(self, squirrelId):
        data = [squirrelId]
        self.cursor.execute("SELECT * FROM squirrels WHERE id = ?", data)
        return self.cursor.fetchone()

    def createSquirrel(self, name, size):
        data = [name, size]
        self.cursor.execute("INSERT INTO squirrels (name, size) VALUES (?, ?)", data)
        self.connection.commit()
        return None

    def updateSquirrel(self, squirrelId, name, size):
        data = [name, size, squirrelId]
        self.cursor.execute("UPDATE squirrels SET name = ?, size = ? WHERE id = ?", data)
        self.connection.commit()
        return None

    def deleteSquirrel(self, squirrelId):
        data = [squirrelId]
        self.cursor.execute("DELETE FROM squirrels WHERE id = ?", data)
        self.connection.commit()
        return None