
class Community:
     def __init__(self, id, name, desc, posts, members):
         self.id = id
         self.name = name
         self.desc = desc
         self.posts = posts
         self.members = members

class Post:
    def __init__(self, id, author, title, content, votes, comments):
        self.id = id
        self.author = author
        self.title = title
        self.content = content

        # Votes is an l2 list where votes[0] is # upvotes and votes[1] is # downvotes
        self.upvotes = votes[0]
        self.downvotes = votes[1]
        
        self.comments = comments

class Comment:
    def __init__(self, id, author, content, votes, isReply, replies, parentID=-1):
        self.id = id
        self.author = author
        self.content = content

        # Votes is an l2 list where votes[0] is # upvotes and votes[1] is # downvotes
        self.upvotes = votes[0]
        self.downvotes = votes[1]

        # replies is an l2 list where replies[0] is true or false to indicate presence of comments, and replies[1] is a dict containing reply chains
        self.isReply = isReply
        # ParentID defaults to -1 when no parent exists
        self.parentID = parentID

        self.hasReplies = replies[0]
        self.replies = replies[1]
