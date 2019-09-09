from Logic import Board, CellStatus
class GameTetris():
    def __init__(self):
        self.field = Board()
        self.field.startGame()

    def CheckOnSquare(self, k, l):
        return self.field.board[k][l].color == 0
    def CheckOnStick(self, k, l):
        return self.field.board[k][l].color == 1

    def CheckOnT(self, k, l):
        return self.field.board[k][l].color == 2

    def CheckOnZipper(self, k, l):
        return self.field.board[k][l].color == 3

    def CheckOnRake(self, k, l):
        return self.field.board[k][l].color == 4

    def GetLenMatrixRows(self):
        return len(self.field.board)

    def GetLenMatrixCols(self):
        return len(self.field.board[0])
    def GetCoordinateX(self, i, j):
        return self.field.board[i][j].x
    def GetCoordinateY(self, i, j):
        return self.field.board[i][j].y
    def Low(self):
        self.field.lowerFigure()
    def Left(self):
        self.field.leftFigure()
    def Right(self):
        self.field.rightFigure()
    def Rotate(self):
        self.field.rotate()
    def CheckTetrisLose(self):
        return not self.field.isStarted
    def GetScore(self):
        return self.field.numLinesRemoved
    def GetSpeed(self):
        return self.field.Speed