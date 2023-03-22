#Importing Necessary Libraries
import tkinter as tk
import numpy as np
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
AI = 1
PLAYER = 2

#Creating Board class to initialize the board of the Connect4 game
class Board:
    #Creating the some class attributes such as values of the board (char), row and column size of the board
    char = [" ", "X", "O"]
    RowSize = 6
    ColumnSize = 7
    
    #It is the constructor of the class. Here, we create instance attributes of the class such as the initial state of the board
    def __init__(self):
        #Initializing board of the game as a numpy array
        self.grid = np.zeros((self.RowSize, self.ColumnSize)).astype("int")
        #drawn_symbols array will let us change the color of the symbols in case of winning
        self.drawn_symbols = [['', '', '', '', '', '', ''], 
                              ['', '', '', '', '', '', ''], 
                              ['', '', '', '', '', '', ''], 
                              ['', '', '', '', '', '', ''], 
                              ['', '', '', '', '', '', ''], 
                              ['', '', '', '', '', '', '']]

    #Creating a function to reinitialize the game. This function changes all values empty string which is the initial state 
    #of drawn_symbols array. And then, we also fill the grid array with 0s which represent the initial state of the board
    def reinit(self):
        # Clear grid
        for i in range(6):
            for j in range(7):
                if self.drawn_symbols[i][j] != '':
                    canvas.delete(self.drawn_symbols[i][j])
                    self.drawn_symbols[i][j] = ''
        self.grid.fill(0)


        
    def Moving(self, grid, row, col, piece):
        grid[row][col] = piece

    def CheckValidLocation(self, grid, col):
        for r in range(ROW_COUNT-1, -1, -1):
            if grid[r][col] == 0:
                return True

    def getNextRow(self, grid, col):
        for r in range(ROW_COUNT-1, -1, -1):
            if grid[r][col] == 0:
                return r
    
    
    def checkThree(self, grid, piece):
        threeCount = 0
        for r in range(ROW_COUNT-1):
            for c in range(COLUMN_COUNT-1):
                if c < COLUMN_COUNT-3:
                    if grid[r][c] == grid[r][c+1] == grid[r][c+2] == piece and grid[r][c+3] == 0:
                        threeCount += 1
                    if r < ROW_COUNT-3:
                        if grid[r][c] == grid[r+1][c+1] == grid[r+2][c+2] == piece and grid[r+3][c+3] == 0:
                            threeCount += 1
                if c >= 3:
                    if grid[r][c] == grid[r][c-1] == grid[r][c-2] == piece and grid[r][c-3] == 0:
                        threeCount += 1
                    if r < ROW_COUNT-3:
                        if grid[r][c] == grid[r+1][c-1] == grid[r+2][c-2] == piece and grid[r+3][c-3] == 0:
                            threeCount += 1
                if r < ROW_COUNT-3:
                    if grid[r][c] == grid[r+1][c] == grid[r+2][c] == piece and grid[r+3][c] == 0:
                        threeCount += 1
        return threeCount        
        

    def checkTwo(self, grid, piece):
        twoCount = 0
        for r in range(ROW_COUNT-1):
            for c in range(COLUMN_COUNT-1):
                if c < COLUMN_COUNT-3:
                    if grid[r][c] == grid[r][c+1] == piece and grid[r][c+2] == grid[r][c+3] == 0:
                        twoCount += 1
                    if r < ROW_COUNT-3:
                        if grid[r][c] == grid[r+1][c+1] == piece and grid[r+2][c+2] == grid[r+3][c+3] == 0:
                            twoCount += 1
                if c >= 3:
                    if grid[r][c] == grid[r][c-1] == piece and grid[r][c-2] == grid[r][c-3] == 0:
                        twoCount += 1
                    if r < ROW_COUNT-3:
                        if grid[r][c] == grid[r+1][c-1] == piece and grid[r+2][c-2] == grid[r+3][c-3] == 0:
                            twoCount += 1
                if r < ROW_COUNT-3:
                    if grid[r][c] == grid[r+1][c] == piece and grid[r+2][c] == grid[r+3][c] == 0:
                        twoCount += 1
        return twoCount


    def calculateScore(self, grid, piece):
        threeScore = self.checkThree(grid, AI) * 1000
        twoScore = self.checkTwo(grid, AI) * 10
        playerThreeScore = self.checkThree(grid, PLAYER) * 1000
        playerTwoScore = self.checkTwo(grid, PLAYER) * 10
        score = twoScore + threeScore - playerTwoScore - playerThreeScore
        return score

    def TakingBestMove(self, grid, piece):
        playableLocations = self.findPlayableLocations(grid)
        print(playableLocations)
        bestScore = float("-inf")
        bestCol = random.choice(playableLocations)
        for col in playableLocations:
            row = self.getNextOpenRow(grid, col)
            tempBoard = grid.copy()
            self.Moving(tempBoard, row, col, piece)
            if self.winCheck(tempBoard, AI):
                score = 100000
            else:
                score = self.calculateScore(tempBoard, piece)
            if score > bestScore:
                bestScore = score
                bestCol = col
        return bestCol

        
        

    def getNextOpenRow(self, grid, col):
        for r in range(ROW_COUNT-1, -1, -1):
            if grid[r][col] == 0:
                return r

    def findPlayableLocations(self, grid):
        playableLocations = []
        for col in range(COLUMN_COUNT):
            if self.CheckValidLocation(grid, col):
                playableLocations.append(col)
        return playableLocations

        

    def winCheck(self, grid, piece):
        # Check for win
        # Check horizontal
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if grid[r][c] == piece and grid[r][c+1] == piece and grid[r][c+2] == piece and grid[r][c+3] == piece:
                    return True

        # Check vertical
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if grid[r][c] == piece and grid[r+1][c] == piece and grid[r+2][c] == piece and grid[r+3][c] == piece:
                    return True

        # Check diagonal right
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if grid[r][c] == piece and grid[r+1][c+1] == piece and grid[r+2][c+2] == piece and grid[r+3][c+3] == piece:
                    return True

        # Check diagonal left
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if grid[r][c] == piece and grid[r-1][c+1] == piece and grid[r-2][c+2] == piece and grid[r-3][c+3] == piece:
                    return True

    #Creating a function to draw symbols on each box in the grid
    def draw_symbol(self, x, y, symbol):
        self.drawn_symbols[x][y] = canvas.create_text((y + 0.5) * (height // 6), (x + 0.5) * (width // 7),
                            font = ("Calibri", width // 7), text = symbol,
                            fill = 'black')

    #Creating check_victory function. This function checks all possible victory cases of the game including column, row, and 
    #diognal alignments and changes color of winning symbols
    def check_victory(self):
        #Checking Column Alignment
        for r in range(self.RowSize):
            for c in range(self.ColumnSize - 3):
                if self.grid[r][c] == self.grid[r][c + 1] == self.grid[r][c + 2] == self.grid[r][c + 3] != 0:
                    #Changing color of winning symbols
                    canvas.itemconfig(self.drawn_symbols[r][c], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r][c + 1], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r][c + 2], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r][c + 3], fill = 'red')
                    return True

        #Checking Row Alignment
        for r in range(self.RowSize - 3):
            for c in range(self.ColumnSize):
                if self.grid[r][c] == self.grid[r + 1][c] == self.grid[r + 2][c] == self.grid[r + 3][c] != 0:
                    #Changing color of winning symbols
                    canvas.itemconfig(self.drawn_symbols[r][c], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r + 1][c], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r + 2][c], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r + 3][c], fill = 'red')
                    return True

        #Checking Diognal 1 Alignment (Top to Bottom)
        for r in range(self.RowSize - 3):
            for c in range(self.ColumnSize - 3):
                if self.grid[r][c] == self.grid[r + 1][c + 1] == self.grid[r + 2][c + 2] == self.grid[r + 3][c + 3] != 0:
                    #Changing color of winning symbols
                    canvas.itemconfig(self.drawn_symbols[r][c], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r + 1][c + 1], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r + 2][c + 2], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r + 3][c + 3], fill = 'red')
                    return True
    
        #Checking Diognal 2 Alignment (Bottom to Top)
        for r in range(3, self.RowSize):
            for c in range(self.ColumnSize - 3):
                if self.grid[r][c] == self.grid[r - 1][c + 1] == self.grid[r - 2][c + 2] == self.grid[r - 3][c + 3] != 0:
                    #Changing color of winning symbols
                    canvas.itemconfig(self.drawn_symbols[r][c], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r - 1][c + 1], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r - 2][c + 2], fill = 'red')
                    canvas.itemconfig(self.drawn_symbols[r - 3][c + 3], fill = 'red')
                    return True

