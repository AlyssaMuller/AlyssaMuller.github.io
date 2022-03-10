import sqlite3


def dict_factory(cursor, row):  # dictionary function
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ChocolatesDB:
    def __init__(self):
        self.connection = sqlite3.connect("chocolates.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def getAllChocolates(self):
        self.cursor.execute("SELECT * from CHOCOLATES")
        return self.cursor.fetchall()

    def getOneChocolate(self, chocolate_id):
        data = [chocolate_id]
        self.cursor.execute("SELECT * FROM CHOCOLATES WHERE id=?", data)
        return self.cursor.fetchone()

    # all other chocolate insert fields(5 for assignment)
    def createChocolate(self, name, flavor, price, size, description, rating):
        data = [name, flavor, price, size, description, int(rating)]
        self.cursor.execute(
            "INSERT into CHOCOLATES (name, flavor, price, size, description, rating) VALUES (?,?,?,?,?,?)", data)
        self.connection.commit()

    # all the chocolate fields. similar to combining getOneRestaurant+ createRestaurant
    def updateChocolate(self, chocolateID, name, flavor, price, size, description, rating):
        data = [name, flavor, price, size,
                description, int(rating), chocolateID]
        self.cursor.execute(
            "UPDATE CHOCOLATES SET name = ?, flavor = ?, price = ?, size = ?, description = ?, rating = ? WHERE id=?", data)
        self.connection.commit()

    def deleteChocolate(self, chocolateID):
        data = [chocolateID]
        self.cursor.execute("DELETE from CHOCOLATES WHERE id=?", data)
        self.connection.commit()


# self.cursor.execute("SELECT * from chocolates")
# print(self.cursor.fetchall())
