# Battleships
This is a battleships clone written in python and pygame. It was designed so I could play around with different battleship AIs and so you interact with the board with a command line and view events through a log. Its designed primarily to allow programmers to mess about with the game battleships. 

![image](https://github.com/DavidBlairs/Battleships/assets/54111529/72af8000-e776-4cbf-a134-d24ea2e592c8)

## Commands and Log Messages

In the game, you can interact with the system by entering commands. These commands control various aspects of the game, and log messages are generated in response to these commands. Below, you'll find a list of available commands and the corresponding log messages.

### Commands

- **`ebattleship x, y`**: Explode a segment of a battleship located at the coordinates `(x, y)`. This command triggers the `ExplodeBattleshipSegment` function.

- **`check x, y`**: Check the placement of a battleship segment at the coordinates `(x, y)`. This command triggers the `CheckPlacement` function.

- **`set x y`**: Set the placement of a battleship at the coordinates `(x, y)`. This command triggers the `SetPlacement` function.

- **`aiexplosion x y`**: Trigger an AI explosion attempt at the coordinates `(x, y)`. This command calls the `Explosion` function.

- **`dbattleship`**: Delete a battleship. This command triggers the `DeleteBattleship` function.

- **`update`**: Update the battleships. This command calls the `UpdateBattleships` function.

- **`supdate`**: Segmented update of battleships. This command calls the `SegmentedUpdate` function.

- **`rplace x y`**: Perform a random placement of battleships starting at coordinates `(x, y)`. This command triggers the `RandomPlacement` function.

- **`pbattleship x y z`**: Place a battleship with various arguments: `(x, y)` is the starting coordinate, and `z` is the orientation (0 for horizontal, 1 for vertical). This command calls the `PlaceBattleship` function.

- **`reset`**: Reset the game board. This command triggers the `Reset` function.

- **`aiattempt x y`**: Make an AI attempt at the coordinates `(x, y)`. This command calls the `AIAttempt` function.

- **`aistate`**: Change the state of the AI. This command toggles the AI state.

### Log Messages

Log messages provide information about the actions taken in response to commands. Here are the log messages corresponding to each command:

- **`ebattleship`**: The Battleship Explode Function Has Been Called.

- **`check`**: The Check Placement Function Has Been Called.

- **`set`**: The Set Placement Function Has Been Called.

- **`aiexplosion`**: The AI Has Made An Attempt.

- **`dbattleship`**: The Destroy Battleship Function Has Been Called.

- **`update`**: The Update Function Has Been Called.

- **`supdate`**: The Segmented Update Function Has Been Called.

- **`rplace`**: The Random Placement Function Has Been Called.

- **`pbattleship`**: The Place Battleship Function Has Been Called.

- **`reset`**: The Board Has Been Reset.

- **`aiattempt`**: The AI Has Made An Attempt.

- **`aistate`**: Change The State Of The AI.

Please use these commands to interact with the game and refer to the log messages to understand the actions taken by the system in response to your commands.

