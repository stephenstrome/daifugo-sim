### Daifugo Simulator
I'm not quite sure how far I'll take this project yet. I'm also not sure if I'll split it into multiple repositories or not. Current goal is to just simulate the card game "Daifugo" using the house rules my friends play with on the command line. From there, I'd like to build analysis into it (whether through machine learning or otherwise) to find optimal plays and see if there's certain techniques that we haven't discovered yet.

If I feel really adventurous, I may eventually build out a GUI and networked play as well. Although for that I'll probably make use of a game engine instead of building everything in raw python. We'll see. For now one step at a time, and that means a simple command line simulator.

## Phases and tasks

I have this broken down into different phases and different tasks needed to be completed for each phase. This list will shift in time as I think of more things or choose to break things down into more specific tasks as the project develops, but I have a few things in mind.

- Phase 1: Manually play games
- [x] Deal and shuffle deck for different amounts of players
- [x] Handle console input from player for handling their turn
- [x] Correctly handle turn progression past finished and passed players
- [x] Process tricks ending
- [ ] Validate the next card played is valid
- [ ] Process special cards (7s, 8s, Jacks)
- [ ] Allow runs
- [ ] Handle shibari, geki shibari, and kakumei
- [ ] Process jokers correctly

- Phase 2: Automatically play games, train models
- [ ] Create test to play out a game with a pre-determined hands and plays to test out all functions
- [ ] Create framework for an AI to learn how to play the game and play games against itself
- [ ] Create analysis system to suggest what it looks for when making moves
- [ ] Allow an individual to play against AI

- Phase 3: Creating a more playable game
- [ ] Transfer logic to game engine and have a playable interface instead of running everything from command line
- [ ] Allow AI model to be used in game engine
- [ ] Create online multiplayer