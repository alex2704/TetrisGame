import sys, random
from enum import Enum


class CellStatus(Enum):
    current = 1
    fixed = 2
    empty = 3
class Board():

    BoardWidth = 10
    BoardHeight = 16
    Speed = 500
    def __init__(self):
        self.initBoard()

    def initBoard(self):
        #self.numLinesRemoved = 0

        self.board = []

        self.isStarted = True
        self.isPaused = False
        self.fillField()
        self.newPiece()


    def __getitem__(self, r, c):
        return self.board[r][c]
    # заполнить поле в начале игры
    def fillField(self):
        for rows in range(Board.BoardHeight):
            row = []
            for columns in range(Board.BoardWidth):
                row.append(Cell(columns, rows, CellStatus.empty, 'transparent'))
            self.board.append(row)
    # Начало игры
    def startGame(self):

        self.isStarted = True
        self.numLinesRemoved = 0



    # Генерация нового кусочка
    def newPiece(self):
        if self.isStarted:
            self.currentfigure = Figure()
            for i in range(len(self.currentfigure.block)):
                if self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].cellstatus != CellStatus.fixed:
                    self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].cellstatus = CellStatus.current
                    self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].color =\
                        self.currentfigure.block[i].color
                else:
                    self.isStarted = False
                    for i in range(len(self.currentfigure.block)):
                        self.board[self.currentfigure.block[i].y][
                            self.currentfigure.block[i].x].cellstatus = CellStatus.fixed
                        self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].color = \
                            self.currentfigure.block[i].color

    # очистка ячейки от блока
    def ClearCell(self):
        for i in range(len(self.currentfigure.block)):
            self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].cellstatus = CellStatus.empty
            self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].color = 'transparent'


    # записывает в ячейку fixed block
    def WriteFixedBlock(self):
        for i in range(len(self.currentfigure.block)):
            self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].cellstatus = \
                CellStatus.fixed
            self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].color= \
                self.currentfigure.block[i].color
    def WriteCurrentBlock(self, i):
        self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].cellstatus = CellStatus.current
        self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].color = \
            self.currentfigure.block[i].color
    # Опустить вниз фигуру
    def lowerFigure(self):
        # проверка на фигуры снизу и границу board
        for i in range(len(self.currentfigure.block)):
            checkedindex = self.currentfigure.block[i].y + 1
            if (self.currentfigure.block[i].y < self.BoardHeight - 1 and \
                self.board[checkedindex][self.currentfigure.block[i].x].cellstatus \
                == CellStatus.fixed) or self.currentfigure.block[i].y >= self.BoardHeight - 1:
                self.WriteFixedBlock()
                self.ClearRow()
                self.CheckLose()
                self.newPiece()
                return
        # сдвиг
        self.ClearCell()
        self.movementY(1)
    # сдвиг влево фигуры
    def leftFigure(self):
        # проверка на границу board и блоки слева
        for i in range(len(self.currentfigure.block)):
            checkedindex = self.currentfigure.block[i].x-1
            if self.currentfigure.block[i].x <= 0 or (self.currentfigure.block[i].x > 0 and
                    self.board[self.currentfigure.block[i].y][checkedindex].cellstatus == CellStatus.fixed):
                return 0
        # сдвиг
        self.ClearCell()
        self.movementX(-1)
    # сдвиг вправо фигуры
    def movementX(self, a):
        for i in range(len(self.currentfigure.block)):
            self.currentfigure.block[i].x += a
            self.WriteCurrentBlock(i)
    def movementY(self, b):
        for i in range(len(self.currentfigure.block)):
            self.currentfigure.block[i].y += b
            self.WriteCurrentBlock(i)
    def rightFigure(self):
        # проверка на границу board и блоки справа
        for i in range(len(self.currentfigure.block)):
            checkedindex = self.currentfigure.block[i].x + 1
            if self.currentfigure.block[i].x >= self.BoardWidth-1 or (self.currentfigure.block[i].x > 0 and
                                                      self.board[self.currentfigure.block[
                                                          i].y][checkedindex].cellstatus == CellStatus.fixed):
                return 0
        # сдвиг вправо
        self.ClearCell()
        self.movementX(1)

    def rotate(self):
        self.currentfigure.ChangeFigures()
        self.currentfigure.ChooseTypeFigure()
        rotatedFigure = self.currentfigure.RotateFigureTest()
        for i in range(len(rotatedFigure)):
            if rotatedFigure[i].x >= self.BoardWidth or rotatedFigure[i].y >= self.BoardHeight:
                break
            if rotatedFigure[i].x < 0 or rotatedFigure[i].y < 0:
                break
            if self.board[rotatedFigure[i].y][rotatedFigure[i].x].cellstatus == CellStatus.fixed:
                break
        else:
            self.ClearCell()
            self.currentfigure.RotateFigure()
            for i in range(len(self.currentfigure.block)):
                self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].cellstatus = CellStatus.current
                self.board[self.currentfigure.block[i].y][self.currentfigure.block[i].x].color = \
                    self.currentfigure.block[i].color

    def ClearRow(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].cellstatus == CellStatus.fixed:
                    row = i
                else:
                    break
            else:
                self.numLinesRemoved += 1
                for k in range(len(self.board[row])):
                    self.board[row][k].cellstatus = CellStatus.empty
                    self.board[row][k].color = 'transparent'
                l = row - 1
                while l < row and l >= 0:
                    for m in range(len(self.board[l])):
                        if self.board[l][m].cellstatus == CellStatus.fixed:
                            self.board[l][m].cellstatus = CellStatus.empty
                            color = self.board[l][m].color
                            self.board[l][m].color = 'transparent'
                            q = l + 1
                            self.board[q][m].cellstatus = CellStatus.fixed
                            self.board[q][m].color = color
                    l -= 1

    def CheckLose(self):
        for i in range(len(self.board[0])):
            if self.board[0][i].cellstatus == CellStatus.fixed:
                self.LoseGame()
                break


    def LoseGame(self):
        self.isStarted = False

