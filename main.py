from Classes.platform import Platform
from Classes.schemas import Community, Post, Comment, Profile

replies = {"1": "G123P12345R123456R789012"}

# Dummy environment set up for testing
env = Platform(pData="Storage/Testing/data.json", pUsers="Storage/Testing/users.json")

test = env.communities["G123"].posts

print(test)

post = env.createPost("G123", "U123456", "New post", "new post content")

print(test)
print(test[post].replies)

post = env.createReply

