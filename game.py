import numpy as np
import enum

class player(enum.Enum):
    nobody = 0
    maxie = 1 #always red
    minnie = 2 #always black

none = player.nobody.value
maxie = player.maxie.value
minnie = player.minnie.value

class Board:
    def __init__(self, turn):
        self.board = np.zeros((6, 7))
        self.h = len(self.board)
        self.w = len(self.board[0])
        self.turn = turn
        self.wboard = np.zeros((6,7))
        self.wboard[0,:] = 1
        self.wboard[:,0] = 1
        self.wboard[:,6] = 1
        self.wboard[1:6, 1] = 1.3
        self.wboard[1:6, 5] = 1.3
        self.wboard[1,1:6] = 1.3
        self.wboard[2,2:5] = 1.6
        self.wboard[2:,2] = 1.6
        self.wboard[2:,4] = 1.6
        self.wboard[3:,3] = 2

    def updateBoard(self, row, col, turn):

#        if row == 0:
#            self.board[row][col] = turn
#        else:
#            self.board[row-1][col] = none
#            self.board[row][col] = turn
        i = 0
        self.turn = turn
        while i < self.h and self.board[i][col] == none:
            if i > 0:
                self.board[i-1][col] = none
            self.board[i][col] = turn
            i += 1

        return self.row4(i - 1, col)

    def row4(self, row, col):

        #check vertically
        win = 0
        for i in range(-3, 4):
            fro = row + i
            if 0 <= fro and fro < self.h:
                if self.board[fro, col] == self.turn:
                    win += 1
                else:
                    win = 0
                if win == 4:
                    return self.turn
            else:
                win = 0

        #check horizontally
        win = 0
        for i in range(-3, 4):
            to = col + i
            if 0 <= to and to < self.w:
                if self.board[row, to] == self.turn:
                    win += 1
                else:
                    win = 0
                if win == 4:
                    return self.turn
            else:
                win = 0

        #check diagnolly y = -x
        win = 0
        for i in range(-3, 4):
            fro = row + i
            to = col + i
            if 0 <= fro and fro < self.h and 0 <= to and to < self.w:
                if self.board[fro, to] == self.turn:
                    win += 1
                else:
                    win = 0
                if win == 4:
                    return self.turn
            else:
                win = 0

        #check diagnolly y = x
        win = 0
        for i in range(-3, 4):
            fro = row - i
            to = col + i
            if 0 <= fro and fro < self.h and 0 <= to and to < self.w:
                if self.board[fro, to] == self.turn:
                    win += 1
                else:
                    win = 0
                if win == 4:
                    return self.turn
            else:
                win = 0

        return 0

    def amIAt(self, x, y):
        return self.board[x][y] == maxie

    def isCpuAt(self, x, y):
        return self.board[x][y] == minnie

    def isFullAt(self, i):
        return self.board[0][i] != none

    def removePieceAt(self, col):
        for i in range(self.h):
            if self.board[i][col] != none:
                self.board[i][col] = none
                break

    def inFavorOf(self):

        #horizontal analysis
        horizontal = self.winning(self.board, self.wboard, 0, self.h, 0, self.w, 1)
        + self.winning(self.board, self.wboard, 0, self.h, self.w-1, -1, -1)

        #verital analysis
        vertical = self.winning(self.board.T, self.wboard.T, 0, self.w, 0, self.h, 1)
        + self.winning(self.board.T, self.wboard.T, 0, self.w, self.h-1, -1, -1)

        return (horizontal + vertical + self.winningDiag()) / 6

    def winning(self, board, wboard, fro1, to1, fro2, to2, incr):
        favor = 0 # neutral
        blank = 1
        queue = []
        InARowMax = 0
        InARowMin = 0
        for row in range(fro1, to1):
            for col in range(fro2, to2, incr):
                if board[row][col] == none:
                    blank *= 1.1
                    InARowMax, InARowMin = 0, 0
                elif board[row][col] == maxie:
                    if len(queue) > 0 and queue[0] < 0:
                        favor += 1.5 ** (InARowMin-1) * blank * sum(queue[:-2])
                        favor += 4 ** (InARowMin-1) * blank * (wboard[row][col])
                        blank = 1
                        queue = []
                    queue.append(wboard[row][col])
                    InARowMax += 1
                    InARowMin = 0
                elif board[row][col] == minnie:
                    if len(queue) > 0 and queue[0] > 0:
                        favor += 1.5 ** (InARowMax-1) * blank * sum(queue[:-2])
                        favor += 4 ** (InARowMax-1) * blank * (-wboard[row][col])
                        blank = 1
                        queue = []
                    queue.append(-wboard[row][col])
                    InARowMin += 1
                    InARowMax = 0
            favor += 3 ** (InARowMax+InARowMin-1) * blank * sum(queue)
            blank = 1
            queue = []
            InARowMax = 0
            InARowMin = 0

        return favor

    def winningDiag(self):
        #diag analysis
        favor = 0
        for j in range(self.w-3):
            to = min(self.w-j, self.h)
            diag = [[self.board[i][i+j] for i in range(to)]]
            wdiag = [[self.wboard[i][i+j] for i in range(to)]]
            favor += self.winning(diag, wdiag, 0, 1, 0, to, 1)
            favor += self.winning(diag, wdiag, 0, 1, to-1, -1, -1)

        for j in range(self.h-3):
            to = min(self.w, self.h-j)
            diag = [[self.board[i+j][i] for i in range(to)]]
            wdiag = [[self.wboard[i+j][i] for i in range(to)]]
            favor += self.winning(diag, wdiag, 0, 1, 0, to, 1)
            favor += self.winning(diag, wdiag, 0, 1, to-1, -1, -1)

        return favor


class Game:

    def __init__(self):
        self.turn = np.random.randint(2) + 1# 1 is maxie, 2 is minnie
        self.board = Board(self.turn)
        self.status = none
        self.row = 0

    def move(self, col):
        self.status = self.board.updateBoard(self.row, col, self.turn)
        self.turn = 3 - self.turn

    def undo(self, col):
        self.board.removePieceAt(col)
        self.turn = 3 - self.turn

    def isMyTurn(self):
        return self.turn == maxie

    def isCpuTurn(self):
        return self.turn == minnie

    def isOver(self):
        return self.status != none

    def moves(self):
        moves = [i for i in range(self.board.w) if not self.board.isFullAt(i)]
        return moves

    def estimate(self):
        return self.board.inFavorOf()







