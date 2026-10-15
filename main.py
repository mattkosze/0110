from Classes.tests import PlatformTests, SystemTests, SimulantTests

# Dummy environment set up for testing

platformTests = PlatformTests()

platformTests.runSuite()

systemTests = SystemTests()

systemTests.runSuite()