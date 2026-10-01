
class Community:
     def __init__(self, id, name, desc, posts={}, members={}):
         self.id = id # str
         self.name = name # str
         self.desc = desc # str
         self.posts = posts # dict
         self.members = members # set

class Post:
    def __init__(self, id, author, title, content, upvotes=0, downvotes=0, replies={}):
        self.id = id
        self.author = author
        self.title = title
        self.content = content
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.replies = replies

class Comment:
    def __init__(self, id, author, content, upvotes, downvotes, hasReplies=False, replies={}, isReply=False, parentID=-1):
        self.id = id
        self.author = author
        self.content = content
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.isReply = isReply
        # ParentID defaults to -1 when no parent exists
        self.parentID = parentID
        self.hasReplies = hasReplies
        self.replies = replies

class Profile:
    def __init__(self, id, name, bio, karma, contributions, posts, replies):
        self.id = id
        self.name = name
        self.bio = bio
        self.karma = karma
        self.contributions = contributions
        self.posts = posts
        self.replies = replies