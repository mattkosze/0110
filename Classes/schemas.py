
class Community:
     def __init__(self, id, name, desc, posts={}, members={}):
         self.id = id # str
         self.name = name # str
         self.desc = desc # str
         self.posts = posts # dict
         self.members = members # set

class Post:
    def __init__(self, id, gID, author, title, content, upvotes=0, downvotes=0, replies={}):
        self.id = id
        self.gID = gID
        self.author = author
        self.title = title
        self.content = content
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.replies = replies

class Reply:
    def __init__(self, id, gID, author, content, upvotes=0, downvotes=0, replies={}):
        self.id = id
        self.gID = gID
        self.author = author
        self.content = content
        self.upvotes = upvotes
        self.downvotes = downvotes
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

class State:
    def __init__(self):
        self.sType = None
        self.sLoc = None
        self.currState = None
        self.prevState = None
        self.feed = None
        self.feedOffset = 0
        self.actionHistory = []
        self.navigationHistory = []

class Action:
    def __init__(self, aType):
        self.aType = aType

class navAction(Action):
    def __init__(self, nType):
        super().__init__("navigate")
        self.nType = nType

class comAction(Action):
    def __init__(self, cName, cDesc):
        super().__init__("community")
        self.cName = cName
        self.cDesc = cDesc

class posAction(Action):
    def __init__(self, gID, pTitle, pContent):
        super().__init__("post")
        self.gID = gID
        self.pTitle = pTitle
        self.pContent = pContent

class repAction(Action):
    def __init__(self, gID, rContent):
        super().__init__("reply")
        self.gID = gID
        self.rContent = rContent

class votAction(Action):
    def __init__(self, vOn, vType):
        super().__init__("vote")
        self.vOn = vOn
        self.vType = vType