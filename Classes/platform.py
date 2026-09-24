class platform():
    def __init__(self, pCommunities=None, pPosts=None, pUsers=None):
        # Communities will be stored in a k:v format where a unique ID (key) corresponds to a community class object (value)
        self.communities = {}
        # Platform users will be stored as a k:v format where a ID (key) corresponds to 
        self.users = {}


        # NOTE: May opt to make all three needed, as there's likely no situation in which they aren't used
        if pCommunities:
            pass
        if pPosts:
            pass
        if pUsers:
            pass

    # <----------------- Object population functions ----------------->

    # Loads in community data from a data store json file
    def populateCommunities(self, cData):
        pass

    def populatePosts(self, pData):
        pass

    # Loads in user data from a data store json file
    def populateUsers(self, uData):
        pass

    # <----------------- Interaction functions ----------------->

    # Handles community creation
    def createCommunity(self, cName, cDesc):
        pass

    # Handles post creation within a community
    def createPost(self):
        pass

    # <----------------- Shutdown functions   ----------------->

    def exportPosts(self):
        pass

    def exportCommunities(self):
        pass

    def exportUsers(self):
        pass
    
    # Orchastrate platform saving and shutdown 
    def shutdown(self):
        pass