from Classes.schemas import Profile

class Simulant(Profile):
    def __init__(self, communities, id, name, bio, karma, contributions, posts, replies, personalBio):
        self.communities = communities

        posts = set(posts)
        replies = set(replies)
        
        postContents = self.loadContent(posts)
        replyContents = self.loadContent(replies)
        
        super().__init__(id, name, bio, karma, contributions, postContents, replyContents)

        self.personalBio = personalBio

    def loadContent(self, IDs):
        contents = {}

        for gID in IDs:
            entryContent = self.traverseTo(gID).content

            contents[gID] = entryContent

            ## Potentially may add more recording here later where upvotes, downvotes, and comments are stored and influence restrospective evaluation of posts and thereby impact future likelihood of posting similar content again

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


# GROUPID: G123
# POSTID: P12345
# REPLYID: R123456
# GID: G123P12345R123456R789012