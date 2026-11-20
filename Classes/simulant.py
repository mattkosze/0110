from Classes.schemas import Profile, State

class Simulant(Profile):
    def __init__(self, communities, id, name, bio, karma, contributions, posts, replies, personalBio):
        self.communities = communities
        
        postContents = self.loadContent(set(posts))
        replyContents = self.loadContent(set(replies))
        
        super().__init__(id, name, bio, karma, contributions, postContents, replyContents)

        self.personalBio = personalBio

        self.state = State()

    def action(self, callNum):
        callNum %= 8

        if callNum == 0:
         response = {
                    "aType": "navigate",
                    "nType": "ignore"
                }
        elif callNum == 1:
            response = {
                "aType": "navigate",
                "nType": "back"
            }
        elif callNum == 2:
            response = {
                "aType": "post",
                "cID": "G123",
                "pTitle": "Simulated post",
                "pContent": "post content"
            }
        elif callNum == 3:
            response = {
                "aType": "navigate",
                "nType": "click",
                "on": "0"
            }
        elif callNum == 4:
            response = {
                "aType": "navigate",
                "nType": "feed"
            }
        elif callNum == 5:
            response = {
                "aType": "navigate",
                "nType": "scroll"
            }
        elif callNum == 6:
            response = {
                "aType": "vote",
                "vOn": "G123P12345R123456",
                "vType": "0"
            }
        elif callNum == 7:
            response = {
                "aType": "reply",
                "rID": "G123P12345R123456",
                "rContent": "text content"
            }

        return response


    def loadContent(self, IDs):
        contents = {}

        for gID in IDs:
            entryContent = self.traverseTo(gID).content
            contents[gID] = entryContent

        return contents

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