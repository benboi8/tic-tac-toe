from clientMultiplayer import *

from GUI import *

class Cell(Button):
	def __init__(self, rect, colors, onClick, onClickArgs):
		super().__init__(rect, colors, onClick=onClick, onClickArgs=onClickArgs, text="", name="", surface=screen, drawData={}, textData={"fontSize": 140}, inputData={}, lists=[])


class Board:
	def __init__(self, rect, colors):
		self.surface = screen
		self.rect = pg.Rect(rect)
		self.backgroundColor = colors[0]
		self.borderColor = colors[1]
		self.winColor = colors[3]
		self.colors = colors

		self.size = (3, 3)

		self.players = ["X", "O"]
		self.currentPlayer = self.players[0]

		self.score = {"player1": 0, "player2": 0}

		self.currentPlayerLabel = Label((10, self.rect.y + self.rect.h // 2 - 105, 200, 100), (self.backgroundColor, self.borderColor), text=f"Player {self.currentPlayer} turn.")
		self.winnerLabel = Label((10, self.rect.y + self.rect.h // 2, 200, 100), (self.backgroundColor, self.borderColor), text=f"No winner.")
		self.restart = Button((width - 210, self.rect.y + self.rect.h // 2 - 50, 200, 100), self.colors, text="Restart", onClick=self.Restart)
		self.won = False

		self.CreateBoard()

	def CreateBoard(self):
		self.board = [[Cell(((i * self.rect.w // self.size[0]) + self.rect.x, (j * self.rect.h // self.size[1]) + self.rect.y, self.rect.w // self.size[0], self.rect.h // self.size[1]), self.colors, self.PlaceMove, [i, j]) for j in range(self.size[0])] for i in range(self.size[1])]

	def Draw(self):
		for row in self.board:
			for cell in row:
				cell.Draw()

	def HandleEvents(self, event):
		for row in self.board:
			for cell in row:
				cell.HandleEvent(event)

	def PlaceMove(self, i, j):
		if not self.won:
			if self.board[i][j].text not in self.players:
				self.board[i][j].UpdateText(self.currentPlayer)
				if self.currentPlayer == self.players[0]:
					self.currentPlayer = self.players[1]
				else:
					self.currentPlayer = self.players[0]

				self.currentPlayerLabel.UpdateText(f"Player {self.currentPlayer} turn.")
				for cell in self.CheckWin():
					cell.ogBackgroundColor = self.winColor
					cell.backgroundColor = self.winColor
					self.winnerLabel.UpdateText(f"Winner is {cell.text}")
					self.won = True

	def CheckWin(self):
		# check horizontal
		for x in range(self.size[0]):
			cells = []
			if self.board[0][x].text in self.players:
				for y in range(3):
					if self.board[y][x].text == self.board[0][x].text:
						cells.append(self.board[y][x])

			if len(cells) >= 3:
				return cells

		# check vertical
		for y in range(self.size[1]):
			cells = []
			if self.board[y][0].text in self.players:
				for x in range(3):
					if self.board[y][x].text == self.board[y][0].text:
						cells.append(self.board[y][x])

			if len(cells) >= 3:
				return cells

		# check diagonal
		if self.board[0][0].text in self.players:
			cells = []
			for i in range(3):
				if self.board[i][i].text == self.board[0][0].text:
					cells.append(self.board[i][i])
			
			if len(cells) >= 3:
				return cells

		if self.board[2][0].text in self.players:
			cells = []
			j = 0
			for i in range(2, -1, -1):
				if self.board[i][j].text == self.board[2][0].text:
					cells.append(self.board[i][j])
				j += 1					
			
			if len(cells) >= 3:
				return cells
		
		return []

	def Restart(self):
		self.currentPlayer = self.players[0]
		self.currentPlayerLabel.UpdateText(f"Player {self.currentPlayer} turn.")
		self.winnerLabel.UpdateText("No winner.")
		self.won = False
		self.CreateBoard()


def DrawLoop():
	screen.fill(darkGray)

	DrawAllGUIObjects()

	b.Draw()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	b.HandleEvents(event)


b = Board((width // 2 - height // 2, 0, height, height), (lightBlack, darkWhite, lightRed, lightBlue))


while running:
	clock.tick_busy_loop(fps)
	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	DrawLoop()
