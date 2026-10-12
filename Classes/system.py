from Classes.platform import Platform

class System:
    def __init__(self, pData, pUsers, simLength, turnLength, timeLength, viewSize):
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
            pass
        if action == "post":
            pass
        elif action == "reply":
            pass
        elif action == "vote":
            pass
        elif action == "navigate":
            type = response["navType"]
            if type == "back":
                pass
            elif type == "click":
                pass
            elif type == "feed":
                pass
            elif type == "scroll":
                pass
            elif type == "ignore":
                pass 
        else:
            pass

    # Adds an action to the completed log
    def _handleCreateCommunity(self, responseData):
        cName = responseData["cName"]
        cDesc = responseData["cDesc"]

        self.platform.createCommunity(cName, cDesc)

    def _handleCreatePost(self):
        pass

    def _handleCreateReply(self):
        pass

    def _handleCreateVote(self):
        pass

    def _handleNavigation(self):
        pass

    # Function to record actions in the simulant and global log
    def _recordAction(self):
        pass

