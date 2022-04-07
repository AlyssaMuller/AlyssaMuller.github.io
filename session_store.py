
import base64
import os


class SessionStore:
    # dict of dicts(session id to session data that matches up to the db)

    def __init__(self):
        # mData
        self.sessions = {}  # Dict of dict, one per session

    def generateSessionID(self):
        randInt = os.urandom(32)  # pick random number
        # convert random number to a string with other chars
        randStr = base64.b64encode(randInt).decode("utf-8")
        return randStr  # return resulting string

    def createSession(self):
        newSessionID = self.generateSessionID()
        self.sessions[newSessionID] = {}
        return newSessionID

    def loadSessionData(self, sessionID):
        if sessionID in self.sessions:  # if sessionID is in the dictionary, return, otherwise prevent a crash by returning None
            return self.sessions[sessionID]
        else:
            return None
