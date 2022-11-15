import pygame as pg
from support import import_folder

class Particleffect(pg.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5

        if type == "jump":#ปัญหาคือการ import ซ้้ำ
            self.frames = import_folder("Infographics/character/dust_particles/jump/")

        if type == "land":
            self.frames = import_folder("Infographics/character/dust_particles/land/")
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill() #destroy the sprite after jumping animation is ran
        else:
            self.image = self.frames[int(self.frame_index)]


    def update(self,x_shift): #to make dust particle move when the screen move
        self.animate()
        self.rect.x += x_shift