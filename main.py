import pygame
import random

# game initialization
pygame.init()

# screen
width = 600
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("OOP GAME")

# game settings
fps = 60
clock = pygame.time.Clock()

# image

image_mozkomor = pygame.image.load("img/mozkomor-modry.png")
scaled_image_mozkomor = pygame.transform.scale(image_mozkomor, (32, 32))
image_bullet = pygame.image.load("img/bullet.png")


# class Game
class Game:
    def __init__(self, grp_mozkomors, grp_bullets):
        self.grp_mozkomors = grp_mozkomors
        self.grp_bullets = grp_bullets

    def update(self):
        self.collision_detect()

    def collision_detect(self):
        collided_mozkomor = pygame.sprite.groupcollide(
            self.grp_mozkomors, self.grp_bullets, True, True
        )
        if len(self.grp_mozkomors) < 5:
            end_of_round = True
        # if collided_mozkomor:
        #     collided_mozkomor.remove(self.grp_mozkomors)

    def reset_game(self):
        pass


# class mozkomor
class Mozkomor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = scaled_image_mozkomor
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # # nastavenie nahodneho smeru
        # self.smer_x = random.choice([-1, 1])
        # self.smer_y = random.choice([-1, 1])
        self.speed = 1

    def update(self):
        self.move()

    def move(self):
        # nahodny pohyb
        self.rect.y += self.speed

        # # odraz mozkomora
        # if self.rect.x < 0 or self.rect.x > width - 64:

        # if self.rect.y < 10 or self.rect.y > height - 64:


# class Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img/rocket.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 4

    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = image_bullet
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.bullet_fired = False

    def update(self):
        self.shot()

    def shot(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


# mozkomor group
mozkomor_group = pygame.sprite.Group()
for i in range(10):
    if i < 3:
        one_mozkomor = Mozkomor(random.randint(1, 10) * 50, random.randint(1, 3) * -100)
        mozkomor_group.add(one_mozkomor)
    elif i < 6:
        one_mozkomor = Mozkomor(random.randint(1, 10) * 50, random.randint(1, 3) * -200)
        mozkomor_group.add(one_mozkomor)
    elif i < 8:
        one_mozkomor = Mozkomor(random.randint(1, 10) * 50, random.randint(1, 3) * -400)
        mozkomor_group.add(one_mozkomor)

# player group
player_group = pygame.sprite.Group()
one_player = Player(width // 2, height - 64)
player_group.add(one_player)

# bullet group
bullet_group = pygame.sprite.Group()

# game object
game = Game(mozkomor_group, bullet_group)

# main LOOP

paused = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(
                    one_player.rect.midtop[0] - 5, one_player.rect.midtop[1]
                )
                bullet_group.add(bullet)
            if event.key == pygame.K_p:
                paused = not paused

    # screen fill
    screen.fill((8, 8, 8))

    if not paused or not end_of_round:
        # mozkomor draw
        mozkomor_group.update()
        mozkomor_group.draw(screen)

        # player draw
        player_group.update()
        player_group.draw(screen)

        # bullet draw
        bullet_group.update()
        bullet_group.draw(screen)

        # game update
        game.update()

    if paused:
        font = pygame.font.Font(None, 74)
        text = font.render("Paused!", True, (255, 155, 155))
        screen.blit(
            text,
            (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2),
        )

    # update
    pygame.display.update()

    # slow down loop
    clock.tick(fps)

# game quit
pygame.quit()
