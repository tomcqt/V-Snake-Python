import vexdev
import numpy as np
import time
import random

# set up screen
Vex = vexdev.Vex()
Screen = Vex.Screen(21, 5, False)
Screen.setCursorTo(1, 1)

# start block code

# variables
global snakeDirection, snakeLength, snakePosItem, score
# lists
global snakePos0, snakePos1, snakePos2, snakePos3, snakePos4, fruitPos, snakeMovementVector, snakePosCalculated
# arrays
# none


def getSnakePos(index):
  global snakePosItem
  # 0 - 19
  if index < 20:
    snakePosItem = snakePos0[index]
  # 20 - 39
  elif index < 40:
    snakePosItem = snakePos1[index - 20]
  # 40 - 59
  elif index < 60:
    snakePosItem = snakePos2[index - 40]
  # 60 - 79
  elif index < 80:
    snakePosItem = snakePos3[index - 60]
  # 80 - 99
  elif index < 100:
    snakePosItem = snakePos4[index - 80]


def setSnakePos(index, value):
  global snakePos0, snakePos1, snakePos2, snakePos3, snakePos4
  # 0 - 19
  if index < 20:
    snakePos0[index] = value
  # 20 - 39
  elif index < 40:
    snakePos1[index - 20] = value
  # 40 - 59
  elif index < 60:
    snakePos2[index - 40] = value
  # 60 - 79
  elif index < 80:
    snakePos3[index - 60] = value
  # 80 - 99
  elif index < 100:
    snakePos4[index - 80] = value


def calculateSnakePos(position):
  global snakePosCalculated
  snakePosCalculated = [0, 0]  # placeholder, overwritten below
  snakePosCalculated[0] = (position - 1) % 100
  snakePosCalculated[1] = (position - 1) // 100  # // is floor division


def addRoomForNewPiece():
  snakePieceTemp = [0, 0]
  getSnakePos(0)
  snakePieceTemp[0] = snakePosItem
  for i in range(0, snakeLength):
    getSnakePos(i + 1)
    snakePieceTemp[1] = snakePosItem
    setSnakePos(i + 1, snakePieceTemp[0])
    snakePieceTemp[0] = snakePieceTemp[1]


def generateFruit():
  global fruitPos
  while True:
    fruitPos = [random.randint(1, 20), random.randint(1, 5)]
    # check if fruitPos is in snakePos0, snakePos1, snakePos2, snakePos3, or snakePos4
    fruitPosFormatted = fruitPos[1] * 100 + fruitPos[0] + 1
    if fruitPosFormatted not in snakePos0 and fruitPosFormatted not in snakePos1 and fruitPosFormatted not in snakePos2 and fruitPosFormatted not in snakePos3 and fruitPosFormatted not in snakePos4:
      break


def handleMovementVector(x, y, direction):
  global snakeMovementVector
  # 0 = up, 1 = right, 2 = down, 3 = left
  snakeMovementVector = [0, 0]  # placeholder, overwritten below
  if direction == 0:
    snakeMovementVector[0] = x
    snakeMovementVector[1] = y - 1
  elif direction == 1:
    snakeMovementVector[0] = x + 1
    snakeMovementVector[1] = y
  elif direction == 2:
    snakeMovementVector[0] = x
    snakeMovementVector[1] = y + 1
  elif direction == 3:
    snakeMovementVector[0] = x - 1
    snakeMovementVector[1] = y


def handleDeath():
  Screen.setCursorTo(7, 3)
  Screen.write("You died!")
  exit()  # add extra handling when porting to Vex


