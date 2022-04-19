import os
import psycopg2
import psycopg2.extras
import urllib.parse


def dict_factory(cursor, row):  # dictionary function
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class ChocolatesDB:
    def __init__(self): #constructor
        #self.connection = sqlite3.connect("chocolates.db")
        #self.connection.row_factory = dict_factory
        urllib.parse.uses_netloc.append("postgres")
        url=urllib.parse.urlparse(os.environ["DATABASE_URL"])
        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cursor = self.connection.cursor()

    def __del__(self): #destructer
        self.connection.close()

    def createUsersTable(self):
        createTable="CREATE TABLE IF NOT EXISTS USERS(id SERIAL PRIMARY KEY, first_name text, last_name text, email text, encrypted_password text)"
        self.cursor.execute(createTable)
        self.connection.commit()

    def createChocolatesTable(self): #createNewSchema
        createTable="CREATE TABLE IF NOT EXISTS CHOCOLATES(id SERIAL PRIMARY KEY, name text, size text, flavor text, price text, description text, rating INTEGER)"
        self.cursor.execute(createTable)
        self.connection.commit()

    def getAllChocolates(self):
        self.cursor.execute("SELECT * from CHOCOLATES")
        return self.cursor.fetchall()

    def getOneChocolate(self, chocolate_id):
        data = [chocolate_id]
        self.cursor.execute("SELECT * FROM CHOCOLATES WHERE id=%s", data)
        return self.cursor.fetchone()

    # all other chocolate insert fields(5 for assignment)
    def createChocolate(self, name, flavor, price, size, description, rating):
        data = [name, flavor, price, size, description, int(rating)]
        self.cursor.execute(
            "INSERT into CHOCOLATES (name, flavor, price, size, description, rating) VALUES (%s,%s,%s,%s,%s,%s)", data)
        self.connection.commit()

    # all the chocolate fields. similar to combining getOneRestaurant+ createRestaurant
    def updateChocolate(self, chocolateID, name, flavor, price, size, description, rating):
        data = [name, flavor, price, size,
                description, int(rating), chocolateID]
        self.cursor.execute(
            "UPDATE CHOCOLATES SET name = %s, flavor = %s, price = %s, size = %s, description = %s, rating = %s WHERE id=%s", data)
        self.connection.commit()

    def deleteChocolate(self, chocolateID):
        data = [chocolateID]
        self.cursor.execute("DELETE from CHOCOLATES WHERE id=%s", data)
        self.connection.commit()


class UsersDB:
    def __init__(self):
        self.connection = sqlite3.connect("chocolates.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def createUser(self, first_name, last_name, email, encrypted_password):
        data = [first_name, last_name, email, encrypted_password]
        self.cursor.execute(
            "INSERT into USERS (first_name, last_name, email, encrypted_password) VALUES (%s,%s,%s,%s)", data)
        self.connection.commit()

    def getAllUsers(self):
        self.cursor.execute("SELECT * from USERS")
        return self.cursor.fetchall()

    def getUserByEmail(self, email):
        data = [email]
        self.cursor.execute("SELECT * FROM USERS WHERE email=%s", data)
        return self.cursor.fetchone()

    def getOneUser(self, user_id):
        data = [user_id]
        self.cursor.execute("SELECT * FROM USERS WHERE id=%s", data)
        return self.cursor.fetchone()

    def updateUser(self, first_name, last_name, email, password):
        data = [first_name, last_name, password, email]
        self.cursor.execute(
            "UPDATE USERS SET first_name=%s, last_name=%s, encrypted_password=%s, WHERE email=%s", data)
        self.connection.commit()

    def deleteUser(self, email):
        data = [email]
        self.cursor.execute("DELETE from USERS WHERE email=%s", data)
        self.connection.commit()