class Cell:
    def __init__(self, x, y, cellstatus, color):
        self.x = x
        self.y = y
        self.cellstatus = cellstatus
        self.color = color
class Block:
    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y

class Figure:
    def __init__(self):
        self.mainblock = Block(random.randint(3, Board.BoardWidth-3), 0, 0)
        #self.mainblock.color = 'red'
        self.ChangeFigures()
        self.indexTypeFigure = random.randint(0, len(self.figures) - 1)
        self.ChooseTypeFigure()
        self.indexBlock = 0
        self.block = self.TypeFigure[0]
        self.mainblock.color = self.indexTypeFigure

    def ChangeFigures(self):
        SquareTypes = (self.buildSquare(), self.buildSquare())
        StickTypes = (self.buildStick(1, 0, -1, 0, -2, 0), self.buildStick(0, -1, 0, -2, 0, 1))
        TTypes = (self.buildT(1, 0, -1, 0, 0, 1), self.buildT(0, -1, 0, 1, -1, 0),
                       self.buildT(-1, 0, 1, 0, 0, -1), self.buildT(0, -1, 0, 1, 1, 0))
        ZipperTypes = (self.buildZipper(-1, 0, 0, 1, 1, 1), self.buildZipper(0, -1, -1, 0, -1, 1))
        RakeTypes = (self.buildRake(-1, 0, 0, 1, 0, 2), self.buildRake(0, -1, -1, 0, -2, 0),
                          self.buildRake(1, 0, 0, -1, 0, -2), self.buildRake(0, 1, 1, 0, 2, 0))

        self.figures = (SquareTypes,
                        StickTypes,
                        TTypes,
                        ZipperTypes,
                        RakeTypes)


    def ChooseTypeFigure(self):
        self.TypeFigure = self.figures[self.indexTypeFigure]


    def RotateFigureTest(self):
        indexBlock = self.indexBlock
        TypeFigure = self.TypeFigure
        if indexBlock < len(TypeFigure)-1:
            indexBlock += 1
        else:
            indexBlock = 0
        return TypeFigure[indexBlock]

    def RotateFigure(self):
        if self.indexBlock < len(self.TypeFigure)-1:
            self.indexBlock += 1
        else:
            self.indexBlock = 0
        self.block =  self.TypeFigure[self.indexBlock]

    def buildSquare(self):
        return (self.mainblock,
        Block(self.mainblock.x+1, self.mainblock.y, 0),
        Block(self.mainblock.x, self.mainblock.y+1, 0),
        Block(self.mainblock.x+1, self.mainblock.y+1, 0))
    def buildStick(self, x1, y1, x2, y2, x3, y3):
        return (self.mainblock,
                Block(self.mainblock.x + x1, self.mainblock.y + y1, 1),
                Block(self.mainblock.x + x2, self.mainblock.y + y2, 1),
                Block(self.mainblock.x + x3, self.mainblock.y + y3, 1))
    def buildT(self, x1, y1, x2, y2, x3, y3):
        return (self.mainblock,
                Block(self.mainblock.x + x1, self.mainblock.y + y1, 2),
                Block(self.mainblock.x + x2, self.mainblock.y + y2, 2),
                Block(self.mainblock.x + x3, self.mainblock.y + y3, 2))
    def buildZipper(self, x1, y1, x2, y2, x3, y3):
        return (self.mainblock,
                Block(self.mainblock.x + x1, self.mainblock.y + y1, 3),
                Block(self.mainblock.x + x2, self.mainblock.y + y2, 3),
                Block(self.mainblock.x + x3, self.mainblock.y + y3, 3))
    def buildRake(self, x1, y1, x2, y2, x3, y3):
        return (self.mainblock,
                Block(self.mainblock.x + x1, self.mainblock.y + y1, 4),
                Block(self.mainblock.x + x2, self.mainblock.y + y2, 4),
                Block(self.mainblock.x + x3, self.mainblock.y + y3, 4))