import json
from schemas import *

class Platform:
    def __init__(self, pData=None, pUsers=None):
        # Communities will be stored in a dict k:v format where a unique ID (key) corresponds to a community class object (value)
        self.communities = {}
        # Platform users will be stored as set format containing user ids
        self.users = {1, 2}

        # NOTE: May opt to make both necessary, as there's likely no situation in which these shouldn't be loaded
        if pData:
            self.populateWebsite(pData)
        if pUsers:
            self.populateUsers(pUsers)

    # <----------------- Object population functions ----------------->

    # Loads in community and post data from a data store json file
    def populateWebsite(self, jsonData):
        with open(jsonData, "r") as file:
            parsedData = json.loads(file)
        for i in parsedData:
            id, name, desc, posts, members = i, parsedData[i]["name"], parsedData[i]["desc"], 
            comm = Community(id, name, desc, posts, members)
            self.communities[i] = comm

    # Loads in user data from a data store json file
    def populateUsers(self, uData):
        pass

    # <----------------- Interaction functions ----------------->

    # Handles community creation
    def createCommunity(self, cName, cDesc):
        pass

    # Handles post creation within a community
    def createPost(self):
        pass

    # <----------------- Shutdown functions   ----------------->
    # LEAVING THIS FOR LAST, SHUTDOWN FUNCTIONS DEPEND ON ALL PREVIOUS INFO

    # Saves data to corresponding json files 
    def exportWebsite(self):
        pass
    
    # Orchastrate platform saving and shutdown
    def shutdown(self):
        pass