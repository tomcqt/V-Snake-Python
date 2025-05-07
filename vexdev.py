import numpy, os, time


class Vex:

  def __init__(self):
    self.name = "VexDev"
    self.version = "1.0.0"
    self.description = "A Python library for testing Vex code by writing not Vex code. Very useful! (not really)"

  class Screen:

    def __init__(self, width, height, clear=True):
      self.width = width
      self.height = height
      self.clear = clear
      self.cursorX = 0
      self.cursorY = 0
      self.buffer = numpy.zeros((self.height, self.width), dtype=str)
      self.buffer.fill(" ")

    def setCursorTo(self, x, y):
      self.cursorX = x - 1
      self.cursorY = y - 1

    def write(self, text):
      if type(text) != str:
        text = str(text)
      for char in text:
        self.buffer[self.cursorY, self.cursorX] = char
        self.cursorX += 1
        if self.cursorX >= self.width:
          self.cursorX = 0
          self.cursorY += 1
          if self.cursorY >= self.height:
            self.cursorY = 0
      self.render()

    def render(self):
      if self.clear:
        if os.name == "nt":
          os.system("cls")
        else:
          os.system("clear")

      print("┌" + "─" * (self.width) + "┐")
      for row in self.buffer:
        print("│" + "".join(row) + "│")
      print("└" + "─" * (self.width) + "┘")
      # time.sleep(0.5)
