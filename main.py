from Classes.platform import Platform
from Classes.schemas import Community, Post, Reply, Profile

# Dummy environment set up for testing
env = Platform(pData="Storage/Testing/data.json", pUsers="Storage/Testing/users.json")

print(env.users['U123456'].posts)