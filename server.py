# CALL BY curl -i http://localhost:8080/path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from chocolatesDB import ChocolatesDB
from socketserver import ThreadingMixIn
import json


class MyRequestHandler(BaseHTTPRequestHandler):
    # instantiated once per request
    # All the code goes here

    def handleListChocolates(self):
        # send status code
        self.send_response(200)  # 200:ok
        # os bytes are read as text
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # write to 'wfile'(aka response body/output stream)
        # changes text to bytes
        # self.wfile.write(bytes(json.dumps(chocolateS), "utf-8"))
        db = ChocolatesDB()
        # db = ChocolatesDB()
        allRecords = db.getAllChocolates()
        self.wfile.write(bytes(json.dumps(allRecords), "utf-8"))

    def handleRetrieveChocolate(self, member_id):
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
        # capture user input from Client Request
        # 1)read the content legth of the 'rfile' request header
        length = self.headers["Content-Length"]

        # 2) read from rfile request body
        request_body = self.rfile.read(int(length)).decode(
            "utf-8")  # read bytes, decode
        print("the raw request body: ", request_body)

        # 3 parse the urlencoded urlrequest body
        parsed_body = parse_qs(request_body)
        print("the parsed request body: ", parsed_body)

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
        length = self.headers["Content-Length"]

        request_body = self.rfile.read(int(length)).decode("utf-8")
        print("the raw request body: ", request_body)

        parsed_body = parse_qs(request_body)
        print("the parsed request body: ", parsed_body)

        chocolate_name = parsed_body["name"][0]
        chocolate_flavor = parsed_body["flavor"][0]
        chocolate_price = parsed_body["price"][0]
        chocolate_size = parsed_body["size"][0]
        chocolate_description = parsed_body["description"][0]
        chocolate_rating = parsed_body["rating"][0]

        db = ChocolatesDB()
        db.updateChocolate(member_id, chocolate_name, chocolate_flavor, chocolate_price,
                           chocolate_size, chocolate_description, chocolate_rating)

        self.send_response(200)  # 200: ok
        self.end_headers()

    def handleDeleteChocolate(self, member_id):
        db = ChocolatesDB()
        chocolateExists = db.getOneChocolate(member_id)

        if chocolateExists:
            db.deleteChocolate(member_id)
            self.send_response(200)  # 200: ok
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

    def handleNotFound(self):
        self.send_response(404)  # 404: Not Found
        self.end_headers()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    # handle any GET request
    def do_GET(self):  # do_METHOD is naming convention of handling methods
        print("The request path is: ", self.path)
        path_parts = self.path.split("/")
        collection_name = path_parts[1]

        if len(path_parts) > 2:
            member_id = path_parts[2]
        else:
            member_id = None

        # print(path_parts)
        # print(collection_name)
        # print(member_id)

        if collection_name == "chocolates":
            if member_id == None:
                self.handleListChocolates()
            else:
                self.handleRetrieveChocolate(member_id)

        else:
            # 404 response
            self.handleNotFound()

    # handle POST requests
    def do_POST(self):
        if self.path == "/chocolates":
            self.handleCreateChocolate()
        else:
            self.handleNotFound()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_DELETE(self):
        print("The request path is: ", self.path)

        path_parts = self.path.split("/")
        collection_name = path_parts[1]

        if len(path_parts) > 2:
            member_id = path_parts[2]
        else:
            member_id = None
        if collection_name == "chocolates" and member_id is not None:
            self.handleDeleteChocolate(member_id)
        else:
            self.handleNotFound()

    def do_PUT(self):
        print("The request path is: ", self.path)

        path_parts = self.path.split("/")
        collection_name = path_parts[1]

        if len(path_parts) > 2:
            member_id = path_parts[2]
        else:
            member_id = None

        if collection_name == "chocolates" and member_id is not None:
            self.handleUpdateChocolate(member_id)
        else:
            self.handleNotFound()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass  # inheritance only


def run():
    listen = ("127.0.0.1", 8080)  # server & port #
    server = ThreadedHTTPServer(listen, MyRequestHandler)

    print("Server Running!")
    server.serve_forever()


if __name__ == "__main__":
    run()
