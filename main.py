import random
import sys
import pygame
from pygame.locals import * 

FPS = 32
SCREENWIDTH = 350
SCREENHEIGHT = 512
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
BACKGROUND = 'gallery/sprites/background_morning.png'
PIPE = 'gallery/sprites/pipe.png'
def selectBirdScreen():
    bird_options = ['bluebird', 'yellowbird', 'redbird']
    selected_bird = 'bluebird'  # Default selection

    bird_frames = {
        'bluebird': load_bird_frames('gallery/sprites/bluebird.png'),
        'yellowbird': load_bird_frames('gallery/sprites/yellowbird.png'),
        'redbird': load_bird_frames('gallery/sprites/redbird.png')
    }

    # Load the "Choose a Bird to Start" image
    choose_bird_image = pygame.image.load('gallery/sprites/choosing.png').convert_alpha()
    
    # Position for the bird options on the screen
    option_y = int(SCREENHEIGHT / 2)
    
    # Adjusted option_x values to make sure birds are centered and not too close to the edges
    option_x = [SCREENWIDTH / 6, SCREENWIDTH / 2, 5 * SCREENWIDTH / 6]
    
    # Position for the choose_bird_image
    choose_bird_x = (SCREENWIDTH - choose_bird_image.get_width())/2
    choose_bird_y = SCREENHEIGHT * 0.05  # A bit below the top

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # Check for arrow key inputs or mouse clicks to change the selection
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    selected_bird = bird_options[bird_options.index(selected_bird) - 1]
                elif event.key == K_RIGHT:
                    selected_bird = bird_options[(bird_options.index(selected_bird) + 1) % len(bird_options)]
                elif event.key == K_RETURN:
                    # Return the selected bird frames when Enter is pressed
                    return bird_frames[selected_bird]
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i, option in enumerate(bird_options):
                    if option_x[i] - 20 < mouse_x < option_x[i] + 20 and option_y - 20 < mouse_y < option_y + 20:
                        return bird_frames[option]

        # Display the selection screen
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))

        # Display the "Choose a Bird to Start" image
        SCREEN.blit(choose_bird_image, (choose_bird_x, choose_bird_y))
        
        # Display the bird options
        for i, option in enumerate(bird_options):
            bird_image = bird_frames[option][0]
            SCREEN.blit(bird_image, (option_x[i] - bird_image.get_width() / 2, option_y - bird_image.get_height() / 2))

            # Highlight the selected option
            if option == selected_bird:
                pygame.draw.rect(SCREEN, (255, 0, 0), (option_x[i] - bird_image.get_width() / 2 - 5, option_y - bird_image.get_height() / 2 - 5, bird_image.get_width() + 10, bird_image.get_height() + 10), 2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def load_bird_frames(sprite_path):
    # Load the bird sprite sheet
    sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
    frame_width = sprite_sheet.get_width() // 3
    frame_height = sprite_sheet.get_height()

    # Extract the frames from the sprite sheet
    bird_frames = []
    for i in range(3):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        bird_frames.append(frame)

    return bird_frames

def welcomeScreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'][0].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'][0], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8
    playerFlapped = False

    bird_frame_index = 0  # To keep track of bird animation frame
    bird_animation_speed = 5  # Speed at which bird flaps its wings
    bird_animation_counter = 0  # Counter to track animation changes

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'][0].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Bird animation logic
        bird_animation_counter += 1
        if bird_animation_counter % bird_animation_speed == 0:
            bird_frame_index = (bird_frame_index + 1) % len(GAME_SPRITES['player'])
            bird_animation_counter = 0

        # Rendering the game screen
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'][bird_frame_index], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if playery + GAME_SPRITES['player'][0].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},  # upper Pipe
        {'x': pipeX, 'y': y2}  # lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Tap to Fly, Survive or Die! 🐦🔥')

    # Load bird frames (animation) from sprite sheet
    GAME_SPRITES['player'] = load_bird_frames('gallery/sprites/bluebird.png')

    # Load other game assets
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background']=pygame.image.load(BACKGROUND)
    # Load sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        GAME_SPRITES['player'] = selectBirdScreen()  # Get the frames for the selected bird
        mainGame()
