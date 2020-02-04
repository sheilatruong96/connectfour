#Sheila Truong 53588737

import connectfour
import connectfour_functions

def playConnectFour():
    GameState = connectfour.new_game() #changed to game state
    while connectfour.winner(GameState) == 0: #changed to game state
        GameState = connectfour_functions.playerMove(GameState) #both changed to gamestate
        connectfour_functions.displayBoard(GameState) #changed to game state
    if connectfour.winner(GameState) == 1:
        print("RED player wins!")
    elif connectfour.winner(GameState) == 2:
        print("YELLOW player wins!")
    
    
if __name__ == '__main__':
    playConnectFour()
