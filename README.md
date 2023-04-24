# Connect 4 AI

## How to use

To use it, launch the given commands below one by one in the root directory :

    # To build the docker image
    docker build -t connect-4 .

    # To build and run the docker container
    docker run --name my-connect -p 8000:8000 -d connect-4

Once you have launched the given commands, you can now access the Connect 4 AI and ask for the best move given a board via the URL `localhost:8000/move?b=<board-content>`

Note that to access the API in the docker container, you have to expose the port 8000 (otherwise you will receive no response)

## Error management

### - Error 400

 - **Invalid board length :** The given board did not have the right number of checkers in a connect 4 game (size should be 42)
 - **Invalid character in board :** The given board contained an invalid character. Valid characters are 'm', 'h' or '0'
 - **Invalid game state :** The given board did not have a valid game state. A valid game state should follow this rule : N(human) = N(machine) + 1
 - **Invalid board configuration :** The given board did not have a valid board configuration (as in some checkers were misplaced and impossible)

### - Error 422

 - **Board Full :** The given board is full and no move can be made
 - **machine won :** The machine has aligned 4 checkers and has won
 - **human won :**: The human player has aligned 4 checkers and has won