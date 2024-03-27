# Sasha and Manar
# CSCE 160
# HW 3 Connect4

import random, sys

# Function Definitions -----------------------------------------------------

# generate_board creates a 6x7 matrix that represents a Connect4 board
def generate_board():
    board = [None] * 6
    for i in range(6):
        board[i] = [' '] * 7
    return board

# display_board takes in a 6x7 matrix and prints out a graphic using unicode characters
def display_board(b):
    top_line = "\u250c\u2500\u252c\u2500\u252c\u2500\u252c\u2500\u252c\u2500\u252c\u2500\u252c\u2500\u2510"
    mid_line = "\u251c\u2500\u253c\u2500\u253c\u2500\u253c\u2500\u253c\u2500\u253c\u2500\u253c\u2500\u2524"
    bot_line = "\u2514\u2500\u2534\u2500\u2534\u2500\u2534\u2500\u2534\u2500\u2534\u2500\u2534\u2500\u2518"
    print("\n 0 1 2 3 4 5 6")
    print(top_line)
    for i in range(6):
        for j in range(7):
            print("\u2502", b[i][j], sep="", end="")
        if (j == 6):
            print("\u2502")
        if (i < 5):
            print(mid_line)
        else:
            print(bot_line)

# valid_column takes in a 6x7 matrix b and a column number c.
# It returns True if c is a column with free spots
# It returns False otherwise.
def valid_column(b, c):
    # b: 6x7 matrix
    # c: column number
    if (c < 0 or c > 6):
        print("Invalid column input. Try again.")
        return False
    for i in range(5,-1,-1):
        if(b[i][c] == " "):
            return True
    return False

# take_turn takes in a 6x7 matrix b, a column number c, and a checker.
def take_turn(b, c, checker):
    # b: 6x7 matrix
    # c: column number
    # checker: the computer's diamond checker or the player's heart checker
    for i in range(5, -1, -1):
        if (b[i][c] == " "):
            b[i][c] = checker
            break

# random_column takes in a 6x7 matrix b and returns a random valid column number.
# A valid column number is one within 0 and 6 and with free spots.
def random_column(b):
    c = random.randint(0, 6)
    while (not valid_column(b, c)):
        c = random.randint(0, 6)
    return c

# horizontal_check looks for horizontal wins.
# If the diamond checkers win, then return "Computer".
# If the heart checkers win, then return "Player".
# If no horizontal wins are found, then return False.
def horizontal_check(b, r, c, diamond, heart):
    # b: 6x7 matrix
    # r: row number
    # c: column number
    # diamond: the computer's checker
    # heart: the player's checker
    win = False
    for i in range(r, r+4):
        if (b[i][c] == b[i][c+1] == b[i][c+2] == b[i][c+3] and b[i][c] != " "):
           if (b[i][c] == diamond):
               win = "Computer"
           elif (b[i][c] == heart):
               win = "Player"
    return win

# vertical_check looks for vertical wins.
# If the diamond checkers win, then return "Computer".
# If the heart checkers win, then return "Player".
# If no vertical wins are found, then return False.
def vertical_check(b, r, c, diamond, heart):
    # b: 6x7 matrix
    # r: row number
    # c: column number
    # diamond: the computer's checker
    # heart: the player's checker
    win = False
    for i in range(c, c+4):
        if (b[r][i] == b[r+1][i] == b[r+2][i] == b[r+3][i] and b[r][i] != " "):
           if (b[r][i] == diamond):
               win = "Computer"
           elif (b[r][i] == heart):
               win = "Player"
    return win

# diagonal_check looks for diagonal wins.
# If the diamond checkers win, then return "Computer".
# If the heart checkers win, then return "Player".
# If no diagonal wins are found, then return False.
def diagonal_check(b, r, c, diamond, heart):
    # b: 6x7 matrix
    # r: row number
    # c: column number
    # diamond: the computer's checker
    # heart: the player's checker
    win = False
    # from top-left-corner to bottom-right-corner
    if (b[r][c] == b[r+1][c+1] == b[r+2][c+2] == b[r+3][c+3] and b[r][c] != " "):
        if (b[r][c] == diamond):
            win = "Computer"
        elif (b[r][c] == heart):
            win = "Player"
    # from bottom-left-corner to top-right corner
    elif (b[r+3][c] == b[r+2][c+1] == b[r+1][c+2] == b[r][c+3] and b[r+3][c] != " "):
        if (b[r+3][c] == diamond):
            win = "Computer"
        elif (b[r+3][c] == heart):
            win = "Player"
    return win

