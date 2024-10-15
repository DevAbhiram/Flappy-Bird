import random
import sys
import pygame
from pygame.locals import *


FPS = 32
SCREEN_WIDTH=289
SCREEN_HEIGHT=511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
ICON = pygame.image.load('ATTACHMENTS/IMAGES/favicon.png')
pygame.display.set_icon(ICON)
GROUND_Y= SCREEN_HEIGHT*0.8
GAME_IMAGES={}
GAME_SOUNDS={}
PLAYER='ATTACHMENTS/IMAGES/bird.png'
BACKGROUND='ATTACHMENTS/IMAGES/background.png'
PIPE='ATTACHMENTS/IMAGES/pipe.png'

def WelcomeScreen():
    
    playerx=int(SCREEN_WIDTH/5)
    playery=int((SCREEN_HEIGHT-GAME_IMAGES['player'].get_height())/2)
    messagex=int((SCREEN_WIDTH-GAME_IMAGES['DISPLAY'].get_width())/2)
    messagey=int(SCREEN_HEIGHT*0.13)
    basex=0
    for action in pygame.event.get():
        if action.type == QUIT or (action.type == KEYDOWN and  action.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif action.type == KEYDOWN and (action.key==K_SPACE or action.key == K_UP):
            return
        else:
            SCREEN.blit(GAME_IMAGES['background'], (0,0))
            SCREEN.blit(GAME_IMAGES['player'], (playerx,playery))
            SCREEN.blit(GAME_IMAGES['DISPLAY'], (messagex,messagey))
            SCREEN.blit(GAME_IMAGES['BASE'], (basex,GROUND_Y))
            pygame.display.update()
            FPS_CLOCK.tick(FPS)
def MainGame():
    score = 0
    playerx = (SCREEN_WIDTH/5)
    playery = (SCREEN_HEIGHT/2)
    basex = 0

    #Pipes
    new_Pipe1=getRandomPipe()
    new_Pipe2=getRandomPipe()
def getRandomPipe():
    pipe_Height = GAME_IMAGES['PIPES'][0].get_height()
    offset = SCREEN_HEIGHT/3
    bottomPipe=offset + random.randrange(0,int(SCREEN_HEIGHT-GAME_IMAGES['BASE'].get_height()-1.2*offset))
    pipe_X = SCREEN_WIDTH + 10
    topPipe=pipe_Height-bottomPipe+offset

    pass
if __name__=="__main__":
    pygame.init()
    FPS_CLOCK=pygame.time.Clock()
    pygame.display.set_caption('Tap to Fly, Survive or Die! 🐦🔥')
    GAME_IMAGES['SCORE']=(
        pygame.image.load('ATTACHMENTS/IMAGES/0.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/1.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/2.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/3.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/4.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/5.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/6.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/7.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/8.png').convert_alpha(),
        pygame.image.load('ATTACHMENTS/IMAGES/9.png').convert_alpha(),
    )

    GAME_IMAGES['DISPLAY']=pygame.image.load('ATTACHMENTS/IMAGES/display.png').convert_alpha()
    GAME_IMAGES['BASE']=pygame.image.load('ATTACHMENTS/IMAGES/base.png').convert_alpha()
    GAME_IMAGES['PIPES']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )


    GAME_SOUNDS['die']=pygame.mixer.Sound('ATTACHMENTS/MUSIC/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('ATTACHMENTS/MUSIC/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('ATTACHMENTS/MUSIC/point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('ATTACHMENTS/MUSIC/swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('ATTACHMENTS/MUSIC/wing.wav')

    GAME_IMAGES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        WelcomeScreen()
        MainGame()
