from collections import namedtuple
import connectfour_functions
import connectfour
import socket

ServerConnection = namedtuple(
    'ServerConnection',
    ['socket', 'socket_in', 'socket_out'])

PlayerCommand = namedtuple(
    'PlayerCommand',
    ['command', 'column'])


def connect(address: 'ServerAddress', port: 'ServerPort') -> ServerConnection:
    ''' Connects the client to server with desired address and port
    '''
    try:
        connectfour_socket = socket.socket()
        connectfour_socket.connect((address, port))

        connectfour_socket_in = connectfour_socket.makefile('r')
        connectfour_socket_out = connectfour_socket.makefile('w')

        return ServerConnection(
            socket = connectfour_socket,
            socket_in = connectfour_socket_in,
            socket_out = connectfour_socket_out)
    except:
        raise ConnectionFailed()

def address() -> 'ServerAddress':
    ''' Asks the client for a server address and returns it
    '''
    while True:
        ServerAddress = input('Server Address: ').strip()
        if ServerAddress == '':
            print('Invalid: Empty Server Address')
        else:
            return ServerAddress


def port() -> 'ServerPort':
    ''' Asks the client for a server port and returns it
    '''
    while True:
        try:
            ServerPort = int(input('Port: ').strip())
            
            if ServerPort < 0 or ServerPort > 65535:
                print('The port number must be in the range (0 - 65535)')
            else:
                return ServerPort
        except ValueError:
            print('The port number must be in the range (0 - 65535)')
            

def username() -> 'Username':
    while True:
        try:
            Username = input('Username: ').strip()
            if len(Username.split(' ')) > 1:
                raise ServerError()
            else:
                return Username
        
        except:
            print('Your username cannot have spaces.\n')
            #raise ServerError()


def hello(connection: ServerConnection, username: 'Username') -> None:
    ''' The opening sequence after connecting to the server
    '''
    _write_line(connection, 'I32CFSP_HELLO {}'.format(username))
    _expect_line(connection, 'WELCOME {}'.format(username))


def request(connection: ServerConnection, gametype: str) -> None:
    ''' The client requests a game with an artificial intelligence
    '''
    _write_line(connection, gametype)
    _expect_line(connection, 'READY')


def send(connection: ServerConnection, action: PlayerCommand) -> None:
    ''' The client sends the action he/she intends to take
    '''
    action = ' '.join(action)
    _write_line(connection, action)

def close(connection: ServerConnection) -> None:
    ''' Closes the open connections with the server
    '''
    connection.socket_in.close()
    connection.socket_out.close()
    connection.socket.close()


def move():
    ''' Asks the user for a command and checks if the move is valid
    '''
    while True:
        try:
            print("Drop: Place a disc in the designated column (EX: DROP 1)")
            print("Pop: Remove one of your discs at the bottom of a column (EX: POP 1)")
            print()
            action = input('What would you like to do?\n')
            action = action.upper().split()

            if len(action) != 2:
                raise connectfour.InvalidMoveError()
            
            elif not action[0].startswith('DROP') and not action[0].startswith('POP'):
                raise connectfour.InvalidMoveError()

            elif int(action[1]) > 7 or int(action[1]) < 1:
                raise connectfour.InvalidMoveError()

            return PlayerCommand(
                command = action[0],
                column = (action[1]))
        except:
            print()
            print('Invalid Move. Please try again.\n')


def updateState(state: 'gameBoard', action: PlayerCommand):
    ''' Updates the current Game State.
    '''
    if action.command.upper() == 'DROP':
        state = connectfour.drop(state, int(action.column) - 1)
        
    elif action.command.upper() == 'POP':
        state = connectfour.pop(state, int(action.column) - 1)

    return state


def networkGame(connection: ServerConnection, state: 'gameBoard') -> None:
    ''' Plays the network version of ConnectFour
    '''
    connectfour_functions.displayBoard(state)
    
    while True:
        action = move()
        
        try:
            state = updateState(state, action)
        except:
            print('Invalid Move. Please try again.\n')
            continue
        
        send(connection, action)

        ServerLine = _read_line(connection)

        if ServerLine == 'OKAY':
            ServerMove = _read_line(connection).split()
            ServerMove = PlayerCommand(
                command = ServerMove[0],
                column = ServerMove[1])
            state = updateState(state, ServerMove)
            connectfour_functions.displayBoard(state)
            print('Server\'s Move: ' + ServerMove.command + ' ' + ServerMove.column + '\n')

            ServerLine2 = _read_line(connection)
            
            if ServerLine2 == 'READY':
                continue

            elif ServerLine == 'WINNER_RED':
                print('RED PLAYER WINS!')
                break                
            
            elif ServerLine2 == 'WINNER_YELLOW':
                print('YELLOW PLAYER WINS!')
                break
        
        elif ServerLine == 'WINNER_RED':
            print()
            print('RED PLAYER WINS!')
            break
        
        elif ServerLine2 == 'WINNER_YELLOW':
            print()
            print('YELLOW PLAYER WINS!')
            break
            
# Private Functions -----------------------------------------------

def _write_line(connection: ServerConnection, line: str) -> None:
    connection.socket_out.write(line + '\r\n')
    connection.socket_out.flush()

def _read_line(connection: ServerConnection) -> str:
    return connection.socket_in.readline()[:-1]

def _expect_line(connection: ServerConnection, expected: str) -> None:
    if _read_line(connection) != expected:
        raise ServerError()


# Exceptions ----------------------------------------------------

class ServerError(Exception):
    pass

class ConnectionFailed(Exception):
    pass

class InvalidMove(Exception):
    pass
