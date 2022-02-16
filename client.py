import pygame
import random
import math

aspect = (800, 600)
player_size = (100, 50)
ball_size = (25,25)
barrier_size = (50,25)
color_gradient = [(150, 0, 0), (150, 100, 0), (0, 150, 0), (0, 50, 150), (75, 0, 75)]

def init_barriers(size):
    barriers = []
    barrier_count = (aspect[0]//size[0])-1
    gap = aspect[0]-(barrier_count*size[0])
    gap_fr = gap/(barrier_count + 1)
    for h in range(5):
        for i in range(barrier_count):
            barrier = Barrier(i*barrier_size[0]+(i+1)*gap_fr,100+h*30, barrier_size[0], barrier_size[1], color_gradient[h])
            barriers.append(barrier)

    return barriers

win = pygame.display.set_mode(aspect)
pygame.display.set_caption("Test")

class Barrier():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
    def draw(self, win):
        pygame.draw.rect(win,self.color, self.rect)

class Ball():
    def __init__(self, x, y, side, color):
        self.x = x
        self.y = y
        self.width = side
        self.height = side
        self.color = color
        self.rect = (x,y,side,side)
        self.dir = math.pi*(random.random()-0.5)
        self.vel = 3
    def draw(self, win):
        pygame.draw.rect(win,self.color, self.rect)
    def bounce(self, edge_dir):
        #self.dir = math.acos(-math.cos(dir-edge_dir)) + math.asin(-math.sin(dir-edge_dir))
        self.dir -= math.pi/2
    def move(self):
        x_diff = self.vel*math.cos(self.dir)
        y_diff = self.vel*math.sin(self.dir)
        if self.x + x_diff < 0:
            self.x = 0
            self.bounce(0)
        elif self.x + x_diff > aspect[0]-ball_size[0]:
            self.x = aspect[0]-ball_size[0]
            self.bounce(0)
        else:
            self.x += self.vel*math.cos(self.dir)
        
        if self.y + y_diff < 0:
            self.y = 0
            self.bounce(math.pi/2)
        elif self.y + y_diff > aspect[1]-ball_size[1]:
            self.y = aspect[1]-ball_size[1]
            self.bounce(math.pi/2)
        else:
            self.y += self.vel*math.sin(self.dir)
        
        self.rect = (self.x, self.y, self.width, self.height)


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 4

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            if self.x - self.vel >= 0:
                self.x -= self.vel
            else:
                self.x = 0
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            if self.x + self.vel <= aspect[0]-player_size[0]:
                self.x += self.vel
            else:
                self.x = aspect[0]-player_size[0]

        self.rect = (self.x, self.y, self.width, self.height)


def redrawWindow(win, player, barriers, ball):
    win.fill((0,0,0))
    player.draw(win)
    ball.draw(win)
    for b in barriers:
        b.draw(win)
    pygame.display.update()

def main():
    run = True
    p = Player(aspect[0]/2-(player_size[0]/2),aspect[1]-(player_size[1]/2),player_size[0],player_size[1],(200,200,200))
    barriers = init_barriers(barrier_size)
    ball = Ball(aspect[0]/2,aspect[1]/2,25,(200,200,200))

    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        p.move()
        ball.move()
        redrawWindow(win, p, barriers, ball)



main()