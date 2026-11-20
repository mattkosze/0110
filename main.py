from Classes.tests import PlatformTests, SystemTests, SimulantTests
from Classes.system import System

# Dummy environment set up for testing

platformTests = PlatformTests()

platformTests.runSuite()

systemTests = SystemTests()

systemTests.runSuite()

# Simulation testing

pData = "./Storage/Testing/data.json"
pUsers = "./Storage/Testing/users.json"

simulation = System(pData, pUsers, 5, 5, 4)

simulation.runSimulation(8)

for i in simulation.globalLog:
    print(f"Turn {i}:")
    for uID in simulation.globalLog[i]:
        print(f"  User {uID}:")
        for action in simulation.globalLog[i][uID]:
            print(f"    {action.action}")