# triple_check looks at a 4x4 section of a matrix and checks for wins in that section.
# If the computer has a horizontal, vertical, or diagonal win, return "Computer". 
# If the player has a horizontal, vertical, or diagonal win, return "Player".
# If there is no winner, return False.
def triple_check(board, row, col, comp, play):
    game_win = False
    # Run horizontal, vertical, and diagonal checks
    horiz = horizontal_check(board, row, col, comp, play)
    vert = vertical_check(board, row, col, comp, play)
    diag = diagonal_check(board, row, col, comp, play)
    # Determine if there is a winner.
    if (horiz == "Computer" or vert == "Computer" or diag == "Computer"):
        game_win = "Computer"
    elif (horiz == "Player" or vert == "Player" or diag == "Player"):
        game_win = "Player"
    return game_win

# strategic_column looks at individual checker on the board
# and looks for empty spots that surround the checker.
# It returns the column number of the first empty spot it finds.
def strategic_column(b):
    # b: 6x7 matrix
    
    # scan column 1, rows 5 thru 1
    for r in range(5, 0, -1):
        if (b[r][0] != " "):
            if (b[r-1][0] == " "): # empty spot above
                return 0
            elif (b[r][1] == " " or b[r-1][1] == " "): # empty spot to the right or right-diagonal
                return 1

    # scan column 6, rows 5 thru 1
    for r in range(5, 0, -1):
        if (b[r][6] != " "):
            if (b[r-1][6] == " "): # empty spot above
                return 6
            elif (b[r][5] == " " or b[r-1][5] == " "): # empty spot to the left or left-diagonal
                return 5

    # scan columns 1-5, rows 5 thru 1
    for r in range(5, 0, -1):
        for c in range(1,6):
            if (b[r][c] != " "):
                if (b[r-1][c] == " "): # empty spot above
                    return c
                elif (b[r][c+1] == " " or b[r-1][c+1] == " "): # empty spot to the right or right-diagonal
                    return c+1
                elif (b[r][c-1] == " " or b[r-1][c-1] == " "): # empty spot to the left or left-diagonal
                    return c-1

# undo_turns goes to the locations of the player and computer's most recent
# checker placements and overwrites their checkers as space characters.
def undo_turns(b, p_coords, c_coords):
    # b: 6x7 matrix
    # p_coords: list where item 0 is row, item 1 is column, of player's checker location
    # c_coords: list where item 0 is row, item 1 is column, of computer's checker location
    b[p_coords[0]][p_coords[1]] = " "
    b[c_coords[0]][c_coords[1]] = " "

# grab_row looks at a particular column of the game board from top to bottom
# and returns the row number of the first checker it finds.
def grab_row(b, c):
    # b: 6x7 matrix
    # c: column number
    for r in range(6):
        if (b[r][c] != " "):
            return r

def Columns_Check(board):
    flag = 0
    for s in range(7):
        m = 0 
        #scanning the column space
        if (board[m][s]== " "): 
            #check for three in a row
            for c in range(1, 5, 1): 
               if (board[m+c][s] != " "):
                flag = flag + 1 
            if (flag >= 2):
                return s
    if(flag < 2):
        col = random_column(board)
        return col

