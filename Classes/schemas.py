
class Community:
     def __init__(self, id, name, desc, posts, members):
         self.id = id
         self.name = name
         self.desc = desc
         self.posts = posts
         self.members = members

class Post:
    def __init__(self, id, author, title, content, upvotes, downvotes, comments):
        self.id = id
        self.author = author
        self.title = title
        self.content = content
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.comments = comments

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