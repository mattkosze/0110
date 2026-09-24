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
            data = json.loads(file)

        for gID in data:
            entry = data[gID]

            id = gID
            name = entry["name"]
            desc = entry["desc"]

            postsRaw = entry["posts"]
            posts = self.populatePosts(postsRaw)

            members = entry["members"]
            
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
            comments = self.populateComments()

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
                replies = self.populateComments(replies, id)
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