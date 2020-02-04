import connectfour_server_protocol
import connectfour_functions
import connectfour

def run_network_connectfour():
    ''' Initiates the ConnectFour program that connects to a server
    '''
    Connection = _valid_connection()

    if Connection != None:

        Username = connectfour_server_protocol.username()

        connectfour_server_protocol.hello(Connection, Username)

        connectfour_server_protocol.request(Connection, 'AI_GAME')

        print()
        print('Welcome to ConnectFour!')
        print()
        print('Let\'s begin!')

        gameBoard = connectfour.new_game()
        
        connectfour_server_protocol.networkGame(Connection, gameBoard)
        
        connectfour_server_protocol.close(Connection)
        
    else:
        print('Closing program.')

# Private Functions ---------------------------

def _valid_connection() -> 'Connection':

    ServerAddress = connectfour_server_protocol.address()
    ServerPort = connectfour_server_protocol.port()

    try:
        Connection = connectfour_server_protocol.connect(ServerAddress, ServerPort)
    
    except:
        print('Connection Failed! Invalid address and/or port.\r\n')
        Connection = None
            
    return Connection


if __name__ == '__main__':
    run_network_connectfour()

