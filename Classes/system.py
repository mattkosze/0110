import copy

from Classes.platform import Platform
from Classes.schemas import navAction, comAction, posAction, repAction, votAction, logItem

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
        self.timeSteps = int(turnLength/timeLength)
        # Number of items seen in a given timeBlock
        self.viewSize = viewSize

        # <-- LOG -->
        # Used to record the actions at every turn and time within the simulation.
        self.globalLog = {}

    # Main simulation function that invokes the simulation for a given number of turns
    def runSimulation(self, simLength):
        # Length in turns, where each turn represents an up to {turnLength} second block with up to {turnLength/timeLength} actions each.
        self.simLength = simLength

        self._initializeUserStates()

        # Run simulation for specific number of turns
        for turn in range(simLength):
            tLog = {}

            # Call each user at each turn
            for uID in self.platform.users:
                actions = self.handleTurn(turn, uID)
                tLog[uID] = actions

            self.globalLog[turn] = tLog


    # Handles a user's turn
    def handleTurn(self, turn, uID):
        actions = []

        for ts in range(self.timeSteps):
            # Handle each timestamp within a turn
            response = self.platform.users[uID].action(turn)

            # HANDLE RESPONSE PROCESSING
            action = self._process(turn, ts, response, uID)

            actions.append(action)
        
        return actions

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
        stateObj.feed = feed
        stateObj.feedOffset = 0
        stateObj.currState = self._getFeedPage(feed)

    def _captureNavigationState(self, stateObj):
        return {
            "sType": stateObj.sType,
            "currState": copy.deepcopy(stateObj.currState),
            "feed": copy.deepcopy(stateObj.feed),
            "feedOffset": stateObj.feedOffset,
        }

    def _saveNavigationState(self, stateObj):
        stateObj.navigationHistory.append(self._captureNavigationState(stateObj))

    def _restoreNavigationState(self, stateObj, savedState):
        stateObj.sType = savedState["sType"]
        stateObj.currState = savedState["currState"]
        stateObj.feed = savedState["feed"]
        stateObj.feedOffset = savedState["feedOffset"]

    def _getFeedPage(self, feed, offset=0):
        feedItems = list(feed.items())

        return dict(feedItems[offset:offset + self.viewSize])
    
    # Overarching function to handle action processing as decided by the simulant
    def _process(self, turn, ts, response, uID):
        action = response["aType"]
        if action == "community":
            self._handleCreateCommunity(response, uID)
        elif action == "post":
            self._handleCreatePost(response, uID)
        elif action == "reply":
            self._handleCreateReply(response, uID)
        elif action == "vote":
            self._handleCreateVote(response, uID)
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

        logItemObj = logItem(turn, ts, uID, action)

        return logItemObj

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
        stateObj = self.platform.users[uID].state

        if stateObj.sType != "f":
            raise RuntimeError

        try:
            selectedIndex = int(response["on"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError("Invalid click index") from exc

        pageItems = list(stateObj.currState.items())
        if selectedIndex < 0 or selectedIndex >= len(pageItems):
            raise RuntimeError("Click index is outside the current feed page")

        selectedID, selectedPost = pageItems[selectedIndex]
        self._saveNavigationState(stateObj)

        stateObj.prevState = copy.deepcopy(stateObj.currState)
        stateObj.sType = "p"
        stateObj.currState = {selectedID: selectedPost}
        stateObj.actionHistory.append(navAction("click"))

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
        # NOTE: Omitting community creation functionality for now, as there's no dedicated community viewing function. To be added in future release.
        pass

    def _handleCreatePost(self, response, uID):
        userObj = self.platform.users[uID]
        stateObj = userObj.state

        cID = response["cID"]
        pTitle = response["pTitle"]
        pContent = response["pContent"]
        gID = self.platform.createPost(cID, uID, pTitle, pContent)

        stateObj.actionHistory.append(posAction(gID, pTitle, pContent))


    def _handleCreateReply(self, response, uID):
        userObj = self.platform.users[uID]
        stateObj = userObj.state

        rID = response["rID"]
        rContent = response["rContent"]
        gID = self.platform.createReply(rID, uID, rContent)

        stateObj.actionHistory.append(repAction(gID, rContent))

    def _handleCreateVote(self, response, uID):
        userObj = self.platform.users[uID]
        stateObj = userObj.state

        vOn = response["vOn"]
        vType = int(response["vType"])
        self.platform.addVote(vOn, vType)

        stateObj.actionHistory.append(votAction(vOn, vType))

    # Function to record actions in the global log
    def _recordAction(self, uID):
        pass