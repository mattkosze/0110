import copy

from Classes.platform import Platform
from Classes.schemas import navAction, comAction, posAction, repAction, votAction

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

    def runSimulation(self, simLength):
        # Length in turns, where each turn represents an up to {turnLength} second block with up to {turnLength/timeLength} actions each.
        self.simLength = simLength

        self._initializeUserStates()

        for i in range(simLength):
            # TODO
            pass

    # Overarching function to handle an agents turn 
    def handleTurn(self, uID):
        for timeStep in range(self.numTimeBlocks):
            # Handle each time within a turn
            pass

    # <----------------- Internal action processing functions ----------------->
    def _initializeUserStates(self):
        # Initializes every user to start from an arbitrary home feed
        for uID in self.platform.users:
            stateObj = self.platform.users[uID].state

            self._setFeedState(stateObj)
            stateObj.prevState = stateObj.currState.copy()

    def _setFeedState(self, stateObj):
        feed = self.platform.returnFeed()

        stateObj.sType = "f"
        stateObj.sLoc = "i"
        stateObj.feed = feed
        stateObj.feedOffset = 0
        stateObj.currState = self._getFeedPage(feed)

    def _captureNavigationState(self, stateObj):
        return {
            "sType": stateObj.sType,
            "sLoc": stateObj.sLoc,
            "currState": copy.deepcopy(stateObj.currState),
            "feed": copy.deepcopy(stateObj.feed),
            "feedOffset": stateObj.feedOffset,
        }

    def _saveNavigationState(self, stateObj):
        stateObj.navigationHistory.append(self._captureNavigationState(stateObj))

    def _restoreNavigationState(self, stateObj, savedState):
        stateObj.sType = savedState["sType"]
        stateObj.sLoc = savedState["sLoc"]
        stateObj.currState = savedState["currState"]
        stateObj.feed = savedState["feed"]
        stateObj.feedOffset = savedState["feedOffset"]

    def _getFeedPage(self, feed, offset=0):
        feedItems = list(feed.items())

        return dict(feedItems[offset:offset + self.viewSize])
    
    # Overarching function to handle action processing as decided by the simulant
    def _process(self, response, uID):
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
            type = response["nType"]
            if type == "ignore":
                self._handleNavIgnore(uID)
            elif type == "feed":
                self._handleNavFeed(uID)
            elif type == "scroll":
                self._handleNavScroll(uID)
            elif type == "click":
                self._handleNavClick(response, uID)
            elif type == "back":
                self._handleNavBack(uID)
        else:
            raise RuntimeError

    # Handles an ignore nav, where user remains on page. Prev / curr locations do not change
    def _handleNavIgnore(self, uID):
        userObj = self.platform.users[uID]
        actionObj = navAction("ignore")

        userObj.state.actionHistory += [actionObj]

    # Handles a feed nav, where user returns to feed
    def _handleNavFeed(self, uID):
        userObj = self.platform.users[uID]
        stateObj = userObj.state
        prevState = stateObj.currState.copy()
        actionObj = navAction("feed")

        self._saveNavigationState(stateObj)
        self._setFeedState(stateObj)

        stateObj.prevState = prevState
        stateObj.actionHistory += [actionObj]

    # Handles scrolling, currently limited to actions on the feed page
    def _handleNavScroll(self, uID):
        userObj = self.platform.users[uID]
        stateObj = userObj.state

        if stateObj.sType == "f":
            feedItems = list(stateObj.feed.items())
            nextOffset = stateObj.feedOffset + self.viewSize
            nextPage = dict(feedItems[nextOffset:nextOffset + self.viewSize])

            if not nextPage:
                return

            self._saveNavigationState(stateObj)
            stateObj.prevState = stateObj.currState.copy()
            stateObj.currState = nextPage
            stateObj.feedOffset = nextOffset
            stateObj.actionHistory.append(navAction("scroll"))

    def _handleNavClick(self, response, uID):
        pass

    def _handleNavBack(self, uID):
        userObj = self.platform.users[uID]
        stateObj = userObj.state

        if not stateObj.navigationHistory:
            return

        currentState = self._captureNavigationState(stateObj)
        previousState = stateObj.navigationHistory.pop()

        self._restoreNavigationState(stateObj, previousState)
        stateObj.prevState = currentState["currState"]
        stateObj.actionHistory.append(navAction("back"))

    # Adds an action to the completed log
    def _handleCreateCommunity(self, response, uID):
        cName = response["cName"]
        cDesc = response["cDesc"]

        self.platform.createCommunity(cName, cDesc)

    def _handleCreatePost(self, response, uID):
        cID = response["cID"]
        pTitle = response["pTitle"]
        pContent = response["pContent"]
        aID = None

        # NOTE: STORE GID IN ACTION ID

        self.platform.createPost(cID, aID, pTitle, pContent)

    def _handleCreateReply(self, response, uID):
        rID = response["rID"]
        rContent = response["rContent"]
        aID = None

        self.platform.createReply(rID, aID, rContent)

        # NOTE: STORE GID IN ACTION ID

    def _handleCreateVote(self, response, uID):
        vOn = response["vOn"]
        vType = int(response["vType"])

        self.platform.addVote(vOn, vType)

    # Function to record actions in the global log
    def _recordAction(self, uID):
        pass