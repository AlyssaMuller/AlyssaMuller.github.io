# CALL BY curl -i http://localhost:8080/path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from chocolatesDB import ChocolatesDB, UsersDB
from socketserver import ThreadingMixIn
from http import cookies
from session_store import SessionStore
from passlib.hash import bcrypt
import sys
import json

SESSION_STORE = SessionStore()  # global


class MyRequestHandler(BaseHTTPRequestHandler):
    # instantiated once per request

    def loadCookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:  # to avoid error, create empty cookie object if no cookie in header yet
            self.cookie = cookies.SimpleCookie()

    def sendCookies(self):
        for morsel in self.cookie.values():
            morsel["samesite"] = "None"  # Prevents postMan
            morsel["secure"] = True
            # for any cookies, send as a header string
            self.send_header("Set-Cookie", morsel.OutputString())

    def loadSessionData(self):  # getLosGalletas
        self.loadCookie()  # load cookie info
        cookies = self.cookie  # cookie dict
        if "sessionID" in cookies:  # check if cookie session id exists
            # load sessionID from session store
            sessionID = self.cookie["sessionID"].value
            self.sessionData = SESSION_STORE.loadSessionData(
                sessionID)  # loadSessionData
            # if not cookie session data/not loaded correctly by server (eg server down)
            if self.sessionData == None:
                self.newSessionData()
        else:  # if no cookie session ID
            self.newSessionData()
        print("MY SESSION DATA:", self.sessionData)

    def newSessionData(self):  # if cookie session data empty or no cookie
        newSessionID = SESSION_STORE.createSession()  # create new cookie sessionID
        self.sessionData = SESSION_STORE.loadSessionData(
            newSessionID)  # get session data
        self.cookie["sessionID"] = newSessionID  # set cookie

        print("NewSessionID: ", newSessionID)
        print("self.sessionData: ", self.sessionData)
        print("\n self.cookie: ", self.cookie["sessionID"])
        print("\n")

    def handleCreateUser(self):
        parsed_body = self.parseRequest()
        # key name is specified by client
        first_name = parsed_body['first_name'][0]
        last_name = parsed_body['last_name'][0]
        email = parsed_body['email'][0]
        password = parsed_body['password'][0]
        db = UsersDB()
        if db.getUserByEmail(email) != None:
            self.handle422()
            return
        encrypted_password = bcrypt.hash(password)
        db.createUser(first_name, last_name, email, encrypted_password)
        # respond with success
        self.handleSuccessCreated()  # 201:created ok

    def handleCreateAuthenticatedSession(self):
        parsed_body = self.parseRequest()
        email = parsed_body['email'][0]
        password = parsed_body['password'][0]
      # step1: find a user in the db with the given email
        db = UsersDB()
        user = db.getUserByEmail(email)
        print(user)
        if user != None:  # If valid user record found
            # step2: compare given password to the encrypted psswd
            print("made it to user not none")
            if bcrypt.verify(password, user["encrypted_password"]):
                print("made it after bcrypt")
                # remember user's authenticated state
                self.sessionData["userID"] = user["id"]
                self.handleSuccessCreated()  # success 201

            else:
                self.handleNotAuthorized()
        else:
            self.handleNotAuthorized()

    def handleRetrieveUser(self, member_id):
        db = UsersDB()
        member = db.getOneUser(member_id)
        if member:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(member), "utf-8"))
        else:
            self.handleNotFound()

    # Chocolates

    def handleListChocolates(self):
        if "userID" not in self.sessionData:
            self.handleNotAuthorized()
            return
        # write to 'wfile'(aka response body/output stream) with text as bytes
        db = ChocolatesDB()
        allRecords = db.getAllChocolates()
        self.send_response(200)  # 200:ok status code
        # os bytes are read as text
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(allRecords), "utf-8"))

    def handleRetrieveChocolate(self, member_id):
        if "userID" not in self.sessionData:
            self.handleNotAuthorized()
            return
        db = ChocolatesDB()
        member = db.getOneChocolate(member_id)

        if member:
            self.send_response(200)  # 200:ok
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(member), "utf-8"))
        else:
            self.handleNotFound()

    def handleCreateChocolate(self):
        if 'userID' not in self.sessionData:
            self.handleNotAuthorized()
            return
        parsed_body = self.parseRequest()

        # 4 append new chocolate to list above (chocolateS)
        # if key doesn't exist in client input, python will be mad
        # key name is specified by client

        chocolate_name = parsed_body["name"][0]
        chocolate_flavor = parsed_body["flavor"][0]
        chocolate_price = parsed_body["price"][0]
        chocolate_size = parsed_body["size"][0]
        chocolate_description = parsed_body["description"][0]
        chocolate_rating = parsed_body["rating"][0]
        # chocolateS.append(chocolate_name)
        # db = ChocolateDB('chocolates.db')
        db = ChocolatesDB()
        db.createChocolate(chocolate_name, chocolate_flavor, chocolate_price,
                           chocolate_size, chocolate_description, chocolate_rating)

        # respond with success
        self.send_response(201)  # 201:created ok
        self.end_headers()

    def handleUpdateChocolate(self, member_id):
        if 'userID' not in self.sessionData:
            self.handleNotAuthorized()
            return
        parsed_body = self.parseRequest()

        chocolate_name = parsed_body["name"][0]
        chocolate_flavor = parsed_body["flavor"][0]
        chocolate_price = parsed_body["price"][0]
        chocolate_size = parsed_body["size"][0]
        chocolate_description = parsed_body["description"][0]
        chocolate_rating = parsed_body["rating"][0]

        db = ChocolatesDB()
        chocolateExists = db.getOneChocolate(member_id)

        if chocolateExists:
            db.updateChocolate(member_id, chocolate_name, chocolate_flavor, chocolate_price,
                               chocolate_size, chocolate_description, chocolate_rating)

            self.send_response(200)  # 200: ok
            self.end_headers()
        else:
            self.handleNotFound()

    def handleDeleteChocolate(self, member_id):
        if 'userID' not in self.sessionData:
            self.handleNotAuthorized()
            return
        db = ChocolatesDB()
        chocolateExists = db.getOneChocolate(member_id)

        if chocolateExists:
            db.deleteChocolate(member_id)
            self.send_response(200)  # 200: ok
            self.end_headers()
        else:
            self.handleNotFound()

    # Status Handlers

    def handleSuccessCreated(self):
        self.send_response(201)  # Success created
        self.end_headers()
        self.wfile.write(bytes("Success!", "utf-8"))

    def handleNotAuthorized(self):
        self.send_response(401)  # notAuthorized
        self.end_headers()
        self.wfile.write(bytes("Not Authorized", "utf-8"))

    def handleNotFound(self):
        self.send_response(404)  # 404: Not Found
        self.end_headers()
        self.wfile.write(bytes("Resource not found", "utf-8"))

    def handle422(self):
        self.send_response(422)  # 422: Unprocessable
        self.end_headers()
        self.wfile.write(bytes("Resource not found", "utf-8"))

    # handle any GET request
    def do_GET(self):  # do_METHOD is naming convention of handling methods
        self.loadSessionData()
        print("The request path is: ", self.path)
        path_parts = self.path.split("/")
        collection_name = path_parts[1]

        if len(path_parts) > 2:
            member_id = path_parts[2]
        else:
            member_id = None

        if collection_name == "chocolates":
            if member_id == None:
                self.handleListChocolates()
            else:
                self.handleRetrieveChocolate(member_id)

        elif collection_name == "users":
            if member_id == None:
                self.handleNotFound()
            else:
                self.handleRetrieveUser(member_id)

        else:
            # 404 response
            self.handleNotFound()

    # handle POST requests
    def do_POST(self):
        self.loadSessionData()
        if self.path == "/chocolates":
            self.handleCreateChocolate()
        elif self.path == "/users":
            self.handleCreateUser()

        elif self.path == "/sessions":
            self.handleCreateAuthenticatedSession()
        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.loadSessionData()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        self.loadSessionData()
        print("The request path is: ", self.path)

        path_parts = self.path.split("/")
        collection_name = path_parts[1]

        if len(path_parts) > 2:
            member_id = path_parts[2]
        else:
            member_id = None

        if collection_name == "chocolates" and member_id is not None:
            self.handleDeleteChocolate(member_id)
        elif collection_name == "users" and member_id is not None:
            self.handleDeleteUser(member_id)
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.loadSessionData()
        print("The request path is: ", self.path)

        path_parts = self.path.split("/")
        collection_name = path_parts[1]

        if len(path_parts) > 2:
            member_id = path_parts[2]
        else:
            member_id = None

        if collection_name == "users" and member_id is not None:
            self.handleUpdateChocolate(member_id)

        elif collection_name == "users" and member_id is not None:
            self.handleUpdateUser(member_id)

        else:
            self.handleNotFound()

# end headers
    def end_headers(self):
        self.sendCookies()  # send cookie header before ending headers
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        super().end_headers()

    def parseRequest(self):
        # capture user input from Client Request
        # read the content length of the 'rfile' request header
        length = self.headers["Content-Length"]
        # read from rfile request body
        request_body = self.rfile.read(int(length)).decode(
            "utf-8")  # read bytes, decode
        print("the raw request body: ", request_body)
        # parse the urlencoded urlrequest body
        parsed_body = parse_qs(request_body)
        print("the parsed request body: ", parsed_body)
        return parsed_body


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass  # inheritance only


def run():
    db=ChocolatesDB()
    db.createChocolatesTable()
    db=None #disconnect

    port=8080
    if len(sys.argv)>1:
        #if running on Heroku
        port=int(sys.argv[1]) #use cmd line input args

    listen = ("0.0.0.0", port)  # server & port # Listen all the time (port "0.0.0.0")
    server = ThreadedHTTPServer(listen, MyRequestHandler)

    print("Server Running!")
    server.serve_forever()


if __name__ == "__main__":
    run()
