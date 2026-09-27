import json

from Classes.platform import Platform
from Classes.schemas import Community, Post, Comment, Profile

replies = {"1": "G123P12345R123456R789012"}

env = Platform(pData="Storage/testingdata.json")

stuff = env.communities["G123"].posts["P12345"].comments["R123456"].replies["R789012"].content

print(f"direct result is {stuff}")

def testing(rIDs, env):
    replies = {}

    for entry in rIDs:
        gID = rIDs[entry]
        groupID = gID[:4]
        postID = gID[4:10]

        comments = env.communities[groupID].posts[postID].comments

        # Gets the reply ID
        lID = gID[10:]

        # If multiple reply ID's in lID, iterate through tree 
        while (len(lID[7:]) != 0):
            comments = comments[lID[:7]].replies
            lID = lID[7:]

        reply = comments[lID].content

        replies[gID] = reply

    return replies

print(testing(replies, env))