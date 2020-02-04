#Sheila Truong 53588737

import connectfour

# ------------------------------------------------------------------------------------------    
# Main Functions ---------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

def playGame(gameBoard) -> None:
    ''' Plays the game until a winner is possible
    '''

    _display_opening_dialogue()
    
    displayBoard(gameBoard)
    
    while connectfour.winner(gameBoard) == 0:
        gameBoard = playerMove(gameBoard)
        displayBoard(gameBoard)
        
    _display_winner(gameBoard)


def playerMove(gameBoard) -> 'Action, Column':
    ''' Updates the gameboard by the desired user move
    '''
    _display_move_dialogue(gameBoard)
    
    playerCommand = input()
    
    try:
        if playerCommand.upper().startswith('DROP'):
            gameBoard = connectfour.drop(gameBoard, int(playerCommand.split()[-1]) - 1)
        elif playerCommand.upper().startswith('POP'):
            gameBoard = connectfour.pop(gameBoard, int(playerCommand.split()[-1]) - 1)
        else:
            print("Sorry, try again.")           
    except:
        print("Incorrect value, try again.")

    return gameBoard


def displayBoard(GameState) -> None:
    ''' Displays the current gameboard in a user-friendly way
    '''
    print()
    _display_column_header(GameState)
    _display_player_symbol(GameState)
    print()



# ------------------------------------------------------------------------------------------    
# Private Functions ------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
        
def _display_column_header(GameState) -> None:
    ''' Prints the number of each column
    '''
    row = []
    
    for n in range(len(GameState.board)):
        row.append(str(n+1))
    row = ' '.join(row)
    
    print(row)


def _display_player_symbol(GameState) -> None:
    ''' Replaces all non-zero values with appropriate player symbols
    '''
    for n in range(len(GameState.board) - 1):
        row = []

        for column in GameState.board:
            if column[n] == 0:
                row.append('.')
            elif column[n] == 1:
                row.append('R')
            elif column[n] == 2:
                row.append('Y')
        row = ' '.join(row)

        print(row)


def _display_winner(gameBoard) -> None:
    ''' Displays the winner, if any
    '''
    if connectfour.winner(gameBoard) == 1:
        print("RED player wins!")
    elif connectfour.winner(gameBoard) == 2:
        print("YELLOW player wins!")
    else:
        pass

def _display_opening_dialogue() -> None:

    print('Welcome to ConnectFour!\n')
    print('Let\'s begin!\n')
    print('Player 1: RED')
    print('Player 2: YELLOW')



def _display_move_dialogue(gameBoard) -> None:
    print('What would you like to do, Player {}?\n'.format(gameBoard.turn))
    print("Drop: Place a disc in the designated column (EX: DROP 1)")
    print("Pop: Remove one of your discs at the bottom of a column (EX: POP 1)")
    print()
