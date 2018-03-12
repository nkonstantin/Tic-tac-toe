'''
This is a simple Tic-Tac-Toe game based on Curses terminal library.
It features a colored TUI, keypad input, 2 alternating players, game state
check, game reset and quit options.
'''

import curses
from curses import wrapper


# Initializing curses
stdscr = curses.initscr()
curses.noecho()
stdscr.keypad(1)
# Using a color pair
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)


# Board reset function
def board_reset():
    global tac_toes
    tac_toes = []
    tac_toes.append([' ', ' ', ' '])
    tac_toes.append([' ', ' ', ' '])
    tac_toes.append([' ', ' ', ' '])


# Get coordinates function
def set_dims(stdscr):
    global win_center_y, win_center_x, win_center_top, win_center_bot
    global win_center_left, win_center_right
    # Getting terminal window dimensions in tuple format (y,x)
    dims = stdscr.getmaxyx()
    # Getting window center coordinates and setting top/bot l/r
    win_center_y = int(dims[0] / 2)
    win_center_x = int(dims[1] / 2)
    win_center_top = win_center_y - 2
    win_center_bot = win_center_y + 2
    win_center_left = win_center_x - 4
    win_center_right = win_center_x + 4


# Initialize player state
def player_init():
    global current_player, mark, quit, player1_win, player2_win, player_tie
    global game_over, reset
    current_player = '2'
    mark = ''
    quit = False
    player1_win = False
    player2_win = False
    player_tie = False
    game_over = False
    reset = False


# Alternate players
def player_alter():
    global current_player, mark
    if current_player == '2':
        current_player = '1'
        mark = 'X'
    else:
        current_player = '2'
        mark = 'O'


# Form game grid
def game_grid_form():
    global game_grid
    game_grid = []
    game_grid.append('-------------')
    game_grid.append('| {} | {} | {} |'.format(tac_toes[0][0],
                                               tac_toes[0][1],
                                               tac_toes[0][2]))
    game_grid.append('-------------')
    game_grid.append('| {} | {} | {} |'.format(tac_toes[1][0],
                                               tac_toes[1][1],
                                               tac_toes[1][2]))
    game_grid.append('-------------')
    game_grid.append('| {} | {} | {} |'.format(tac_toes[2][0],
                                               tac_toes[2][1],
                                               tac_toes[2][2]))
    game_grid.append('-------------')


# Form game text
def game_text_form():
    global game_title, player_text, bottom_text
    global player_tie, player1_win, player2_win, current_player
    directions1 = 'Use arrow keys to choose a square'
    directions2 = 'Press "x" to confirm your move'
    game_title = '\u2660 TIC-TAC-TOE\u2660'
    if game_over is False:
        player_text = 'Player {} turn'.format(current_player)
    else:
        if player_tie is True:
            player_text = 'THE GAME IS A TIE'
            directions1 = ' '
            directions2 = 'Press "r" to reset the game'
        if player1_win is True:
            player_text = 'PLAYER 1 WINS!'
            directions1 = ' '
            directions2 = 'Press "r" to reset the game'
        if player2_win is True:
            player_text = 'PLAYER 2 WINS!'
            directions1 = ' '
            directions2 = 'Press "r" to reset the game'

    bottom_text = [player_text, directions1, directions2, 'Press "q" to exit']


# Draw screen fuction
def draw_screen(stdscr):
    global cursor_pos_x, cursor_pos_y
    # Setting Y coordinate to use game grid center as a pivot
    y_pos = win_center_y - int(len(game_grid) / 2)
    # Clearing the screen
    stdscr.clear()
    # Drawing the title 3 rows above the grid
    stdscr.addstr(y_pos - 3,
                  win_center_x - int(len(game_title) / 2),
                  game_title, curses.color_pair(1))

    # Drawing the game grid in the window center
    for item in game_grid:
        stdscr.addstr(y_pos,
                      win_center_x - int(len(item) / 2),
                      item, curses.color_pair(1))
        y_pos += 1

    # Drawing bottom text 3 rows beneath the grid
    y_pos += 3
    for item in bottom_text:
        stdscr.addstr(y_pos,
                      win_center_x - int(len(item) / 2),
                      item, curses.color_pair(1))
        y_pos += 1

    # Resetting the cursor to the center of game grid
    cursor_pos_x = win_center_x
    cursor_pos_y = win_center_y
    stdscr.move(cursor_pos_y, cursor_pos_x)

    # Refreshing screen
    stdscr.refresh()


