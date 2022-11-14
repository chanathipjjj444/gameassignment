import pygame as pg
import random

import pygame.transform

from settings import screen_width, screen_height


class Bullet_generater(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y,spawn):
        super().__init__()
        self.image = pg.image.load("./graphics/non_character/bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.bullet_speed = 3
        self.spawn = spawn



    def update(self):
        #move bullet
        if self.spawn == "L":
            self.rect.x += (self.bullet_speed)
        elif self.spawn == "R":
            self.rect.x -= (self.bullet_speed)

        #check if bullet gone off screen
        if (self.rect.left > (screen_width * 1.3)) and self.spawn == "L":
            self.kill()
        elif (self.rect.right < -100) and self.spawn == "R":
            self.kill()

class Bounce_bullet(pg.sprite.Sprite):
    def __init__(self,posx, posy,spawn):
        super().__init__()
        self.image = pg.image.load("./graphics/non_character/shuriken/1.png")
        self.rect = self.image.get_rect()
        self.rect.center = [posx, posy]
        self.bullet_speed_x = 1.5
        self.bullet_speed_y = 1.5
        self.spawn = spawn


        dir_state = ["t_collide","g_collide"]
        rand_index = random.randrange(len(dir_state))
        rand_dir = dir_state[rand_index]
        self.direction = rand_dir


    def bounce(self):
        if self.rect.x > (0.98)*screen_width:
            self.bullet_speed_x = -self.bullet_speed_x
        if self.rect.x < 0:
            self.bullet_speed_x = -self.bullet_speed_x
        if self.rect.y < 0:
            self.bullet_speed_y = -self.bullet_speed_y
        if self.rect.y > 0.95*(screen_height):
            self.bullet_speed_y = -self.bullet_speed_y

        self.rect.x += self.bullet_speed_x
        self.rect.y += self.bullet_speed_y
        self.laststage = self.spawn



    def update(self):
        self.bounce()
        #move bullet


class GOLD_BULLET(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y,spawn):
        super().__init__()
        self.image = pg.image.load("./graphics/non_character/yellow_bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 31))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.bullet_speed = 3
        self.spawn = spawn

    def update(self):
        #move bullet
        if self.spawn == "L":
            self.rect.x += (self.bullet_speed)
        elif self.spawn == "R":
            self.rect.x -= (self.bullet_speed)

        #check if bullet gone off screen
        if (self.rect.left > (screen_width * 1.3)) and self.spawn == "L":
            self.kill()
        elif (self.rect.right < -100) and self.spawn == "R":
            self.kill()