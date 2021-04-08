import random
import numpy as np
import pygame

class Simulation:
    def __init__(self):
        self.dim = self.width, self.height = 720, 420
        self.init_x, self.init_y = round(self.width/2), round(self.height/2)
        self.x, self.y = self.init_x-10, self.init_y

        self.min_x, self.min_y = self.x, self.y
        self.max_x, self.max_y = self.x, self.y
        self.domain = 10
        self.domain_min_x = self.init_x - self.domain
        self.domain_max_x = self.init_x + self.domain
        self.domain_min_y = self.init_y - self.domain
        self.domain_max_y = self.init_y + self.domain

        self.screen = None
        self.update = False
        self.crystalColor = pygame.Color("#808080")
        self.colorful = False


    def init(self):
        pygame.init()
        pygame.display.set_caption("Crystal-Simulation")
        self.screen = pygame.display.set_mode(self.dim)
        self.isRunning = True

        self.screen.set_at((self.init_x, self.init_y + 10), self.crystalColor) #seedpoint
        pygame.display.update()

    def event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def loop(self):
        n_dir = random.choice(((0,1), (0,-1), (1,0), (-1,0), (1,-1), (-1,1), (1,1), (-1,-1))) #get new random direction

        n_x = self.x + n_dir[0] #new x-pos
        n_y = self.y + n_dir[1] #new y-pos

        #check that it fits the screen
        if (n_x < self.domain_min_x):
            n_x = self.domain_max_x

        if (n_x > self.domain_max_x):
            n_x = self.domain_min_x

        if (n_y < self.domain_min_y):
            n_y = self.domain_max_y

        if (n_y > self.domain_max_y):
            n_y = self.domain_min_y

        if (self.screen.get_at((n_x, n_y)) == self.crystalColor):  #checks if pixel is already set --> if crystal is already there
            self.update = True

            #grow domain
            if(self.x < self.min_x):
                self.min_x = self.x

            if(self.x > self.max_x):
                self.max_x = self.x

            if(self.y < self.min_y):
                self.min_y = self.y

            if(self.y > self.max_y):
                self.max_y = self.y

            #modify domain
            self.domain_min_x = max([self.min_x - self.domain , 1]) #pick between self.min_x - self.pad_size and 1
            self.domain_max_x = min([self.max_x + self.domain , self.width -1]) #pick between self.max_x + self.pad_size and self.width -1
            self.domain_min_y = max([self.min_y - self.domain , 1]) #pick between self.min_y - self.pad_size and 1
            self.domain_max_y = min([self.max_y + self.domain , self.height -1]) #pick between self.max_y + self.pad_size and self.height -1

        else: #if theres is not alreay a crystal
            #print(n_x, n_y)
            self.update = False
            self.x, self.y = n_x, n_y #update to the new position


    def draw(self):
        if self.update:
            if self.colorful:
                rgbl=[255,0,0]
                random.shuffle(rgbl)
                color = tuple(rgbl)
                self.crystalColor = color
            self.screen.set_at((self.x, self.y), self.crystalColor)
            pygame.display.update()

            self.update = False

            #select one of the domains sides as starting point
            n_side = random.choice((1,2,3,4))

            if(n_side == 1):
                self.x = self.domain_min_x
                self.y = int(random.uniform(self.domain_min_y, self.domain_max_y))
            elif(n_side == 2):
                self.x = int(random.uniform(self.domain_min_x, self.domain_max_x))
                self.y = self.domain_min_y
            elif(n_side == 3):
                self.x = self.domain_max_x
                self.y = int(random.uniform(self.domain_min_y, self.domain_max_y))
            elif(n_side == 4):
                self.x = int(random.uniform(self.domain_min_x, self.domain_max_y))
                self.y = self.domain_max_y

    def execute(self):
        if self.init() == False:
            self.isRunning = False

        while self.isRunning:
            for event in pygame.event.get():
                self.event(event)

            self.loop()
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    p = Simulation()
    p.execute()
