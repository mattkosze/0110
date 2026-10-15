from Classes.platform import Platform

class System:
    def __init__(self, pData, pUsers, turnLength, timeLength, viewSize):
        # <-- INTERNAL -->
        # Initialize the platform object for the simulation
        self.platform = Platform(pData, pUsers)
       
        # <-- INPUTS -->
        # Length of a turn, e.g. 30 seconds
        self.turnLength = turnLength
        # Length of a timeblock, e.g. 6 seconds
        self.timeLength = timeLength
        # Number of timeSteps within a turn, e.g. 30/6 = 5 timeSteps, where a timeStep is the one action unit
        self.timeSteps = turnLength/timeLength
        # Number of items seen in a given timeBlock
        self.viewSize = viewSize

    def initializeUserStates(self):
        # Initializes every user to start from an arbitrary home feed
        for uID in self.platform.users:
            userFeed = self.platform.returnFeed(self.viewSize)
            stateObj = self.platform.users[uID].state

            stateObj.sType = "f"
            stateObj.sLoc = "i"
            stateObj.currState = userFeed
            stateObj.prevState = userFeed

    def runSimulation(self, simLength):
        # Length in turns, where each turn represents an up to {turnLength} second block with up to {turnLength/timeLength} actions each.
        self.simLength = simLength

        for i in range(simLength):
            # TODO
            pass

    # Overarching function to handle an agents turn at a given
    def handleTurn(self, agent):
        for timeStep in range(self.numTimeBlocks):
            # Handle each time within a turn
            pass

    # <----------------- Internal action processing functions ----------------->
    # Overarching function to handle action processing as decided by the simulant
    def _process(self, response):
        action = response["aType"]
        if action == "community":
            self._handleCreateCommunity(response)
        if action == "post":
            self._handleCreatePost(response)
        elif action == "reply":
            self._handleCreateReply(response)
        elif action == "vote":
            self._handleCreateVote(response)
        elif action == "navigate":
            type = response["navType"]
            if type == "back":
                self._handleNavBack(response)
            elif type == "click":
                self._handleNavClick(response)
            elif type == "feed":
                self._handleNavFeed(response)
            elif type == "scroll":
                self._handleNavScroll(response)
            elif type == "ignore":
                self._handleNavIgnore(response) 
        else:
            raise RuntimeError

    # Adds an action to the completed log
    def _handleCreateCommunity(self, response):
        cName = response["cName"]
        cDesc = response["cDesc"]

        self.platform.createCommunity(cName, cDesc)

    def _handleCreatePost(self, response):
        cID = response["cID"]
        pTitle = response["pTitle"]
        pContent = response["pContent"]
        aID = None

        self.platform.createPost(cID, aID, pTitle, pContent)

    def _handleCreateReply(self, response):
        rID = response["rID"]
        rContent = response["content"]
        aID = None

        self.platform.createReply(rID, aID, rContent)

    def _handleCreateVote(self, response):
        vOn = response["vOn"]
        vType = int(response["vType"])

        self.platform.addVote(vOn, vType)

    def _handleNavBack(self, response):
        # Need to return to previous state, therefore need to store current & prev state.
        # Will not support consecutive back actions.
        pass

    def _handleNavClick(self, response):
        # Need to have next element
        pass

    def _handleNavFeed(self, response):
        pass

    def _handleNavScroll(self, response):
        pass

    def _handleNavIgnore(self, response):
        pass

    # Function to record actions in the simulant and global log
    def _recordAction(self):
        pass