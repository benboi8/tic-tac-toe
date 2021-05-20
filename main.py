import pygame as pg
import pygame.gfxdraw 

pg.init()

clock = pg.time.Clock()

sf = 2
width, height = 640, 360
screen = pg.display.set_mode((width * sf, height * sf))

lightGray = (205, 205, 205)
darkGray = (55, 55, 55)

running = True

winObjs = []
sideBarObjs = []
allButtons = []

def DrawRectOutline(surface, color, rect, width=1, outWards=False):
	x, y, w, h = rect
	width = max(width, 1)  # Draw at least one rect.
	width = min(min(width, w//2), h//2)  # Don't overdraw.

	# This draws several smaller outlines inside the first outline
	# Invert the direction if it should grow outwards.
	if outWards:
		for i in range(int(width)):
			pg.gfxdraw.rectangle(surface, (x-i, y-i, w+i*2, h+i*2), color)
	else:
		for i in range(int(width)):
			pg.gfxdraw.rectangle(surface, (x+i, y+i, w-i*2, h-i*2), color)


class Label:
	def __init__(self, surface, rect, colors, textData, drawData=(True, False), lists=[]):
		self.surface = surface
		self.ogRect = pg.Rect(rect)
		self.borderColor = colors[0]
		self.backgroundColor = colors[1]
		self.text = textData[0]
		self.ogFontSize = textData[1]
		self.textColor = textData[2]
		self.drawBorder = drawData[0]
		self.drawBackground = drawData[1]

		for l in lists:
			l.append(self)

		self.Rescale()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)
		fontSize = self.ogFontSize * sf
		self.font = pg.font.SysFont("arial", fontSize)
		self.textSurface = self.font.render(self.text, True, self.textColor)

	def UpdateText(self, text):
		self.text = text
		self.textSurface = self.font.render(self.text, True, self.textColor)

	def Draw(self):
		if self.drawBorder:
			if self.drawBackground:
				pg.draw.rect(self.surface, self.backgroundColor, self.rect)
			DrawRectOutline(self.surface, self.borderColor, self.rect, 1.5 * sf)
		else:
			if self.drawBackground:
				pg.draw.rect(self.surface, self.borderColor, self.rect)

		self.surface.blit(self.textSurface, ((self.rect.x + self.rect.w // 2) - self.textSurface.get_width() // 2, (self.rect.y + self.rect.h // 2) - self.textSurface.get_height() // 2))


class Button:
	def __init__(self, surface, rect, colors, functionName, textData, lists=[allButtons]):
		self.surface = surface
		self.ogRect = pg.Rect(rect)
		self.borderColor = colors[0]
		self.backgroundColor = colors[1]
		self.functionName = functionName
		self.text = textData[0]
		self.ogFontSize = textData[1]
		self.textColor = textData[2]

		for l in lists:
			l.append(self)

		self.Rescale()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)
		fontSize = self.ogFontSize * sf
		self.font = pg.font.SysFont("arial", fontSize)
		self.textSurface = self.font.render(self.text, True, self.textColor)

	def UpdateText(self, text):
		self.textSurface = self.font.render(text, True, self.textColor)

	def Draw(self):
		pg.draw.rect(self.surface, self.backgroundColor, self.rect)
		DrawRectOutline(self.surface, self.borderColor, self.rect, 1.5 * sf)

		self.surface.blit(self.textSurface, ((self.rect.x + self.rect.w // 2) - self.textSurface.get_width() // 2, (self.rect.y + self.rect.h // 2) - self.textSurface.get_height() // 2))

	def HandleEvent(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				if self.rect.collidepoint(pg.mouse.get_pos()):
					globals()[self.functionName]()


def DrawLoop():
	global hasWon
	screen.fill(darkGray)

	board.Draw()

	if hasWon:
		for obj in winObjs:
			obj.Draw()

	for obj in sideBarObjs:
		obj.Draw()

	pg.display.update()


class Board:
	def __init__(self, rect, colors):
		self.surface = screen
		self.ogRect = pg.Rect(rect)
		self.borderColor = colors[0]
		self.backgroundColor = colors[1]

		self.size = (3, 3)

		self.player = "X"
		self.numOfMoves = 0

		self.score = (0, 0)

		self.Rescale()
		self.CreateBoard()

	def Rescale(self):
		self.rect = pg.Rect(self.ogRect.x * sf, self.ogRect.y * sf, self.ogRect.w * sf, self.ogRect.h * sf)

	def CreateBoard(self):
		self.boardState = [["" for i in range(self.size[0])] for j in range(self.size[1])]
		self.boardRects = []
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				self.boardRects.append(pg.Rect(self.rect.x + (self.rect.w // self.size[0] * i), self.rect.y + (self.rect.h // self.size[1] * j), self.rect.w // self.size[0], self.rect.h // self.size[1]))

	def Draw(self):
		pg.draw.rect(self.surface, self.backgroundColor, self.rect)
		DrawRectOutline(self.surface, self.borderColor, self.rect, 2*sf)
		for rect in self.boardRects:
			DrawRectOutline(self.surface, self.borderColor, rect, 1*sf)

		counter = 0
		for row in self.boardState:
			for value in row:
				rect = self.boardRects[counter]
				font = pg.font.SysFont("arial", 140 * sf)
				text = font.render(str(value), True, self.borderColor)
				self.surface.blit(text, (rect.x + rect.w // 2 - text.get_width() // 2, rect.y + rect.h // 2 - text.get_height() // 2))
				counter += 1

	def HandleEvent(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				for index, rect in enumerate(self.boardRects):
					if rect.collidepoint(pg.mouse.get_pos()):
						self.Place(index)

	def GetBoardState(self):
		boardState = ""
		for row in self.boardState:
			for i, value in enumerate(row):
				if i % 3 == 0:
					boardState += "\n| {} ".format(value)
				else:
					if i % 3 == 2:
						boardState += "| {} |".format(value)
					else:
						boardState += "| {} ".format(value)
		return boardState

	def Place(self, index):	
		player = self.player
		x, y = index // 3, index % 3
		if self.boardState[x][y] != "X" and self.boardState[x][y] != "O":
			self.boardState[x][y] = player
			self.numOfMoves += 1
			self.CheckWin()

	def CheckWin(self):
		global gameInProgress, winner
		if self.CheckHorizontal() or self.CheckVeritical() or self.CheckDiagonal():
			if self.player == "X":
				self.score = (self.score[0] + 1, self.score[1])
			else:
				self.score = (self.score[0], self.score[1] + 1)
			Win()
		elif self.numOfMoves >= 9:
			self.player = "Tie"
			Win()

		if self.player == "X":
			self.player = "O"
		else:
			self.player = "X"

	def CheckHorizontal(self):
		wins = 0
		for y, yList in enumerate(self.boardState):
			for x in range(len(yList)):
				indexs = set([])
				for i in range(3):
					try:
						if self.boardState[y][x + i] == self.player:
							indexs.add((x + i, y))
						else:
							break
					except:
						break
				if len(indexs) >= 3:
					wins += 1
				indexs = set([])

		if wins >= 1:
			return True
		else:
			return False

	def CheckVeritical(self):
		wins = 0
		for y, yList in enumerate(self.boardState):
			for x in range(len(yList)):
				indexs = set([])
				for i in range(3):
					try:
						if self.boardState[y + i][x] == self.player:
							indexs.add((x, y + i))
						else:
							break
					except:
						break
				if len(indexs) >= 3:
					wins += 1
				indexs = set([])

		if wins >= 1:
			return True
		else:
			return False

	def CheckDiagonal(self):
		wins = 0
		for y, yList in enumerate(self.boardState):
			for x in range(len(yList)):
				indexs = set([])
				for i in range(3):
					try:
						if self.boardState[y + i][x + i] == self.player:
							indexs.add((x + i, y + i))
						else:
							break
					except:
						break
				if len(indexs) >= 3:
					wins += 1

				indexs = set([])
				for i in range(3):
					try:
						if x - i >= 0 and y + i >= 0:
							if self.boardState[y + i][x - i] == self.player:
								indexs.add((x - i, y + i))
							else:
								break
					except:
						break
				if len(indexs) >= 3:
					wins += 1

		if wins >= 1:
			return True
		else:
			return False


def CreateWinObjects():
	global winObjs
	winObjs = []
	Label(screen, (width - 135, height - 40, 130, 25), (lightGray, darkGray), ("", 14, lightGray), (True, True), lists=[winObjs])


def CreateSideBarObjs():
	global sideBarObjs
	sideBarObjs = []
	# scores
	Label(screen, (5, 40, 130, 25), (lightGray, darkGray), ("Player one score: 0", 12, lightGray), (True, True), lists=[sideBarObjs])
	Label(screen, (width - 135, 40, 130, 25), (lightGray, darkGray), ("Player two score: 0", 12, lightGray), (True, True), lists=[sideBarObjs])

	# titles
	Label(screen, (5, 10, 130, 25), (lightGray, darkGray), ("Player one: X", 15, lightGray), (True, True), lists=[sideBarObjs])
	Label(screen, (width - 135, 10, 130, 25), (lightGray, darkGray), ("Player two: O", 15, lightGray), (True, True), lists=[sideBarObjs])
	
	Button(screen, (5, height - 40, 130, 25), (lightGray, darkGray), "Restart", ("Restart", 16, lightGray), lists=[sideBarObjs, allButtons])


def Win():
	global hasWon
	hasWon = True
	CreateWinObjects()
	if board.player != "Tie":
		winObjs[0].UpdateText("Player {} has won.".format(board.player))
	else:
		winObjs[0].UpdateText("It was a tie.")

	sideBarObjs[0].UpdateText("Player one score: {}".format(board.score[0]))
	sideBarObjs[1].UpdateText("Player two score: {}".format(board.score[1]))


def Restart():
	global hasWon, board, winObjs
	winObjs = []
	hasWon = False
	try:
		score = board.score
	except:
		score = (0, 0)
	board = Board((width // 2 - height // 2, 0, height, height), (lightGray, darkGray))
	board.score = score


Restart()
CreateSideBarObjs()
while running:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		if not hasWon:
			board.HandleEvent(event)

		for button in allButtons:
			button.HandleEvent(event)

	DrawLoop()