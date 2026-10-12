from Classes.platform import Platform

class Tests:
    def __init__(self):
        self.env = Platform()
        self.loaded = False

    # Testing loading data 
    def loadData(self):
        postData = "./Storage/Testing/data.json"
        userData = "./Storage/Testing/users.json"

        self.env.populateWebsite(postData)
        self.env.populateUsers(userData)      

        self.loaded = True

    def addCommunity(self):
        if not self.loaded:
            self.loadData()

        testName = "Simulation community"
        testDesc = "Testing simulation description"

        gID = self.env.createCommunity(testName, testDesc)

        commObj = self.env.traverseTo(gID)

        assert commObj.name == testName, "Name did not populate correctly"
        assert commObj.desc == testDesc, "Content did not populate correctly"

    def addPost(self):
        if not self.loaded:
            self.loadData()

        cID = "G123"
        aID = "1234"
        testTitle = "Post about fascinating simulation"
        testContent = "There's a lot to simulate."

        gID = self.env.createPost(cID, aID, testTitle, testContent)

        postObj = self.env.traverseTo(gID)

        assert postObj.title == testTitle, "Title did not populate correctly"
        assert postObj.content == testContent, "Content did not populate correctly"

    def addReply(self):
        if not self.loaded:
            self.loadData()

        rID = "G123P12345"
        aID = "1234"
        testContent = "This is a test reply"

        gID = self.env.createReply(rID, aID, testContent)

        replyObj = self.env.traverseTo(gID)

        assert replyObj.content == testContent, "Content did not populate correctly"

    def upvote(self):
        if not self.loaded:
            self.loadData()

        gID = "G123P12345"
        voteObject = self.env.traverseTo(gID)

        prevUpvotes = voteObject.upvotes
        self.env.addVote(gID, 0)
        currUpvotes = voteObject.upvotes

        assert currUpvotes == (prevUpvotes + 1), "Upvotes not working correctly"

    def downvote(self):
        if not self.loaded:
            self.loadData()

        gID = "G123P12345"
        voteObject = self.env.traverseTo(gID)

        prevDownvotes = voteObject.downvotes
        self.env.addVote(gID, 1)
        currDownvotes = voteObject.downvotes

        assert currDownvotes == (prevDownvotes - 1), "Downvotes not working correctly"

    def fetchFeed(self):
        currFeed = self.env.returnFeed(3)

        assert len(currFeed) == 3, "Incorrect feed length"

    def shutdown(self):
        self.env.exportWebsite()
        self.env.exportUsers()

    def runSuite(self):
        if not self.loaded:
            self.loadData()

        self.addCommunity()
        self.addPost()
        self.addReply()
        self.upvote()
        self.downvote()
        self.fetchFeed()

        self.shutdown()

        print("Test suite completed with no errors")
        