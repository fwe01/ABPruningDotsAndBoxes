from tkinter import *
import numpy as np


class DotsAndBoxes:
    # Some class constants that can be changed quickly
    BOARD_SIZE = 600
    NUMBER_OF_DOTS = 6  # total amount of dots is n x n
    SYMBOL_SIZE = (BOARD_SIZE / 3 - BOARD_SIZE / 8) / 2
    SYMBOL_THICKNESS = 50
    DOT_COLOR = '#7BC043'
    PLAYER1_COLOR = '#0492CF'
    PLAYER1_COLOR_LIGHT = '#67B0CF'
    PLAYER2_COLOR = '#EE4035'
    PLAYER2_COLOR_LIGHT = '#EE7E77'
    THEME_COLOR = '#7BC043'
    NEUTRAL_COLOR = '#111111'
    DOT_WIDTH = 0.25 * BOARD_SIZE / NUMBER_OF_DOTS
    EDGE_WIDTH = 0.1 * BOARD_SIZE / NUMBER_OF_DOTS
    DISTANCE_BETWEEN_DOTS = BOARD_SIZE / NUMBER_OF_DOTS
    ROW = 'row'
    COLUMN = 'col'

    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=self.BOARD_SIZE, height=self.BOARD_SIZE)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.player1_starts = True
        self.reset_board = False
        self.player1_turn = None
        self.board_status = None
        self.row_status = None
        self.col_status = None
        self.turntext_handle = []
        self.already_marked_boxes = []

        self.refreshBoard()
        self.restartGame()

    def mainloop(self):
        self.window.mainloop()

    def restartGame(self):
        self.refreshBoard()
        self.board_status = np.zeros(shape=(self.NUMBER_OF_DOTS - 1, self.NUMBER_OF_DOTS - 1))
        self.row_status = np.zeros(shape=(self.NUMBER_OF_DOTS, self.NUMBER_OF_DOTS - 1))
        self.col_status = np.zeros(shape=(self.NUMBER_OF_DOTS - 1, self.NUMBER_OF_DOTS))

        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.showTurn()

    # UTILITY FUNCTIONS

    def isGridOccupiedUtil(self, logical_pos, row_column_status):
        row = logical_pos[0]
        column = logical_pos[1]

        occupied = True

        if row_column_status == self.ROW and self.row_status[column][row] == 0:
            occupied = False
        elif row_column_status == self.COLUMN and self.col_status[column][row] == 0:
            occupied = False

        return occupied

    def convGridToLogicalPosUtil(self, grid_pos):
        grid_pos = np.array(grid_pos)
        pos = (grid_pos - self.DISTANCE_BETWEEN_DOTS / 4) // (self.DISTANCE_BETWEEN_DOTS / 2)

        row_column_status = False
        logical_pos = []

        if pos[1] % 2 == 0 and (pos[0] - 1) % 2 == 0:
            r = int((pos[0] - 1) // 2)
            c = int(pos[1] // 2)
            logical_pos = [r, c]
            row_column_status = self.ROW
            # self.row_status[c][r]=1
        elif pos[0] % 2 == 0 and (pos[1] - 1) % 2 == 0:
            c = int((pos[1] - 1) // 2)
            r = int(pos[0] // 2)
            logical_pos = [r, c]
            row_column_status = self.COLUMN

        return logical_pos, row_column_status

    def isGameOverUtil(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def markBox(self):
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = self.PLAYER1_COLOR_LIGHT
                self.fillBox(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                color = self.PLAYER2_COLOR_LIGHT
                self.fillBox(box, color)

    def updateBoard(self, logical_pos, row_column_status):
        row = logical_pos[0]
        column = logical_pos[1]
        val = 1

        if self.player1_turn:
            val = -1

        if column < (self.NUMBER_OF_DOTS - 1) and row < (self.NUMBER_OF_DOTS - 1):
            self.board_status[column][row] += val

        if row_column_status == self.ROW:
            self.row_status[column][row] = 1
            if column >= 1:
                self.board_status[column - 1][row] += val

        elif row_column_status == self.COLUMN:
            self.col_status[column][row] = 1
            if row >= 1:
                self.board_status[column][row - 1] += val

    def makeEdge(self, logical_position, row_column_status):
        start_x = start_y = end_x = end_y = 0

        if row_column_status == self.ROW:
            start_x = self.DISTANCE_BETWEEN_DOTS / 2 + logical_position[0] * self.DISTANCE_BETWEEN_DOTS
            end_x = start_x + self.DISTANCE_BETWEEN_DOTS
            start_y = self.DISTANCE_BETWEEN_DOTS / 2 + logical_position[1] * self.DISTANCE_BETWEEN_DOTS
            end_y = start_y
        elif row_column_status == self.COLUMN:
            start_y = self.DISTANCE_BETWEEN_DOTS / 2 + logical_position[1] * self.DISTANCE_BETWEEN_DOTS
            end_y = start_y + self.DISTANCE_BETWEEN_DOTS
            start_x = self.DISTANCE_BETWEEN_DOTS / 2 + logical_position[0] * self.DISTANCE_BETWEEN_DOTS
            end_x = start_x

        if self.player1_turn:
            color = self.PLAYER1_COLOR
        else:
            color = self.PLAYER2_COLOR

        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=self.EDGE_WIDTH)

    def displayGameOver(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        player2_score = len(np.argwhere(self.board_status == 4))

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Player 1 Wins '
            color = self.PLAYER1_COLOR
        elif player2_score > player1_score:
            text = 'Player 2 Wins '
            color = self.PLAYER2_COLOR
        else:
            text = 'Its a tie'
            color = self.NEUTRAL_COLOR

        self.canvas.delete("all")
        self.canvas.create_text(self.BOARD_SIZE / 2, self.BOARD_SIZE / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.BOARD_SIZE / 2, 5 * self.BOARD_SIZE / 8, font="cmr 40 bold", fill=self.THEME_COLOR,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(self.BOARD_SIZE / 2, 3 * self.BOARD_SIZE / 4, font="cmr 30 bold", fill=self.THEME_COLOR,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.BOARD_SIZE / 2, 15 * self.BOARD_SIZE / 16, font="cmr 20 bold",
                                fill=self.NEUTRAL_COLOR, text=score_text)

    def refreshBoard(self):
        for i in range(self.NUMBER_OF_DOTS):
            x = i * self.DISTANCE_BETWEEN_DOTS + self.DISTANCE_BETWEEN_DOTS / 2
            self.canvas.create_line(x, self.DISTANCE_BETWEEN_DOTS / 2, x,
                                    self.BOARD_SIZE - self.DISTANCE_BETWEEN_DOTS / 2, fill='gray', dash=(2, 2))
            self.canvas.create_line(self.DISTANCE_BETWEEN_DOTS / 2, x,
                                    self.BOARD_SIZE - self.DISTANCE_BETWEEN_DOTS / 2, x, fill='gray', dash=(2, 2))

        for i in range(self.NUMBER_OF_DOTS):
            for j in range(self.NUMBER_OF_DOTS):
                start_x = i * self.DISTANCE_BETWEEN_DOTS + self.DISTANCE_BETWEEN_DOTS / 2
                end_x = j * self.DISTANCE_BETWEEN_DOTS + self.DISTANCE_BETWEEN_DOTS / 2
                self.canvas.create_oval(start_x - self.DOT_WIDTH / 2, end_x - self.DOT_WIDTH / 2,
                                        start_x + self.DOT_WIDTH / 2, end_x + self.DOT_WIDTH / 2, fill=self.DOT_COLOR,
                                        outline=self.DOT_COLOR)

    def showTurn(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = self.PLAYER1_COLOR
        else:
            text += 'Player2'
            color = self.PLAYER2_COLOR

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(self.BOARD_SIZE - 5 * len(text),
                                                       self.BOARD_SIZE - self.DISTANCE_BETWEEN_DOTS / 8,
                                                       font="cmr 15 bold", text=text, fill=color)

    def fillBox(self, box, color):
        start_x = self.DISTANCE_BETWEEN_DOTS / 2 + box[1] * self.DISTANCE_BETWEEN_DOTS + self.EDGE_WIDTH / 2
        start_y = self.DISTANCE_BETWEEN_DOTS / 2 + box[0] * self.DISTANCE_BETWEEN_DOTS + self.EDGE_WIDTH / 2
        end_x = start_x + self.DISTANCE_BETWEEN_DOTS - self.EDGE_WIDTH
        end_y = start_y + self.DISTANCE_BETWEEN_DOTS - self.EDGE_WIDTH
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convGridToLogicalPosUtil(grid_position)
            if valid_input and not self.isGridOccupiedUtil(logical_positon, valid_input):
                self.updateBoard(logical_positon, valid_input)
                self.makeEdge(logical_positon, valid_input)
                self.markBox()
                self.refreshBoard()
                self.player1_turn = not self.player1_turn

                if self.isGameOverUtil():
                    # self.canvas.delete("all")
                    self.displayGameOver()
                else:
                    self.showTurn()
        else:
            self.canvas.delete("all")
            self.restartGame()
            self.reset_board = False

