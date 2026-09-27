from schemas import Profile

class Simulant(Profile):
    def __init__(self, env, id, name, bio, karma, contributions, posts, replies, personalBio):
        self.env = env
        
        postContents = self.loadPosts(posts)
        replyContents = self.loadReplies(replies)
        
        super.__init__(id, name, bio, karma, contributions, postContents, replyContents)

        self.personalBio = personalBio

    def loadPosts(self, pIDs):
        posts = {}

        for entry in pIDs:
            gID = pIDs[entry]
            groupID = gID[:4]
            postID = gID[4:]

            contents = self.env.communities[groupID].posts[postID].content

            posts[gID] = contents

            ## Potentially may add more recording here later where upvotes, downvotes, and comments are stored and influence restrospective evaluation of posts and thereby impact future likelihood of posting similar content again

        return posts

    def loadReplies(self, rIDs):
        replies = {}

        for entry in rIDs:
            gID = rIDs[entry]
            groupID = gID[:4]
            postID = gID[4:10]

            comments = self.env.communities[groupID].posts[postID].comments

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