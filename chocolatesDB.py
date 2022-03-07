import sqlite3


def dict_factory(cursor, row):  # dictionary function
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ChocolatesDB:
    def __init__(self):
        self.conn = sqlite3.connect("chocolates.db")
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        exe = self.cur.execute

    def getAllChocolates(self):
        self.cur.execute("SELECT * from CHOCOLATES")
        return self.cur.fetchall()

    def getOneRestaurant(self, chocolate_id):
        data = [chocolate_id]
        self.cur.execute(
            "SELECT * FROM CHOCOLATES WHERE id=?", data)
        return self.cur.fetchone()

    # all other chocolate insert fields(5 for assignment)
    def createRestaurant(self, name, flavor, price, size, description, rating):
        data = [name, flavor, price, size, description, rating]
        self.cur.execute(
            "INSERT into CHOCOLATES(name, flavor, price,size,description, rating) VALUES (?,?,?,?,?,?)", data)
        self.conn.commit()

    # all the chocolate fields. similar to combining getOneRestaurant+ createRestaurant
    def updateRestaurant(self, chocolateID, chocolateName, chocolateFlavor, chocolatePrice, chocolateSize, chocolateDescription, chocolateRating):
        data=[chocolateID, chocolateName, chocolateFlavor, chocolatePrice,
            chocolateSize, chocolateDescription, chocolateRating]
        self.cur.execute(
            "UPDATE from CHOCOLATES SET name=?, cuisine=?, rating=? WHERE id=?", data)
        self.conn.commit()

    def deleteRestaurant(self, chocolateID):
        data=[id]
        self.cur.execute("DELETE from CHOCOLATES WHERE id=?", data)
        self.conn.commit()


# self.cur.execute("SELECT * from chocolates")
# print(self.cur.fetchall())