#Creating Connect4 class
class Connect4:
    #Setting some class attributes such as symbols and turn
    symbols = [" ", "O", "X"]
    turn = 1
    human_move = True
    
    #Constructor of the class. Here, we create object from Board() class, set the game on, and make information label 
    #user's choice. Then, we change text of this label to display which turn it is and which player is playing
    def __init__(self, info_label):
        self.board = Board()
        self.game_on = True
        self.information_label = info_label
        self.information_label['text'] = "Turn " + str(self.turn) + " - Player " + str((self.turn-1) % 2 + 1) + " is playing"
        #Attributes of controlling functions of buttons for each column
        self.x = 0
        self.y = 0
        self.x1 = 0
        self.y1 = 5
        self.x2 = 1
        self.y2 = 5
        self.x3 = 2
        self.y3 = 5
        self.x4 = 3
        self.y4 = 5
        self.x5 = 4
        self.y5 = 5
        self.x6 = 5
        self.y6 = 5
        self.x7 = 6
        self.y7 = 5
        
    #We also have reinit function in Connect4 which reinitialize the attributes of this class. This is the main reason that
    #we have reinit() function in both classes
    def reinit(self):
        self.board.reinit()
        self.game_on = True
        self.turn = 1
        self.information_label['text'] = "Turn " + str(self.turn) + " - Player " + str((self.turn-1) % 2 + 1) + " is playing"
        self.information_label['fg'] = 'black'
        #We also reinitialize the parameters of controlling functions of buttons so that everything starts from beginning
        self.x = 0
        self.y = 0
        self.x1 = 0
        self.y1 = 5
        self.x2 = 1
        self.y2 = 5
        self.x3 = 2
        self.y3 = 5
        self.x4 = 3
        self.y4 = 5
        self.x5 = 4
        self.y5 = 5
        self.x6 = 5
        self.y6 = 5
        self.x7 = 6
        self.y7 = 5
    
    def ai_turn(self):
        col = self.board.TakingBestMove(self.board.grid, AI)
        print(self.board.grid)
        if self.board.CheckValidLocation(self.board.grid, col):
            row = self.board.getNextRow(self.board.grid, col)
        self.move(col, row)
    
    #Following 7 function are for controlling the button for each column
    def column1(self):
        if self.y1 > 0:
            if self.board.grid[self.y1][self.x1] == 0:
                self.x = self.x1
                self.y = self.y1
            else:
                self.y1 = self.y1 - 1
                self.x = self.x1
                self.y = self.y1
            self.move(self.x, self.y)
        self.ai_turn()

    def column2(self):
        if self.y2 > 0:
            if self.board.grid[self.y2][self.x2] == 0:
                self.x = self.x2
                self.y = self.y2
            else:
                self.y2 = self.y2 - 1
                self.x = self.x2
                self.y = self.y2
            self.move(self.x, self.y)
        self.ai_turn()

    def column3(self):
        if self.y3 > 0:
            if self.board.grid[self.y3][self.x3] == 0:
                self.x = self.x3
                self.y = self.y3
            else:
                self.y3 = self.y3 - 1
                self.x = self.x3
                self.y = self.y3
            self.move(self.x, self.y)
        self.ai_turn()
    
    def column4(self):
        if self.y4 > 0:
            if self.board.grid[self.y4][self.x4] == 0:
                self.x = self.x4
                self.y = self.y4
            else:
                self.y4 = self.y4 - 1
                self.x = self.x4
                self.y = self.y4
            self.move(self.x, self.y)
        self.ai_turn()
    
    def column5(self):
        if self.y5 > 0:
            if self.board.grid[self.y5][self.x5] == 0:
                self.x = self.x5
                self.y = self.y5
            else:
                self.y5 = self.y5 - 1
                self.x = self.x5
                self.y = self.y5
            self.move(self.x, self.y)
        self.ai_turn()
        
    def column6(self):
        if self.y6 > 0:
            if self.board.grid[self.y6][self.x6] == 0:
                self.x = self.x6
                self.y = self.y6
            else:
                self.y6 = self.y6 - 1
                self.x = self.x6
                self.y = self.y6
            self.move(self.x, self.y)
        self.ai_turn()
        
    def column7(self):
        if self.y7 > 0:
            if self.board.grid[self.y7][self.x7] == 0:
                self.x = self.x7
                self.y = self.y7
            else:
                self.y7 = self.y7 - 1
                self.x = self.x7
                self.y = self.y7
            self.move(self.x, self.y)
        self.ai_turn()
        
    #Creating move function. Here, we have additionaly conditions that decide what will be the label (win or draw)
    def move(self, x, y):
        player = self.turn%2 + 1
        if self.game_on and self.board.grid[y][x] == 0:
            self.board.grid[y][x] = player
            self.board.draw_symbol(y, x, self.symbols[self.turn%2 + 1])
            if self.board.check_victory() or self.turn == 42:
                self.game_on = False
                self.information_label['fg'] = 'red'
                if self.board.check_victory():
                    self.information_label['text'] = "Player " + str((self.turn - 1)%2 + 1) + " wins !"
                else:
                    self.information_label['text'] = "This is a draw !"
                return
            #Incrementing turn and changing the label based on this incremented turn
            self.turn = self.turn + 1
            self.information_label['text'] = "Turn " + str(self.turn) + " - Player " + str((self.turn - 1)%2 + 1) + " is playing"
            print(self.board.grid)
            