def player_input(stdscr):
    global tac_toes, cursor_pos_x, cursor_pos_y, quit, reset
    while True:
        q = stdscr.getch()
        # Moving the cursor coords around the grid
        if q == curses.KEY_UP and cursor_pos_y != win_center_y - 2:
            cursor_pos_y -= 2
        elif q == curses.KEY_DOWN and cursor_pos_y != win_center_y + 2:
            cursor_pos_y += 2
        elif q == curses.KEY_LEFT and cursor_pos_x != win_center_x - 4:
            cursor_pos_x -= 4
        elif q == curses.KEY_RIGHT and cursor_pos_x != win_center_x + 4:
            cursor_pos_x += 4
        # If 'x' is pressed and game is not over:
        elif (q == ord('x')) and (game_over is False):
            if cursor_pos_y == win_center_top and cursor_pos_x == win_center_left and tac_toes[0][0] == ' ':
                tac_toes[0][0] = mark
                break
            if cursor_pos_y == win_center_top and cursor_pos_x == win_center_x and tac_toes[0][1] == ' ':
                tac_toes[0][1] = mark
                break
            if cursor_pos_y == win_center_top and cursor_pos_x == win_center_right and tac_toes[0][2] == ' ':
                tac_toes[0][2] = mark
                break
            if cursor_pos_y == win_center_y and cursor_pos_x == win_center_left and tac_toes[1][0] == ' ':
                tac_toes[1][0] = mark
                break
            if cursor_pos_y == win_center_y and cursor_pos_x == win_center_x and tac_toes[1][1] == ' ':
                tac_toes[1][1] = mark
                break
            if cursor_pos_y == win_center_y and cursor_pos_x == win_center_right and tac_toes[1][2] == ' ':
                tac_toes[1][2] = mark
                break
            if cursor_pos_y == win_center_bot and cursor_pos_x == win_center_left and tac_toes[2][0] == ' ':
                tac_toes[2][0] = mark
                break
            if cursor_pos_y == win_center_bot and cursor_pos_x == win_center_x and tac_toes[2][1] == ' ':
                tac_toes[2][1] = mark
                break
            if cursor_pos_y == win_center_bot and cursor_pos_x == win_center_right and tac_toes[2][2] == ' ':
                tac_toes[2][2] = mark
                break
        # Quitting the game if 'q' is pressed
        elif q == ord('q'):
            quit = True
            break
        # Resetting the game after a gameover
        elif q == ord('r') and game_over is True:
            reset = True
            break
        # Drawing the cursor
        stdscr.move(cursor_pos_y, cursor_pos_x)
        stdscr.refresh()


# Checking for win condition
def check_win(tac_toes):
    tie = True
    global player_tie, game_over

    def check_winning_player(x):
        global player1_win, player2_win, game_over
        if x == 'X':
            player1_win = True
            game_over = True
        else:
            player2_win = True
            game_over = True
    # Horizontal check
    if tac_toes[0][0] == tac_toes[0][1] == tac_toes[0][2] != ' ':
        check_winning_player(tac_toes[0][0])
    elif tac_toes[1][0] == tac_toes[1][1] == tac_toes[1][2] != ' ':
        check_winning_player(tac_toes[1][0])
    elif tac_toes[2][0] == tac_toes[2][1] == tac_toes[2][2] != ' ':
        check_winning_player(tac_toes[2][0])
    # Vertical check
    elif tac_toes[0][0] == tac_toes[1][0] == tac_toes[2][0] != ' ':
        check_winning_player(tac_toes[0][0])
    elif tac_toes[0][1] == tac_toes[1][1] == tac_toes[2][1] != ' ':
        check_winning_player(tac_toes[0][1])
    elif tac_toes[0][2] == tac_toes[1][2] == tac_toes[2][2] != ' ':
        check_winning_player(tac_toes[0][2])
    # Diagonal check
    elif tac_toes[0][0] == tac_toes[1][1] == tac_toes[2][2] != ' ':
        check_winning_player(tac_toes[0][0])
    elif tac_toes[2][0] == tac_toes[1][1] == tac_toes[0][2] != ' ':
        check_winning_player(tac_toes[2][0])
    # Check for tie
    else:
        for x in tac_toes:
            for y in x:
                if y == ' ':
                    tie = False
        if tie is True:
            game_over = True
            player_tie = True


# Main function to be passed to wrapper for proper terminal reset.
def main(stdscr):
    # Initial variables
    set_dims(stdscr)
    board_reset()
    player_init()
    # Main game loop
    while True:
        # Quit condition
        if quit is True:
            break
        # Resetting the game
        if reset is True:
            board_reset()
            player_init()
        # Game code goes below
        check_win(tac_toes)
        player_alter()
        game_grid_form()
        game_text_form()
        draw_screen(stdscr)
        player_input(stdscr)
    # Exiting the app
    curses.endwin()


# Wrapped main function
wrapper(main)
