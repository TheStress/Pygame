import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Sprites/car_red_1.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Block(pygame.sprite.Sprite):
    def __init__(self):
        super(Block, self).__init__()
        self.surf = pygame.image.load("Sprites/barrier_red.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center= (
            random.randint(SCREEN_WIDTH-50, SCREEN_WIDTH-40),
            random.randint(0, SCREEN_HEIGHT)
        ))
        self.speed = 3

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


player = Player()

blocks = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
allSprites.add(player)

clock = pygame.time.Clock()

ADD_BLOCK = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_BLOCK, 1500)

running = True
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == ADD_BLOCK:
            newBlock = Block()
            blocks.add(newBlock)
            allSprites.add(newBlock)


    screen.fill((255, 255, 255))

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    blocks.update()

    if pygame.sprite.spritecollideany(player, blocks):
        player.kill()
        running = False

    for entity in allSprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()