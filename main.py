import pygame
import sys
import random

pygame.init()

class Bird:

    def __init__(self):
        self.img = pygame.image.load('bird.png')
        self.img.convert()

        self.rect = self.img.get_rect()
        self.rect.center = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        self.velocity = 0
        self.acceleration = 0.5
        self.jump_power = -12

        self.rotation = 0
        self.rotation_speed = 5
        self.rotation_max = -25

    def update(self):
        rotated_image = pygame.transform.rotate(self.img, -self.rotation)
        new_rect = rotated_image.get_rect(center=self.rect.center)

        screen.blit(rotated_image, new_rect.topleft)

        if self.rotation < 0:
            self.rotation += 1
        elif self.rotation > 0 and self.rotation <= self.rotation_max:
            self.rotation = 1

        self.velocity += self.acceleration
        self.rect.y += self.velocity

        if self.rect.bottom > SCREEN_HEIGHT:
            print("Quitting Game...")
            pygame.quit()
            sys.exit()
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
            self.rotation = 0

    def jump(self):
        self.velocity = self.jump_power
        self.rotation = self.rotation_max

class Pipe:

    def __init__(self):
        offset = random.randint(400, 800)
        self.pipeAnchor = [SCREEN_WIDTH, offset]

        self.bottom = pygame.image.load('bottom_pipe.png')
        self.bottom.convert()

        self.bottom_rect = self.bottom.get_rect()
        self.bottom_rect.center = self.pipeAnchor[0] + 100, self.pipeAnchor[1] + 150
        self.bottom_rect[1] += 25

        self.top = pygame.image.load('top_pipe.png')
        self.top.convert()

        self.top_rect = self.top.get_rect()
        self.top_rect.center = self.pipeAnchor[0] + 100, self.pipeAnchor[1] - 650
        self.top_rect[1] -= 25

    def update(self):
        screen.blit(self.bottom, self.bottom_rect)
        screen.blit(self.top, self.top_rect)

        self.bottom_rect.x -= 5
        self.top_rect.x -= 5

    def spawn_pipes(self):
        pipes.append(Pipe())

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
CLOCK = pygame.time.Clock()
FPS = 60

WHITE = (0, 200, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird - A Remake")

score = 0

spawnPipe = pygame.USEREVENT
timer = pygame.time.set_timer(spawnPipe, 2000)

remove_pipes = []

bird = Bird()
pipes = [Pipe()]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Quitting Game...")
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird.jump()
        elif event.type == spawnPipe:
            Pipe().spawn_pipes()

    screen.fill(WHITE)

    for pipe in pipes:
        pipe.update()

        if pipe.bottom_rect[0] < -150 and pipe.top_rect[0] < -150:
            remove_pipes.append(pipe)
        
        if pygame.Rect.colliderect(bird.rect, pipe.bottom_rect) or pygame.Rect.colliderect(bird.rect, pipe.top_rect):
            print("Quitting Game...")
            pygame.quit()
            sys.exit()

    for pipe in remove_pipes:
        pipes.remove(pipe)

    remove_pipes = []

    bird.update()

    pygame.display.update()

    CLOCK.tick(FPS)