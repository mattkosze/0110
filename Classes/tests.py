import copy

from Classes.platform import Platform
from Classes.system import System
from Classes.simulant import Simulant

class PlatformTests:
    def __init__(self):
        self.env = Platform()
        self.loaded = False

    # Testing loading data 
    def loadData(self):
        pData = "./Storage/Testing/data.json"
        pUsers = "./Storage/Testing/users.json"

        self.env.populateWebsite(pData)
        self.env.populateUsers(pUsers)      

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
        currFeed = self.env.returnFeed()

        assert len(currFeed) == len(self.env.postStore)
        assert len(set(currFeed)) == len(currFeed)

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

        print("Platform test suite completed with no errors")

class SystemTests:
    def __init__(self):
        pData = "./Storage/Testing/data.json"
        pUsers = "./Storage/Testing/users.json"
        turnLength = 30
        timeLength = 6
        viewSize = 3

        self.system = System(pData, pUsers, turnLength, timeLength, viewSize)

        self.users = self.system.platform.users
        self.testUserKey = list(self.users.keys())[0]
        self.testUser = self.users[self.testUserKey]

    def userInitialization(self):
        self.system._initializeUserStates()

        users = self.system.platform.users
        
        for uID in users:
            userObj = users[uID]
            stateObj = userObj.state

            assert stateObj.currState is not None and stateObj.prevState is not None

    def navIgnore(self):
        # Copy the initial user data
        initUser = copy.deepcopy(self.testUser)

        # Complete ignore action
        self.system._handleNavIgnore(self.testUserKey)

        userAccess = self.testUser.state
        # Test state updates
        assert (userAccess.currState.keys() == initUser.state.currState.keys()), "States not the same"
        assert (len(userAccess.actionHistory) == (len(initUser.state.actionHistory)+1)), "Length not updated with additional action"
        assert (userAccess.actionHistory[-1].nType == "ignore"), "Last action not an ignore"

    def navFeed(self):
        pass

    def navScroll(self):
        # Copy the initial user data
        initUser = copy.deepcopy(self.testUser)

        # Complete scroll action
        self.system._handleNavScroll(self.testUserKey)
        
        userAccess = self.testUser.state
        # Test state updates
        assert (initUser.state.currState.keys() != userAccess.currState.keys()), "Feed not updated to reflect scroll"
        assert (userAccess.actionHistory[-1].nType == "scroll"), "Last action not a scroll"

    def navBack(self):
        userAccess = self.testUser.state
        currentPage = copy.deepcopy(userAccess.currState)
        currentOffset = userAccess.feedOffset
        historyLength = len(userAccess.actionHistory)

        self.system._handleNavBack(self.testUserKey)

        assert userAccess.currState.keys() != currentPage.keys(), "Back did not restore the previous page"
        assert userAccess.feedOffset < currentOffset, "Back did not restore the previous feed offset"
        assert len(userAccess.actionHistory) == historyLength + 1, "Back action was not recorded"
        assert userAccess.actionHistory[-1].nType == "back", "Last action was not back"

        self.system._handleNavBack(self.testUserKey)
        assert userAccess.feedOffset == 0, "Back did not restore the initial feed page"

        historyLength = len(userAccess.actionHistory)
        self.system._handleNavBack(self.testUserKey)
        assert len(userAccess.actionHistory) == historyLength, "Empty back navigation was not a no-op"

    def runSuite(self):
        self.userInitialization()
        self.navIgnore()
        self.navFeed()
        self.navScroll()
        self.navBack()


        print("System test suite completed with no errors")

class SimulantTests:
    def __init__(self):
        pass