def rows_Check(board):
    runtimes = 0
    for g in range(5,-1,-1):
        a = 0
        for a in range(7):
            if(board[g][a == " "]):
                
                #scanning the rows 
                if(a <= 2): 
                    #check just in front
                    for k in range(1,3,1):
                        if(board[g][a+k]!= " "):
                            runtimes = runtimes + 1 
                    if(runtimes >= 3):
                        return g
            
                elif(a == 3):
                    #must check both front and back
                    for i in range(1,3,1):
                        if(board[g][a+i]!= " "):
                            runtimes = runtimes + 1 
            
                    for z in range(1,3,1):
                        if(board[g][a-z]!= " "):
                            runtimes = runtimes + 1 
            
                    if(runtimes >= 3):
                        return g
            
                elif(a>= 4):
                    #checks everything behind only 
                    for n in range(1,3,1):                                                  
                        if(board[g][a-n]!= " "):
                            runtimes = runtimes + 1 
                    if(runtimes >= 3):
                        return g

    if(runtimes < 2):
        col = random_column(board)
        return col

def main():
    # We will increment turns by 1 after the player's turn and after the computer's turn.
    turns = 0

    # We represent the computer's checker with the diamond unicode character
    # and the player's checker with the heart unicode character.
    computer = '\u2666'
    player = '\u2665'

    print("Welcome to Connect4.")
    print("The player's checkers are hearts:", player)
    print("The computer's checkers are diamonds:", computer)

    # Create and display the Connect4 board to the user.
    game_board = generate_board()
    display_board(game_board)
    playerTurns = 0
    
    # Loop the player and computer taking turns.
    while(True):
        
        print("\nIt's the player's turn.")
        print("Which column will you place your checker?")
        column_choice = int(input("Enter a column number between 0 and 6: "))
        
        # Force user to pick a column within 0 and 6 and with free spots.
        while (not valid_column(game_board, column_choice)):
            print("Invalid column input. Try again.")
            column_choice = int(input("Enter a column number between 0 and 6: "))

        # Player's turn.
        take_turn(game_board, column_choice, player)
        turns = turns + 1
        playerTurns = playerTurns + 1
        display_board(game_board)
        
        # Store coordinates of player's checker placement.
        player_row = grab_row(game_board, column_choice)
        player_coords = [player_row, column_choice]
        
        # Check if someone has won the game.
        for k in range(3):
            for i in range(4):    
                win = triple_check(game_board, k, i, computer, player)
                if (win == "Computer"):
                    print("------------------------")
                    print("Computer won the game!")
                    print("------------------------")
                    sys.exit()
                elif (win == "Player"):
                    print("------------------------")
                    print("Player won the game!")
                    print("------------------------")
                    sys.exit()
        
        # Computer's turn.
        print("\nIt's the computer's turn.")
        
        
        # Randomly choose a pre-determined computer move.
        x = random.randint(1,4)
        #x = 2
        if (x == 1 or playerTurns < 3):
            computer_choice = random_column(game_board)
        elif (x == 2):
            computer_choice = strategic_column(game_board)
        elif (x == 3):
            computer_choice = rows_Check(game_board)
        elif (x == 4):
            computer_choice = Columns_Check(game_board)
        
        # Place computer's checker.
        take_turn(game_board, computer_choice, computer)
        turns = turns + 1
        display_board(game_board)
        
        # Store coordinates of computer's checker placement.
        computer_row = grab_row(game_board, computer_choice)
        computer_coords = [computer_row, computer_choice]
        
        # Undo button.
        print("\nWant to undo this round of turns?")
        undo = input("Enter 1 to undo or 2 to continue without undoing: ")
        if (undo == "1"):
            undo_turns(game_board, player_coords, computer_coords)
            display_board(game_board)
            turns = turns - 2
        elif (undo == "2"):
            print("You chose to keep going without undoing.")
        
        # Check if there's a tie
        if(turns == 42):
            print("This is a tie. Nobody wins.")
            sys.exit()

        # Check if someone has won the game.
        for k in range(3):
            for i in range(4):    
                win = triple_check(game_board, k, i, computer, player)
                if (win == "Computer"):
                    print("------------------------")
                    print("Computer won the game!")
                    print("------------------------")
                    sys.exit()
                elif (win == "Player"):
                    print("------------------------")
                    print("Player won the game!")
                    print("------------------------")
                    sys.exit()        

# Main ---------------------------------------------------------------------
        
main()