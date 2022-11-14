import random
from pygame import mixer
from enemy import Bullet_generater,Bounce_bullet,GOLD_BULLET
import pygame as pg
from settings import tile_size, screen_width, screen_height
from player import Player
from particle import Particleffect
from tile import Tile

SCREEN = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("gameover")
GAMEOVER = pg.image.load("graphics/non_character/gameover.jpg")
screen = pg.display.set_mode((screen_width, screen_height))


class Level:
    def __init__(self, level_data, surface):
        #level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        self.start_ticks = pg.time.get_ticks()
        self.goldstart_ticks = pg.time.get_ticks()
        self.name = ""
        self.extrascore = 0
        #score



        self.text_x = screen_width/1.15
        self.text_y =10

        #dust
        self.dust_sprite = pg.sprite.GroupSingle() #we onlyhave 1 animation of a dust particle
        self.player_on_ground =False

    def show_score(self,x ,y):
        pg.init()
        self.score = int(pg.time.get_ticks()/100) + self.extrascore
        self.font = pg.font.SysFont("8-bit Madness",32)
        score = self.font.render("Score: " + str(self.score),True, (255,255,255))
        self.display_surface.blit(score, (x,y))


    def create_jump_particle(self, pos):
        if self.player.sprite.facing_right:
            pos -= pg.math.Vector2(10,5)
        else:
            pos += pg.math.Vector2(10,5)
        jump_particle_sprite = Particleffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_onground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
            self.player.jump2 = False
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites(): #means that there is no sprite in the group single
            if self.player.sprite.facing_right:
                offset = pg.math.Vector2(10,15)
            else:
                offset = pg.math.Vector2(-10,15)
            fall_dust_particle = Particleffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        # self.enemies = pg.sprite.Group()
        self.tiles = pg.sprite.Group()        ###______
        self.player = pg.sprite.GroupSingle() #if its a dynamic object its must always add to a sprite Group
        self.bullet = pg.sprite.Group()
        self.bounce_bullet = pg.sprite.Group()
        self.gold_bullet = pg.sprite.Group()


        for row_index,row in enumerate(layout):
            for col_index,cell in enumerate(row):
                x = col_index * tile_size
                player_x = col_index
                player_y = row_index
                y = row_index * tile_size

                if cell == "x":
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile)

                if cell == "p":
                    self.player_sprite = Player((player_x,player_y), self.display_surface, self.create_jump_particle)
                    self.player.add(self.player_sprite)

                if cell == "o":
                    #to make a speed adjusatable
                    try:
                        self.hardcheck = (pg.time.get_ticks() - self.start_ticks)
                    except:
                        self.hardcheck = 1
                        print("lol")

                    for bullet in range(self.hardcheck):
                        new_bullet = Bullet_generater(random.randrange(-2000,0),(random.randrange(0,screen_height)), "L")
                        self.bullet.add(new_bullet)

                    for bullet in range(int(self.hardcheck)):
                        new_bullet = Bullet_generater(random.randrange(800,2000),(random.randrange(0,screen_height)), "R")
                        self.bullet.add(new_bullet)

                    for bullet in range(5):
                        new_bullet = GOLD_BULLET(random.randrange(-2000,0),(random.randrange(0,screen_height)), "L")
                        self.gold_bullet.add(new_bullet)

                    for bullet in range(5):
                        new_bullet = Bullet_generater(random.randrange(800,2000),(random.randrange(0,screen_height)), "R")
                        self.gold_bullet.add(new_bullet)

                    for bullet in range(2):
                        new_bullet = Bounce_bullet(random.randrange(1000,screen_width), (random.randrange(0,screen_height)), "R")
                        self.bounce_bullet.add(new_bullet)

                    for bullet in range(2):
                        new_bullet = Bounce_bullet(random.randrange(0,0.2*(screen_width)),(random.randrange(0,screen_height)), "L")
                        self.bounce_bullet.add(new_bullet)


    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x


        if player_x < (screen_width * 0.2) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
            bullet_speed = 4
            bounce_speed = 2.5
            for sprite in self.bullet:
                sprite.rect.x += bullet_speed
            for sprite in self.bounce_bullet:
                sprite.rect.x += bounce_speed

        elif player_x > (screen_width * 0.8) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
            bullet_speed = -4
            bounce_speed = -2.5
            for sprite in self.bullet:
                sprite.rect.x += bullet_speed
            for sprite in self.bounce_bullet:
                sprite.rect.x += bounce_speed

        else:
            self.world_shift = 0
            player.speed = 8
            self.seconds = (pg.time.get_ticks()-self.start_ticks)/1000
            self.goldseconds = (pg.time.get_ticks() - self.goldstart_ticks) / 1000
            if self.seconds > 5:
                self.start_ticks = pg.time.get_ticks()
                for bullet in range(5):
                    new_bullet = Bullet_generater(random.randrange(-2000, 0), (random.randrange(0, screen_height)), "L")
                    self.bullet.add(new_bullet)

                for bullet in range(5):
                    new_bullet = Bullet_generater(random.randrange(800, 2000), (random.randrange(0, screen_height)),"R")
                    self.bullet.add(new_bullet)

            if self.goldseconds > 10:
                self.goldstart_ticks = pg.time.get_ticks()
                for bullet in range(2):
                    new_bullet = GOLD_BULLET(random.randrange(-2000, 0), (random.randrange(0, screen_height)), "L")
                    self.gold_bullet.add(new_bullet)

                for bullet in range(2):
                    new_bullet = GOLD_BULLET(random.randrange(800, 2000), (random.randrange(0, screen_height)),"R")
                    self.gold_bullet.add(new_bullet)


    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed #direction อยู่ใน file player

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):

                if player.direction.x < 0 : #means that player is moving to the left
                    player.rect.left = sprite.rect.right #------
                    player.on_left = True
                    self.current_x = player.rect.left

                elif player.direction.x > 0:#------ means that playerrect cannot move throgh the ob stacle
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0) :
            player.on_left = False

        if player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0) :
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():

            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0.8: #means that player is moving downward
                    player.rect.bottom = sprite.rect.top  #------
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0.8 :#------ means that playerrect cannot move throgh the ob stacle
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: # check if player is jumping or floating
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        #dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.die()
        #level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        #player
        self.player.update()
        self.get_player_onground() # check if the player is on the ground
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)

        #bullet
        self.bullet.draw(self.display_surface)
        self.bullet.update()
        self.bounce_bullet.draw(self.display_surface)
        self.bounce_bullet.update()
        self.gold_bullet.draw(self.display_surface)
        self.gold_bullet.update()

        #bullet and player collide to subtract the health bar
        self.check_collide()


        #score
        self.show_score(self.text_x,self.text_y)

    def check_collide(self):
        #check_collide_laser
        if pg.sprite.spritecollide(self.player.sprite,self.bullet, True):
            player_damaged = mixer.Sound("graphics/non_character/sound/player_hit.wav")
            player_damaged.play()
            self.player_sprite.current_health -= 5
        #check_collide_shuriken
        if pg.sprite.spritecollide(self.player_sprite, self.bounce_bullet, False):
            player_damaged = mixer.Sound("graphics/non_character/sound/player_hit.wav")
            player_damaged.play()
            self.player_sprite.current_health -= 1

        if pg.sprite.spritecollide(self.player_sprite,self.gold_bullet,True):
            coin_sound = mixer.Sound("graphics/non_character/sound/coin_sound.wav")
            coin_sound.play()
            self.extrascore += 100
            self.tf = False

        if self.player_sprite.current_health < 0:
            self.highscore_W()
        #     SCREEN.blit(GAMEOVER,(350,100))
        #     pg.display.update()
        #     pg.time.wait(3000)
        #     pg.quit()





    def die(self):
        if self.player.sprite.rect.bottom > 750:
            self.player.sprite.rect.bottom = 0

    def highscore_W(self):
        score_to_record = self.score
        with open("leaderboard.txt","a") as file:
            file.write(str(score_to_record) + " :" + self.name + "\n")