#Setting details of canvas and its attributes such as width, height, and thickness of grid
width = 700
height = 600
grid_thickness = 5

#Initializing the window
window = tk.Tk()
#Setting a title to the window
window.title("Connect4")
#Setting size of the window
window.geometry("700x700")

#Creating canvas with its details 
canvas = tk.Canvas(window, bg = "white", width = width, height = height)

#Drawing Grid of the Connect4 Game

#Horizontal Lines
line1 = canvas.create_line(0, height//6, width, height//6, fill = 'black', width = grid_thickness)
line2 = canvas.create_line(0, (height//6)*2, width, (height//6)*2, fill = 'black', width = grid_thickness)
line3 = canvas.create_line(0, (height//6)*3, width, (height//6)*3, fill = 'black', width = grid_thickness)
line4 = canvas.create_line(0, (height//6)*4, width, (height//6)*4, fill = 'black', width = grid_thickness)
line5 = canvas.create_line(0, (height//6)*5, width, (height//6)*5, fill = 'black', width = grid_thickness)

#Vertical Lines
line7 = canvas.create_line(width//7, 0, width//7, height, fill = 'black', width = grid_thickness)
line8 = canvas.create_line((width//7)*2, 0, (width//7)*2, height, fill = 'black', width = grid_thickness)
line9 = canvas.create_line((width//7)*3, 0, (width//7)*3, height, fill = 'black', width = grid_thickness)
line10 = canvas.create_line((width//7)*4, 0, (width//7)*4, height, fill = 'black', width = grid_thickness)
line11 = canvas.create_line((width//7)*5, 0, (width//7)*5, height, fill = 'black', width = grid_thickness)
line12 = canvas.create_line((width//7)*6, 0, (width//7)*6, height, fill = 'black', width = grid_thickness)

#Initializing canvas grid to represent several buttons and label
canvas.grid(row = 0, column = 0, columnspan = 2)

#Creating a label that indicates information about the result of the game (win or draw)
information = tk.Label(window, text = "")
information.place(x = 322, y = 640)

#Creating object from TicTacToe() class
game = Connect4(information)

#Creating button to restart the game
buttonNewGame = tk.Button(window, text = 'New game', command = game.reinit)
buttonNewGame.place(x = 222, y = 670)

#Creating a button to quit the game
buttonQuit = tk.Button(window, text = 'Quit', command = window.destroy)
buttonQuit.place(x = 422, y = 670)

#Creating buttons for each column of Connect4 game board
button1 = tk.Button(window, text = "Column 1", command = game.column1)
button1.place(x = 22, y = 610)

button2 = tk.Button(window, text = "Column 2", command = game.column2)
button2.place(x = 122, y = 610)

button3 = tk.Button(window, text = "Column 3", command = game.column3)
button3.place(x = 222, y = 610)

button4 = tk.Button(window, text = "Column 4", command = game.column4)
button4.place(x = 322, y = 610)

button5 = tk.Button(window, text = "Column 5", command = game.column5)
button5.place(x = 422, y = 610)

button6 = tk.Button(window, text = "Column 6", command = game.column6)
button6.place(x = 522, y = 610)

button7 = tk.Button(window, text = "Column 7", command = game.column7)
button7.place(x = 622, y = 610)

#Showing the window
window.mainloop()