def checkCollisions():
  global score, snakeLength
  getSnakePos(0)
  calculateSnakePos(snakePosItem)

  handleMovementVector(snakePosCalculated[0], snakePosCalculated[1],
                       snakeDirection)

  nextPosFormatted = snakeMovementVector[1] * 100 + snakeMovementVector[0] + 1

  if snakeMovementVector[0] > 20 or snakeMovementVector[
      0] < 0 or snakeMovementVector[1] > 5 or snakeMovementVector[
          1] < 0:  # hitting wall
    handleDeath()
  elif nextPosFormatted in snakePos0 or nextPosFormatted in snakePos1 or nextPosFormatted in snakePos2 or nextPosFormatted in snakePos3 or nextPosFormatted in snakePos4:  # hitting self
    handleDeath()
  elif snakeMovementVector[0] == fruitPos[0] and snakeMovementVector[
      1] == fruitPos[1]:
    score += 25
    snakeLength += 1
    generateFruit()


def removeLastPiece():
  setSnakePos(snakeLength, 0)


def moveSnake():
  addRoomForNewPiece()
  getSnakePos(0)
  calculateSnakePos(snakePosItem)
  handleMovementVector(snakePosCalculated[0], snakePosCalculated[1],
                       snakeDirection)
  setSnakePos(0, snakeMovementVector[1] * 100 + snakeMovementVector[0] + 1)
  removeLastPiece()


def snakeLoop():
  checkCollisions()
  moveSnake()


def clearBoard():
  for y in range(1, 6):
    for x in range(1, 22):
      Screen.setCursorTo(x, y)
      Screen.write(" ")


def drawSnake():
  for i in range(0, snakeLength):
    getSnakePos(i)
    calculateSnakePos(snakePosItem)
    Screen.setCursorTo(snakePosCalculated[0], snakePosCalculated[1])
    if i == 0:
      Screen.write("+")
    else:
      Screen.write("*")


def drawFruit():
  Screen.setCursorTo(fruitPos[0], fruitPos[1])
  Screen.write("O")


def drawScore():
  # draws the score vertically on the right side of the screen
  for i in range(0, 5):
    Screen.setCursorTo(21, 6 - (i + 1))
    Screen.write(score % (10**(i + 1)) // (10**i))


def drawLoop():
  clearBoard()
  drawSnake()
  drawFruit()
  drawScore()

def showMenu():
  Screen.setCursorTo(1, 1)
  Screen.write("+++++++++++++++++++++")
  Screen.setCursorTo(1, 2)
  Screen.write("+      V-Snake      +")
  Screen.setCursorTo(1, 3)
  Screen.write("+   Snake for Vex   +")
  Screen.setCursorTo(1, 4)
  Screen.write("+   Press [Check]   +")
  Screen.setCursorTo(1, 5)
  Screen.write("+++++++++++++++++++++")

def handleControl(control):
  global snakeDirection
  # 0 = up, 1 = right, 2 = down, 3 = left
  if control == "up":
    if snakeDirection == 0:
      # up to left
      snakeDirection = 3
    elif snakeDirection == 1:
      # right to up
      snakeDirection = 0
    elif snakeDirection == 2:
      # down to left
      snakeDirection = 3
    elif snakeDirection == 3:
      # left to up
      snakeDirection = 0
  elif control == "down":
    if snakeDirection == 0:
      # up to right
      snakeDirection = 1
    elif snakeDirection == 1:
      # right to down
      snakeDirection = 2
    elif snakeDirection == 2:
      # down to right
      snakeDirection = 1
    elif snakeDirection == 3:
      # left to down
      snakeDirection = 2

if __name__ == "__main__":
  snakeDirection = 0
  snakeLength = 3
  snakePos0 = [
      306, 305, 304, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  ]
  snakePos1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  snakePos2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  snakePos3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  snakePos4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  fruitPos = [17, 3]
  score = 0
  snakeDirection = 1 # 0 = up, 1 = right, 2 = down, 3 = left

  showMenu()
  # wait for check button to be pressed when porting to Vex
  input()

  while True:
    score += 1
    snakeLoop()
    drawLoop()
    # print(snakePos0)
    # print(snakePos1)
    # print(snakePos2)
    # print(snakePos3)
    # print(snakePos4)
    # time.sleep(1)
    control = input("")
    if control == "w":
      handleControl("up")
    elif control == "s":
      handleControl("down")

# end block code
