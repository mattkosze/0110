# Simulating behaviour on social media
This is a simulation project regarding modelling behaviour on social media platforms. It's meant to simulate individual user behaviour and collective interaction over a period of time.

## Architecture 
The simulation is broken down into three components: the platform architecture, the system architecture, and the simulant architecture. The system broadly is the primary point of interaction, centrally controlling the test and mediating interaction between the platform and simulant.  

### Platform Architecture
The platform is represented as a class data structure. This means that it lacks a traditional GUI and instead uses a class to represent both current state as well as potential actions going forward.

### System Architecture
The system is responsible for orchestrating the simulation. It takes as input initial platform and user data and instantiates a platform object which is then used for the simulation. Simulation length is passed through in terms of turns, which each turn is turnLength long, and is split into n timeLength segments where n = turnlength/timeLength. Therefore, a single turn is composed of n times, where at each time i the simulant can take actions corresponding to its current state.

### Simulant Architecture
Simulants are designed as a generalizable class that can be instantiated as a specific person a given reddit profile. This reddit profile, followers, karma, contributions, reddit age, and number of subreddits active this. This is then populated with all their comments, upvotes, and so on. A given time i in turn t, the simulant is presented with a current state, representing the page they are on, and then makes an LLM call where (page dependent) they can either navigate {one page back, click on something, back to the feed, ignore and stay at state, scroll} or create a {community, post, reply, upvote, downvote}. 

## Data Storage
Platform and user data is stored in corresponding JSON files, where for platform data the structure goes `community --> post --> repl(ies)` and is stored in objects so it can be accessed in a tree-like fashion. 

To access data, you follow a tree using `GROUPID`'s, `POSTID`'s, and `REPLYID`'s. This is where `GROUPID`'s are of format "G123,"  `POSTID`'s follow "P12345," and `REPLYID`'s follow "R123456."

For example, a top-level reply would have it's global ID be "G123P12345R123456", which can then be broken down to access the reply itself. Lower-level replies would have total ID "...R123456R789012" which is again traversed down the tree until the record is accessed.

Users are stored by their unique `USERID` following "U123456."

See the example folder at `Storage --> Example --> Data Storage` for examples of the data and user schemas.

## LLM Response Schemas
The queried LLM will return JSON with the core differentiator begin the action type, denoted `aType`, with different fields per the action type. 

See the example folder at `Storage --> Example --> LLM Responses` for the exact returned schemas.