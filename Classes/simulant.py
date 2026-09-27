from Classes.schemas import Profile

class Simulant(Profile):
    def __init__(self, community, id, name, bio, karma, contributions, posts, replies, personalBio):
        self.community = community

        posts = set(posts)
        replies = set(replies)
        
        postContents = self.loadPosts(posts)
        replyContents = self.loadReplies(replies)
        
        super().__init__(id, name, bio, karma, contributions, postContents, replyContents)

        self.personalBio = personalBio

    def loadPosts(self, pIDs):
        posts = {}

        for gID in pIDs:
            groupID = gID[:4]
            postID = gID[4:]

            contents = self.community[groupID].posts[postID].content

            posts[gID] = contents

            ## Potentially may add more recording here later where upvotes, downvotes, and comments are stored and influence restrospective evaluation of posts and thereby impact future likelihood of posting similar content again

        return posts

    def loadReplies(self, rIDs):
        replies = {}

        for gID in rIDs:
            groupID = gID[:4]
            postID = gID[4:10]

            comments = self.community[groupID].posts[postID].comments

            # Gets the reply ID
            lID = gID[10:]

            # If multiple reply ID's in lID, iterate through tree 
            while (len(lID[7:]) != 0):
                comments = comments[lID[:7]].replies
                lID = lID[7:]

            reply = comments[lID].content

            replies[gID] = reply

        return replies


# GROUPID: G123
# POSTID: P12345
# REPLYID: R123456
# GID: G123P12345R123456R789012