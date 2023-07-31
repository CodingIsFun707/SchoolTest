from tkinter import *
import math
import random

class SnakeGame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()

        self.width = 20
        self.height = 20
        self.movement_speed = 150 # Easy mode: 200ms (PB: 34), Medium mode: 150ms (PB: 27), Hard mode: 100ms (PB: 8), Insane mode: 50ms (PB: ?)
        self.colorGrid = ['white' for i in range(self.width * self.height)]
        self.frameGrid = [Frame(width = 20, height = 20) for i in range(self.width * self.height)]
        self.botData = {0:'down', 1:'left', 7:'down', 8:'right', 14:'down', 15:'left', 21:'down', 22:'right', 28:'down', 29:'left', 35:'down', 36:'right', 42:'down', 43:'left', 50:'up', 57:'right'}
        self.colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#9400D3', '#FF00FF']
        self.grays = ['#101010', '#202020', '#404040', '#606060', '#808080', '#A0A0A0', '#C0C0C0', '#E0E0E0', '#F0F0F0']
        self.snakeHead = 190
        self.snakeTail = 0
        self.timer = 0
        self.tick = 0
        self.doLoop = True
        self.snakeDir = 'right'
        self.snakeLength = 30
        self.apple = random.randint(0, (self.width * self.height) -  1)
        self.snakeBody = []
        self.gameOver = []
        self.score = IntVar()
        self.score.set(0)

        self.gameOver.append(Label(self, text = 'GAME OVER!', font = ['Arial', 20, 'bold']))
        self.gameOver.append(Label(self, text = 'Your score was:'))
        self.gameOver.append(Label(self, textvariable = self.score))
        self.gameOver.append(Button(self, text = 'Quit', command = root.destroy))

        root.bind('<Key>', self.key_pressed)

        self.show_all()
        root.after(1000, self.inf_loop)
        self.update_grid()
        
    def show_all(self):
        n = 0
        for i in self.frameGrid:
            i.grid(row = math.floor(n / self.width), column = n % self.width)
            n += 1
    
    def grid_to_xy(self, grid):
        x = grid % self.width
        y = math.floor(grid / self.width)
        return [x, y]
    
    def xy_to_grid(self, x, y):
        return (y * self.grid_width) + x
    
    def switch_to_gameover(self):
        for i in self.frameGrid:
            i.grid_forget()
        
        self.gameOver[0].grid(row = 0, column = 0)
        self.gameOver[1].grid(row = 1, column = 0)
        self.gameOver[2].grid(row = 2, column = 0)
        self.gameOver[3].grid(row = 3, column = 0)
    
    def bot(self):
        apple = self.grid_to_xy(self.apple)
        head = self.grid_to_xy(self.snakeHead)
        diffx = apple[0] - head[0]
        diffy = apple[1] - head[1]
        if diffx != 0:
            if diffx < 0: self.snakeDir = 'left'
            if diffx > 0: self.snakeDir = 'right'
            apple = self.grid_to_xy(self.apple)
            head = self.grid_to_xy(self.snakeHead)
            diffx = apple[0] - head[0]
            diffy = apple[1] - head[1]
        if diffy != 0:
            if diffy < 0: self.snakeDir = 'up'
            if diffy > 0: self.snakeDir = 'down'
            apple = self.grid_to_xy(self.apple)
            head = self.grid_to_xy(self.snakeHead)
            diffx = apple[0] - head[0]
            diffy = apple[1] - head[1]

    def inf_loop(self):
        self.tick += 1
        self.timer += 1
        self.tick = self.tick % 64
        moveOn = False
        if self.apple == self.snakeHead:
            self.snakeLength += 1
            self.score.set(self.score.get() + 1)
            print(self.score.get())
            while not moveOn:
                self.apple = random.randint(0, (self.width * self.height) -  1)
                val = True
                for i in self.snakeBody:
                    if i == self.apple:
                        val == False
                if val: moveOn = True       
        else:
            self.colorGrid[self.apple] = 'red'

        #self.bot()

        for i in self.snakeBody:
            if self.snakeHead == i:
                self.switch_to_gameover()
                self.doLoop = False

        oldPos = self.snakeHead
        if self.snakeDir == 'up':
            self.snakeHead -= self.width
            if self.snakeHead < 0:
                self.switch_to_gameover()
                self.doLoop = False
        if self.snakeDir == 'left':
            if self.snakeHead % self.width == 0:
                self.switch_to_gameover()
                self.doLoop = False
            self.snakeHead -= 1
        if self.snakeDir == 'down':
            self.snakeHead += self.width
            if self.snakeHead > (self.width * self.height) - 1:    
                self.switch_to_gameover()
                self.doLoop = False
        if self.snakeDir == 'right':
            self.snakeHead += 1
            if self.snakeHead % self.width == 0:
                self.switch_to_gameover()
                self.doLoop = False

        self.snakeBody.append(oldPos)
        self.snakeTail = self.snakeBody[0]

        if len(self.snakeBody) >= self.snakeLength:
            self.snakeBody.remove(self.snakeTail)
            self.colorGrid[self.snakeTail] = 'white'
            

        self.colorGrid[self.snakeHead] = '#000000'
        for i in self.snakeBody:
            if self.doLoop:
                self.snakeBody.reverse()
                self.colorGrid[i] = self.grays[(self.snakeBody.index(i) + 1) % 9]
                self.snakeBody.reverse()
        self.update_grid()
        if self.doLoop: root.after(self.movement_speed, self.inf_loop)
    
    def key_pressed(self, data):
        char = data.char
        if char == 'w': self.snakeDir = 'up'
        if char == 'a': self.snakeDir = 'left'
        if char == 's': self.snakeDir = 'down'
        if char == 'd': self.snakeDir = 'right'

    def update_grid(self):
        for i in range(self.width * self.height):
            self.frameGrid[i].configure(bg = self.colorGrid[i])

root = Tk()
root.configure(width = 1000, height = 1000)
s = SnakeGame(root)

root.mainloop()
