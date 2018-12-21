WIDTH = 1920
HEIGHT = 1080

# COLORS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (52, 255, 38)
BLUE = (0, 0, 255)
TABLE_BLUE = (57, 27, 252)
WHITE = (255, 255, 255)
ORANGE = (255, 157, 66)

PADDLE_W = 30
PADDLE_H = 100
PADDLE_DIST = 30
PADDLE_SPEED = 20

BALL_RADIUS = 15
BALL_SPEEDX = 15
BALL_SPEEDY = 5
BALL_SPEEDY_VAR = 25

P1_COLOR = RED
P2_COLOR = BLACK
BALL_COLOR = ORANGE
BACKGROUND_COLOR = BLUE

class Player:
    def __init__(self, color, x, y, w, h, mode):
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.mode = mode
        self.score = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x,
            self.y, self.w, self.h))

    def getLeft(self):
        return self.x
    def getRight(self):
        return self.x + self.w
    def getUp(self):
        return self.y
    def getDown(self):
        return self.y + self.h

    def getHittingRange(self):
        if self.mode == 'l':
            return range(self.getRight()-BALL_SPEEDX-2, self.getRight())
        if self.mode == 'r':
            return range(self.getLeft(), self.getLeft()+BALL_SPEEDX+2)

    def getVerticalRange(self):
        return range(self.getUp()-3, self.getDown()+4)


class Ball:
    def __init__(self, color, x, y, radius, speedX, speedY):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speedX = speedX
        self.speedY = speedY
        self.lastRight = True

    def draw(self, window):
        pygame.draw.circle(window, self.color,
                (self.x, self.y), self.radius)

    def goToCenter(self):
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)
        if self.lastRight:
            self.speedX = -BALL_SPEEDX
        else:
            self.speedX = BALL_SPEEDX
            
        self.speedY = BALL_SPEEDY
        self.lastRight = not self.lastRight

    def move(self):
        self.x += self.speedX
        self.y += self.speedY

        if self.y > HEIGHT - self.radius or self.y < 0:
            self.speedY *= -1

    def getRight(self):
        return self.x + self.radius
    def getLeft(self):
        return self.x - self.radius
    def getUp(self):
        return self.y + self.radius
    def getDown(self):
        return self.y - self.radius

    def hit(self, player):
            pCenter = (player.getUp()+player.getDown())/2
            offDist = abs(self.y-pCenter)
            offVal = -int((offDist/(player.h/2))*BALL_SPEEDY_VAR)

            self.speedX *= -1
            self.speedY = offVal

def drawScore(p1, p2):
    p1ScoreString = "P1: " + str(p1.score)
    p2ScoreString = "P2: " + str(p2.score)

    font = pygame.font.SysFont("comicsansms", 72)
    p1Text = font.render(p1ScoreString, True, WHITE)
    p2Text = font.render(p2ScoreString, True, WHITE)

    win.blit(p1Text, (100, 100))
    win.blit(p2Text, (WIDTH-300, 100))



import pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FIRST GAME")

p1 = Player(P1_COLOR, PADDLE_DIST, int(HEIGHT/2), PADDLE_W, PADDLE_H, 'l')
p2 = Player(P2_COLOR, WIDTH-PADDLE_DIST-PADDLE_W, int(HEIGHT/2), PADDLE_W, PADDLE_H, 'r')
ball = Ball(BALL_COLOR, int(WIDTH/2), int(HEIGHT/2), BALL_RADIUS, BALL_SPEEDX, BALL_SPEEDY)

run = True
while run:
    pygame.time.delay(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    # p1 UP
    if keys[pygame.K_w]:
        if p1.y >= PADDLE_SPEED:
            p1.y -= PADDLE_SPEED
    # p1 DOWN
    if keys[pygame.K_s]:
        if p1.y <= HEIGHT - p1.h - PADDLE_SPEED:
            p1.y += PADDLE_SPEED
    # p2 UP
    if keys[pygame.K_o]:
        if p2.y >= PADDLE_SPEED:
            p2.y -= PADDLE_SPEED
    # p2 DOWN
    if keys[pygame.K_k]:
        if p2.y <= HEIGHT - p2.h - PADDLE_SPEED:
            p2.y += PADDLE_SPEED

    if keys[pygame.K_r]:
        p1.score = 0
        p2.score = 0

    if keys[pygame.K_q]:
        run = False

    win.fill(BACKGROUND_COLOR)
    if ball.getRight() in p2.getHittingRange() and ball.speedX > 0:
        if ball.y in p2.getVerticalRange():
            ball.hit(p2)
            
    if ball.getLeft() in p1.getHittingRange() and ball.speedX < 0:
        if ball.y in p1.getVerticalRange():
            ball.hit(p1)

    if ball.getRight() >= WIDTH:
        ball.goToCenter()
        p1.score += 1
    if ball.getLeft() <= 0:
        ball.goToCenter()
        p2.score += 1

    p1.draw(win)
    p2.draw(win)
    
    drawScore(p1, p2)

    ball.draw(win)
    ball.move()

    pygame.display.update()

print("QUIT")
pygame.quit()
