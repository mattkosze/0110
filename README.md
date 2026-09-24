# Simulating behaviour on social media
This is a simulation project regarding modelling behaviour on social media platforms. t's meant to simulate individual user behaviour at a given point in time, and where simulants can join communities, and \{upvote, downvote, comment on, create new, ignore\} posts, or totally switch reddit communities at a given point in time.

## Architecture 
The system is broken down into three components: the platform architecture, the simulant architecture, and the testing overhead. This is then combined into the main running files which leverages all the components to run simulations.

### Platform Architecture
The platform is represented as a class data structure. This means that it lacks a traditional GUI and instead uses a class to represent both current state as well as potential actions going forward.

### Simulant Architecture
Simulants are designed as a generalizable class that can be instantiated as a specific person a given reddit profile. This reddit profile, followers, karma, contributions, reddit age, and number of subreddits active this. This is then populated with all their comments, upvotes, and so on. 

### Testing Overhead
The testing architure allows for specification regarding the list of reddit communites and posts upon which to act.