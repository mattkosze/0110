import json
import random
from Classes.schemas import *
from Classes.simulant import Simulant

class Platform:
    def __init__(self, pData=None, pUsers=None):
        # Communities will be stored in a dict k:v format where a unique ID (key) corresponds to a community class object (value)
        self.communities = {}
        # Platform users will be stored as set format containing user ids
        self.users = {}

        # NOTE: May opt to make both necessary, as there's likely no situation in which these shouldn't be loaded
        if pData:
            self.populateWebsite(pData)
        if pUsers:
            self.populateUsers(pUsers)

    # <----------------- Object population functions ----------------->

    # Loads in community and post data from a data store json file
    def populateWebsite(self, jsonData):
        with open(jsonData, "r") as file:
            data = json.load(file)

        for gID in data:
            entry = data[gID]

            id = gID
            name = entry["name"]
            desc = entry["desc"]

            postsRaw = entry["posts"]
            posts = self.populatePosts(postsRaw)

            members = set(entry["members"])
            
            comm = Community(id, name, desc, posts, members)
            self.communities[gID] = comm

    def populatePosts(self, pData):
        posts = {}

        for pID in pData:
            entry = pData[pID]

            id = pID
            author = entry["author"]
            title = entry["title"]
            content = entry["content"]
            upvotes = entry["votes"][0]
            downvotes = entry["votes"][1]
            comments = self.populateComments(entry["comments"][1])

            post = Post(id, author, title, content, upvotes, downvotes, comments)

            posts[pID] = post

        return posts

    def populateComments(self, cData):
        comments = {}

        for cID in cData:
            entry = cData[cID]

            id = cID
            author = entry["author"]
            content = entry["content"]
            upvotes = entry["votes"][0]
            downvotes = entry["votes"][1]
            
            hasReplies = entry["replies"][0]
            replies = entry["replies"][1]

            if hasReplies:
                replies = self.populateReplies(replies, id)
                comment = Comment(id, author, content, upvotes, downvotes, hasReplies, replies)
            else:
                comment = Comment(id, author, content, upvotes, downvotes)

            comments[cID] = comment

        return comments 


    def populateReplies(self, rData, parentID):
        replies = {}

        for rID in rData:
            entry = rData[rID]

            id = rID
            author = entry["author"]
            content = entry["content"]
            upvotes = entry["votes"][0]
            downvotes = entry["votes"][1]

            isReply = True

            hasReplies = entry["replies"][0]
            replies = entry["replies"][1]

            if hasReplies:
                replies = self.populateReplies(replies, id)
                reply = Comment(id, author, content, upvotes, downvotes, isReply, parentID, hasReplies, replies)
            else:
                reply = Comment(id, author, content, upvotes, downvotes, isReply, parentID)

            replies[rID] = reply

        return replies

    # Loads in user data from a data store json file
    def populateUsers(self, jsonData):
        with open(jsonData, "r") as file:
            data = json.load(file)

        for uID in data:
            
            entry = data[uID]

            community = self.communities

            id = uID
            name = entry["name"]
            bio = entry["bio"]
            karma = entry["karma"]
            contributions = entry["contributions"]
            posts = entry["posts"]
            replies = entry["replies"]
            personalBio = entry["personalBio"]

            simulant = Simulant(community, id, name, bio, karma, contributions, posts, replies, personalBio)

            self.users[id] = simulant

    # <----------------- Interaction functions ----------------->

    # Handles community creation
    def createCommunity(self, cName, cDesc):
        # Generate community ID
        while True:
            id = f"G{random.randint(0, 999):03d}"
            if id not in self.communities:
                break
        
        community = Community(id, cName, cDesc)

        self.communities[id] = community

    # Handles post creation within a community
    def createPost(self, cID, aID, title, content):
        # Generate post ID
        while True:
            id = f"P{random.randint(0, 99999):05d}"
            if id not in self.communities[cID].posts:
                break

        post = Post(id, aID, title, content)

        self.communities[cID].posts[id] = post

    def createComment(self):
        # Generate comment ID
        while True:
            id = f"G{random.randint(0, 999999):06d}"
            if id not in self.communities:
                break

    # Helper function to get to selected reply level
    def traverseTo(self, gID, rAccess=None):
        if gID[0] == "R":
            if len(gID) > 6:
                locate = rAccess.replies
                traverse
        elif gID[0] == "P":
            pass
        else:
            pass
        
# GID: G123P12345R123456R789012
 
    # <----------------- Shutdown functions   ----------------->
    # LEAVING THIS FOR LAST, SHUTDOWN FUNCTIONS DEPEND ON ALL PREVIOUS INFO

    # Saves data to corresponding json files 
    def exportWebsite(self):
        pass
    
    # Orchastrate platform saving and shutdown
    def shutdown(self):
        pass