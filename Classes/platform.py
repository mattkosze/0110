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
        # Stores a list of posts in system for returning a feed
        self.postStore = {}

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

        for cID in data:
            entry = data[cID]

            id = cID
            name = entry["name"]
            desc = entry["desc"]

            postsRaw = entry["posts"]
            posts = self.populatePosts(postsRaw, cID)

            members = set(entry["members"])
            
            comm = Community(id, name, desc, posts, members)
            self.communities[cID] = comm

    def populatePosts(self, pData, cID):
        postList = {}

        for pID in pData:
            entry = pData[pID]

            id = pID
            gID = cID + pID
            author = entry["author"]
            title = entry["title"]
            content = entry["content"]
            upvotes = entry["votes"][0]
            downvotes = entry["votes"][1]
            replies = self.populateReplies(entry["replies"], gID)

            post = Post(id, gID, author, title, content, upvotes, downvotes, replies)

            postList[pID] = post
            self.postStore[gID] = post

        return postList

    def populateReplies(self, rData, tID):
        replyList = {}

        for id in rData:
            entry = rData[id]

            gID = tID + id
            author = entry["author"]
            content = entry["content"]
            upvotes = entry["votes"][0]
            downvotes = entry["votes"][1]

            replies = entry["replies"]
            hasReplies = (True if replies != {} else False) 

            if hasReplies:
                recReplies = self.populateReplies(replies, gID)
                reply = Reply(id, gID, author, content, upvotes, downvotes, recReplies)
            else:
                reply = Reply(id, gID, author, content, upvotes, downvotes)

            replyList[id] = reply

        return replyList

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

        return id

    # Handles post creation within a community
    def createPost(self, cID, aID, title, content):
        # Generate post ID
        while True:
            id = f"P{random.randint(0, 99999):05d}"
            if id not in self.communities[cID].posts:
                break

        gID = cID + id

        post = Post(id, gID, aID, title, content)

        self.communities[cID].posts[id] = post

        return gID

    # Handles reply creation within a post or reply
    def createReply(self, rID, aID, content):
        # Access top level comment being replied to
        replyTo = self.traverseTo(rID)

        # Generate reply ID, which varies for comments versus replies
        while True:
            id = f"R{random.randint(0, 999999):06d}"
            ## Check that it's not already at this level
            if id not in replyTo.replies:
                break

        gID = rID + id
        
        reply = Reply(id, gID, aID, content)

        replyTo.replies[id] = reply

        return gID

    # Handles adding upvotes and downvotes to posts or replies
    # TODO Add karma handling to modify record of associated user
    def addVote(self, gID, voteType):
        replyObj = self.traverseTo(gID)

        #voteType == 0 for upvotes, 1 for downvotes
        if voteType == 0:
            replyObj.upvotes += 1
        elif voteType == 1:
            replyObj.downvotes -= 1
        else:
            raise RuntimeError

    # Helper function to access a given global id (of form G123P12345R123456R789012)
    def traverseTo(self, gID, rAccess=None):
        if len(gID) == 0:
            return rAccess

        if gID[0] == "R":
            locate = rAccess.replies[gID[:7]]
            accessPoint = self.traverseTo(gID[7:], locate)
        elif gID[0] == "P":
            locate = rAccess.posts[gID[:6]]
            accessPoint = self.traverseTo(gID[6:], locate)
        elif gID[0] == "G":
            locate = self.communities[gID[:4]]
            accessPoint = self.traverseTo(gID[4:], locate)
        else:
            raise RuntimeError

        return accessPoint

    # Returns a random post feed based on the viewSize
    def returnFeed(self, viewSize):
        # Chooses a random subset of post key, value pairs from global posts
        selected = dict(random.sample(list(self.postStore.items()), viewSize))

        return selected
         
    # <----------------- Shutdown functions ----------------->
    # Saves website data to JSON file
    def exportWebsite(self):
        data = {}

        for cID, community in self.communities.items():
            posts = {}
            for pID, post in community.posts.items():
                posts[pID] = {
                    "author": post.author,
                    "title": post.title,
                    "content": post.content,
                    "votes": [post.upvotes, post.downvotes],
                    "replies": self._exportReplies(post.replies),
                }

            data[cID] = {
                "name": community.name,
                "desc": community.desc,
                "posts": posts,
                "members": sorted(community.members),
            }

        with open("./Storage/Export/data.json", "w") as file:
            json.dump(data, file, indent=4)

    def _exportReplies(self, replies):
        data = {}

        for rID, reply in replies.items():
            data[rID] = {
                "author": reply.author,
                "content": reply.content,
                "votes": [reply.upvotes, reply.downvotes],
                "replies": self._exportReplies(reply.replies),
            }

        return data
    
    # Saves user data to JSON file
    def exportUsers(self):
        data = {}

        for uID, user in self.users.items():
            data[uID] = {
                "name": user.name,
                "bio": user.bio,
                "karma": user.karma,
                "contributions": user.contributions,
                "posts": sorted(user.posts),
                "replies": sorted(user.replies),
                "personalBio": user.personalBio,
            }

        with open("./Storage/Export/users.json", "w") as file:
            json.dump(data, file, indent=4)