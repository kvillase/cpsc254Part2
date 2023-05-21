import random
import pygame, sys
from pygame.locals import * 
from button import Button

pygame.init()

def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100
  
    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()
  
    # List containing lower pipes
    down_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
         'y': second_pipe[1]['y']},
    ]
  
    # List Containing upper pipes
    up_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
         'y': second_pipe[0]['y']},
    ]
  
    # pipe velocity along x
    pipeVelX = -9 #-4 is magic number 
    positionScore = 9
    UpperBound = 15

    # bird velocity
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1
  
    bird_flap_velocity = -8
    bird_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
  

        # This function will return true
        # if the flappybird is crashed
        if 15 < your_score < 18: 
            collision = False
            #show power up text
            gameOverScreen_TEXT = get_font(55).render("Invincible", True, "Yellow")
            gameOverScreen_RECT = gameOverScreen_TEXT.get_rect(center=(300,50))
            window.blit(gameOverScreen_TEXT, gameOverScreen_RECT)
            pygame.display.update()
        else:
            collision = True
      
        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal,
                               vertical,
                               up_pipes,
                               down_pipes,
                              collision)         

        #Game is Over go to Game Over Screen
        if game_over:
            gameOverScreen(your_score)
            return
  
        # check for your_score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + positionScore:
                your_score += 1
                print(f"Your your_score is {your_score}")

        if (your_score % 2 == 0):
            pipeVelX += -.04
            positionScore += .04
           # UpperBound += .04

        if (your_score % 5 == 0 and your_score != 0):
            pipeVelX -= -.02
            positionScore -= .02
          #  UpperBound -= .02
            gameOverScreen_TEXT = get_font(55).render("SLOW DOWN", True, "Blue")
            gameOverScreen_RECT = gameOverScreen_TEXT.get_rect(center=(300, 50))
            window.blit(gameOverScreen_TEXT, gameOverScreen_RECT)
            pygame.display.update()

        
  
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
  
        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + \
            min(bird_velocity_y, elevation - vertical - playerHeight)
  
        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
  
        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < UpperBound: ##for greater 5 is magic numb
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
  
        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
  
        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
  
        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
  
        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1
  
        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
  
        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)
  

  
def isGameOver(horizontal, vertical, up_pipes, down_pipes,Collision):

    if vertical > elevation - 25 or vertical < 0:
        return Collision
  
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and\
           abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return Collision
  
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and\
        abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return Collision
    return False
  




def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + \
        random.randrange(
            0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))  
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},
  
        # lower Pipe
        {'x': pipeX, 'y': y2}
    ]
    return pipe

#set the height and width of window#########################
window_width = 600
window_height = 499
window = pygame.display.set_mode((window_width, window_height))
elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage  = 'images/pipe.png'
background_image = 'images/background.jpg'
birdplayer_image = 'images/bird.png'
sealevel_image = 'images/base.jfif'
hourglass_image = 'assets/hourglass.png'
framepersecond_clock = pygame.time.Clock()
#############################################################

pygame.display.set_caption("Menu")

#Load images which will be used in the game#################
game_images['scoreimages'] = (
    pygame.image.load('images/0.png').convert_alpha(),
    pygame.image.load('images/1.png').convert_alpha(),
    pygame.image.load('images/2.png').convert_alpha(),
    pygame.image.load('images/3.png').convert_alpha(),
    pygame.image.load('images/4.png').convert_alpha(),
    pygame.image.load('images/5.png').convert_alpha(),
    pygame.image.load('images/6.png').convert_alpha(),
    pygame.image.load('images/7.png').convert_alpha(),
    pygame.image.load('images/8.png').convert_alpha(),
    pygame.image.load('images/9.png').convert_alpha()
)
game_images['flappybird'] = pygame.image.load(
    birdplayer_image).convert_alpha()
game_images['sea_level'] = pygame.image.load(
    sealevel_image).convert_alpha()
game_images['background'] = pygame.image.load(
    background_image).convert_alpha()
game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(
    pipeimage).convert_alpha(), 180), pygame.image.load(
  pipeimage).convert_alpha())

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/Space.ttf", size)

def gameOverScreen(score):
     while True:
        #set the basic backsreen and pointer
        window.fill("Black")
        gameOverScreen_MOUSE_POS = pygame.mouse.get_pos()

        #create text incuding Screen, Score text, actual Score
        gameOverScreen_TEXT = get_font(55).render("GAME OVER", True, "Red")
        gameOverScreen_RECT = gameOverScreen_TEXT.get_rect(center=(300, 50))
        score_TEXT = get_font(55).render("score:", True, "GREEN")
        score_RECT = score_TEXT.get_rect(center=(275, 150))
        scoreNumber_TEXT = get_font(55).render(str(score), True, "GREEN")
        scoreNumber_RECT = scoreNumber_TEXT.get_rect(center=(415, 150))

        #Display the text created
        window.blit(gameOverScreen_TEXT, gameOverScreen_RECT)
        window.blit(score_TEXT, score_RECT)
        window.blit(scoreNumber_TEXT, scoreNumber_RECT)

        #Create a button to return to main menu
        gameOverScreen_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(300, 300), 
                            text_input="MAIN MENU", font=get_font(30), base_color="White", hovering_color="Green")
        gameOverScreen_BACK.changeColor(gameOverScreen_MOUSE_POS)
        gameOverScreen_BACK.update(window)

        #Parameters for quitting game and button reaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameOverScreen_BACK.checkForInput(gameOverScreen_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def play():

    while True:
  
        # sets the coordinates of flappy bird
        horizontal = int(window_width/5)
        vertical = int(
            (window_height - game_images['flappybird'].get_height())/2)
        ground = 0
        

        while True:
            for event in pygame.event.get():
  
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
                # If the user presses space or
                # up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):
                    flappygame()
  
                # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'],
                                (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)


def LEADER_BOARD():
    while True:
        #set the basic backsreen and pointer
        LEADER_BOARD_POS = pygame.mouse.get_pos()
        window.fill("Black")

        #create text incuding that this will be the leadboard page
        LEADER_BOARD_TEXT = get_font(30).render("This is the LEADER BOARD screen.", True, "White")
        LEADER_BOARD_RECT = LEADER_BOARD_TEXT.get_rect(center=(300, 130))
        window.blit(LEADER_BOARD_TEXT, LEADER_BOARD_RECT)

        #create the button to return to the main menu
        LEADER_BOARD_BACK = Button(image=None, pos=(300, 400), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        LEADER_BOARD_BACK.changeColor(LEADER_BOARD_POS)
        LEADER_BOARD_BACK.update(window)

        #Parameters for quitting game and button reaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEADER_BOARD_BACK.checkForInput(LEADER_BOARD_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        #set the basic backsreen and pointer
        window.fill("Black")
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #Create the text for the gae name
        MENU_TEXT = get_font(55).render("Name Pending", True, "Red")
        MENU_RECT = MENU_TEXT.get_rect(center=(300, 50))

        #Create the button for the diffrent screen including play, leaderboard, and quit option
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(300, 175), 
                            text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")
        LEADER_BOARD_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(300, 300), 
                            text_input="LEADER BOARD", font=get_font(55), base_color="#d7fcd4", hovering_color="Green")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(300, 425), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="Green")

        window.blit(MENU_TEXT, MENU_RECT)


        #Set the interaction with the buttons to chnage color when you hover over 
        for button in [PLAY_BUTTON, LEADER_BOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        #Parameters for quitting game and buttons reaction
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if LEADER_BOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    LEADER_BOARD()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

