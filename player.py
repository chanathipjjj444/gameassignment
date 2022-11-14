import pygame as pg
from support import import_folder
from pygame import mixer
Slashstate = False


class Player(pg.sprite.Sprite):
    def __init__(self, pos,surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame_index]
        #get rid of self.image.fill to make our character visible not filled in red.
        self.rect = self.image.get_rect(topleft = pos)
        #particle movement
        self.import_dust_run_particle()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles

        #player health
        self.current_health = 200
        self.maximum_health = 1000
        self.health_bar_lenght = 200
        self.health_ratio = self.maximum_health / self.health_bar_lenght



        #player_movement
        self.direction = pg.math.Vector2(0,0) #Vector = master of movement
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        self.jump2 = False

        #player status
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        #slash_control
        self.time_slash = 0
        self.slash_count = 1
        self.another_slash = False


    def import_character_assets(self):
        character_path = "graphics/character/"
        self.animations = {"idle": [], "run":[], "jump":[], "fall":[], "slash":[] }

        for animation in self.animations.keys(): #try to get acces to all the animation file key
            full_path = character_path+ animation + "/"
            self.animations[animation] = import_folder(full_path) #function from supprt.py


    def jump(self):
        Jump_sound = mixer.Sound("graphics/non_character/sound/jump_sound.ogg")
        Jump_sound.play()
        self.direction.y = self.jump_speed
        self.jump_time = pg.time.get_ticks()
        self.jump2 = True

    def draw_health(self):
        pg.draw.rect(self.display_surface, (255,0,0),(10,10,self.current_health,10))
        pg.draw.rect(self.display_surface,(255,255,255),(10,10,self.health_bar_lenght,10),2)


    def double_jump(self):
        now = pg.time.get_ticks()
        keys = pg.key.get_pressed()
        if  now - self.jump_time > 300 and keys[pg.K_j]:
            Jump_sound = mixer.Sound("graphics/non_character/sound/jump_sound.ogg")
            Jump_sound.play()
            self.direction.y = 0
            self.direction.y += self.jump_speed
            self.jump2 = False

    def slash(self):
        keys = pg.key.get_pressed()
        ## อาจจะต้องทำ state ในการชนกระสุนทอง



    def animate(self):# to play the different frame of the gesture of our mc
        animation = self.animations[self.status]
        #loop over frame index
        if self.status == "slash":
            self.animation_speed = 0.01

        else:
            self.animation_speed = 0.15

        # if self.status == "slash" and self.time_slash - pg.time.get_ticks() < 100 :
        #     self.another_slash = True

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0 #set if the frame index is > animation surface list we will set it to 0.

        image = animation[int(self.frame_index)] #set a local variable to flip it when mc look at the left

        if self.facing_right:
            self.image = image
        else:
            flipped_image = pg.transform.flip(image,True,False) # True false means that we flip x axis
            self.image = flipped_image

        ### set the rectangle
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == "run" and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0

            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pg.math.Vector2(6,10)   #in the first place dust particle is being drawn far to low so we subtract axis with vector
                self.display_surface.blit(dust_particle, pos) #display the dust particle
            else:
                flipped_dust_particle = pg.transform.flip(dust_particle, True, False)
                pos = self.rect.bottomright - pg.math.Vector2(6, 10)
                self.display_surface.blit(flipped_dust_particle, pos)


    def get_input(self):

        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            self.direction.x = 1 #self.direction มันคือ vector ก็ไอ้ s.dr.y ก็คือเราไปบวกค่าที่เเกน y ของ vector นั่นเอง
            self.facing_right = True
            if keys[pg.K_j] and self.on_ground:
                self.create_jump_particles(self.rect.midbottom)
                self.jump()
            if self.jump2:
                self.double_jump()
        elif keys[pg.K_a]:
            self.direction.x = -1
            self.facing_right = False
            if keys[pg.K_j] and self.on_ground:
                self.create_jump_particles(self.rect.midbottom)
                self.jump()
            if self.jump2:
                self.double_jump()

        elif self.direction.y > 0 and self.direction.y < 1 and keys[pg.K_j]:
            self.jump2 = True

        elif keys[pg.K_x]:
            pg.quit()

        else:
            if keys[pg.K_j] and self.on_ground:
                self.create_jump_particles(self.rect.midbottom)
                self.jump()
            self.direction.x = 0
        if keys[pg.K_l]:
            self.gravity = 2.5
        else:
            self.gravity = 0.8


    def import_dust_run_particle(self):
        self.dust_run_particles = import_folder("graphics/character/dust_particles/run/") #import dust particle


    def get_state(self): #check the self.direction(vector) to get the state of the player
        key = pg.key.get_pressed()

        if key[pg.K_k]:
                self.status = "slash"
                slash = mixer.Sound("graphics/non_character/sound/slash_sound.wav")
                slash.play()
                self.time_slash = pg.time.get_ticks()

        elif self.direction.y < 0:

            if (self.time_slash - pg.time.get_ticks() < 200) and self.another_slash:
                pass
            else:
                self.status = "jump"
                self.another_slash = False



        elif self.direction.y > 1: # > 1 because if the player is on the floor gravity will apply 0.8 automatically which will make mc animation really weird
            if (self.time_slash - pg.time.get_ticks() < 200) and self.another_slash:
                pass
            else:
                self.status = "fall"
                self.another_slash = False

        elif self.direction.x != 0 :
            if (self.time_slash - pg.time.get_ticks() < 200) and self.another_slash:
                pass
            else:
                self.status = "run"
                self.another_slash = False
        else:
            if (self.time_slash - pg.time.get_ticks() < 200) and self.another_slash:
                pass
            else:
                self.status = "idle"
                self.another_slash = False

            if self.time_slash - pg.time.get_ticks() > 1000:
                self.another_slash = True
        if(self.status == "slash"):
            return True


    def apply_gravity(self):
        if(self.direction.y < 30):
            self.direction.y += self.gravity #ที่ค่าบวกเป็นตกลงเพราะว่าค่าเเกน x,y ของคอมมันไม่เหมือนกับในเลข
        self.rect.y += self.direction.y

    def update(self):
        self.get_input()
        self.get_state()
        self.animate()
        self.run_dust_animation()
        self.draw_health()