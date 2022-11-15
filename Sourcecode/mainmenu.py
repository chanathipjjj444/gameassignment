import pygame, sys
from Button import Button
import pygame as pg
from settings import *
from natsort import natsorted
from level import Level
from os import path
from pygame import mixer

pygame.init()

SCREEN = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Infographics/non_character/new_bg.jpg")


screen_width = 1200
screen_height = 700
frame = 60
screen = pg.display.set_mode((screen_width, screen_height))
clock = pg.time.Clock()
level = Level(level_map, screen)
now = pg.time.get_ticks()
PLAYER_NAME = ""


def load_data():
    dir = path.dirname(__file__)
    with open(path.join(dir, highscore_file), 'w') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0

def gethighscore():
    with open("leaderboard.txt", "r") as file:
        readthefile = file.readlines()
        sortedData = natsorted(readthefile, reverse=True)
        for num in range(len(sortedData)):
           sortedData[num]  = sortedData[num].strip()
    return sortedData

def draw_text(self, text, size, color, x, y):
    font = get_font(size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    self.screen.blit(text_surface, text_rect)

def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Infographics/non_character/njnaruto.ttf", size)

def play():
    mixer.music.load("Infographics/non_character/sound/ingame_bg.mp3")
    mixer.music.play(-1)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.fill("black")
        # command to update entire game
        if level.player_sprite.current_health < 0:

            loser_screen()


        level.run()
        pg.display.update()
        clock.tick(frame)



def main_menu():
    user_text = ""
    base_font = pg.font.Font('Infographics/non_character/njnaruto.ttf',25)
    input_rect = pg.Rect(590,145,300,32)
    color_passive = pg.Color('lightskyblue3')
    color_active = pg.Color('pink')
    mixer.music.load("Infographics/non_character/sound/mainmenu_bg.mp3")
    mixer.music.play(-1)
    color = color_passive

    active = False
    can_play = False

    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()


        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 100))

        ENTERNAME = get_font(25).render("Enter your name:", True, "White")

        PLAY_BUTTON = Button(image=pygame.image.load("Infographics/non_character/Play Rect.png"), pos=(600, 250),
                             text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Infographics/non_character/Options Rect.png"), pos=(600, 400),
                                text_input="HighScore", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Infographics/non_character/Quit Rect.png"), pos=(600, 550),
                             text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        SCREEN.blit(ENTERNAME,(350,150))

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pg.KEYDOWN:
                if active == True:
                    if event.key == pg.K_BACKSPACE:
                        user_text = user_text[:-1]
                    elif event.key == pg.K_RETURN:
                        entersound = mixer.Sound("Infographics/non_character/sound/enter_sound.wav")
                        entersound.play()
                        level.name = user_text
                        can_play = True
                        user_text = ""
                    else:
                        user_text  += event.unicode
                        if text_surface.get_width() > input_rect.w - 10:
                            user_text = user_text[:-1]
                        if(event.key != pg.K_LSHIFT):
                            keyboard_sound = mixer.Sound("Infographics/non_character/sound/keyboard_input_sound.wav")
                            keyboard_sound.play()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS) and can_play:
                    selected_sound = mixer.Sound("Infographics/non_character/sound/menu_selected.wav")
                    selected_sound.play()
                    play()

                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_sound = mixer.Sound("Infographics/non_character/sound/menu_selected.wav")
                    selected_sound.play()
                    high_score()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    selected_sound = mixer.Sound("Infographics/non_character/sound/menu_selected.wav")
                    selected_sound.play()
                    pygame.quit()
                    sys.exit()

        if active:
            color = color_active
        else:
            color = color_passive

        pg.draw.rect(SCREEN,color,input_rect,2)
        text_surface = base_font.render(user_text,True,(255,255,255))
        screen.blit(text_surface,(input_rect.x + 5, input_rect.y + 2))

        #input_rect.w = max(100,text_surface.get_width() + 10)
        pygame.display.update()

def high_score():
    highscore = gethighscore()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        HIGH_SCORE = pygame.image.load("Infographics/non_character/highscore.png")
        SCREEN.blit(HIGH_SCORE, (0, 0))
        HIGHSCORE_TEXT = get_font(80).render("Top 5 Score!!", True, "Green")
        HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(600, 50))
        SCREEN.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)
        try:
            SCORE1 = get_font(35).render(highscore[0], True, "#C9B037")
            SCORE_RECT1 = HIGHSCORE_TEXT.get_rect(center=(750, 200))
            SCORE2 = get_font(35).render(highscore[1], True, "#B4B4B4")
            SCORE_RECT2 = HIGHSCORE_TEXT.get_rect(center=(750, 260))
            SCORE3 = get_font(35).render(highscore[2], True, "#6A3805")
            SCORE_RECT3 = HIGHSCORE_TEXT.get_rect(center=(750, 320))
            SCORE4 = get_font(35).render(highscore[3], True, "#50577A")
            SCORE_RECT4 = HIGHSCORE_TEXT.get_rect(center=(750, 380))
            SCORE5 = get_font(35).render(highscore[4], True, "#50577A")
            SCORE_RECT5 = HIGHSCORE_TEXT.get_rect(center=(750, 440))


            SCREEN.blit(SCORE2, SCORE_RECT2)
            SCREEN.blit(SCORE1,SCORE_RECT1)
            SCREEN.blit(SCORE3, SCORE_RECT3)
            SCREEN.blit(SCORE4, SCORE_RECT4)
            SCREEN.blit(SCORE5, SCORE_RECT5)
        except:
            pass

        OPTIONS_BACK = Button(image=None, pos=(580, 600),
                              text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    selected_sound = mixer.Sound("Infographics/non_character/sound/menu_selected.wav")
                    selected_sound.play()
                    main_menu()
        pygame.display.update()

def loser_screen():
    count_down = pg.time.get_ticks()
    while True:

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        HIGH_SCORE = pygame.image.load("Infographics/non_character/loser_wallpaper.jpg")
        SCREEN.blit(HIGH_SCORE, (0, 0))
        HIGHSCORE_TEXT = get_font(80).render("You just lost the way of a Ninja!", True, "Red")
        HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(600, 50))
        HIGHSCORE_TEXT2 = get_font(80).render(":You Lost?!@", True, "Red")
        HIGHSCORE_RECT2 = HIGHSCORE_TEXT2.get_rect(center=(870, 150))
        SCREEN.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)
        SCREEN.blit(HIGHSCORE_TEXT2, HIGHSCORE_RECT2)
        memes = pygame.image.load("Infographics/non_character/memes.jpg")
        SCREEN.blit(memes,(500,200))
        if pg.time.get_ticks() - count_down > 3000:
            high_score()
        # OPTIONS_BACK = Button(image=None, pos=(580, 600),
        #                       text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")
        #
        # OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        # OPTIONS_BACK.update(SCREEN)
        #
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
        #             selected_sound = mixer.Sound("Infographics/non_character/sound/menu_selected.wav")
        #             selected_sound.play()
        #             main_menu()
        pygame.display.update()




main_menu()