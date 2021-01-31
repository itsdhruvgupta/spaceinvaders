import pygame
import random
import math
from pygame import mixer
pygame.init()

#create screen
screen = pygame.display.set_mode((800,600)) 

# title and icon
pygame.display.set_caption(" Space fight")
icon = pygame.image.load('image/icon.png')
pygame.display.set_icon(icon)

# sound background sound
mixer.music.load('sounds/music.mp3')
mixer.music.play(-1)

# score
score_count = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY= 10

# Game over
game_over_text = pygame.font.Font('freesansbold.ttf', 55)


# player and position
playerImg = pygame.image.load('image/player.png')
playerX = 370
playerY = 480
playerX_move = 0
playerY_move = 0


#enemy and position
enemyImg = []
enemyX = []
enemyY = []
enemyX_move = []
enemyY_move = []

no_of_enemy = 6

for i in range(no_of_enemy):
    enemyImg.append(pygame.image.load('image/enm.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(10,150))
    enemyX_move.append(3)
    enemyY_move.append(0.2)
    

#backgruong image
Background = pygame.image.load('image/background.jpg')

# bullet
bulletImg = pygame.image.load('image/bullet.png')
bulletX = 0
bulletY = 480
bullet_state = "ready"
bulletX_move = 0
bulletY_move = 40

def fscore(x, y):
    score = font.render(" Score : " + str(score_count), True, (255,255,255))
    screen.blit(score,(x,y))

def fplayer(x,y):
    screen.blit(playerImg,(x,y))
    
def fenemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))
    
def fbullet (x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16,y + 10))
    
def iskill(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if dist <=28:
        return True
    else:
        False

def gameOver():
    gameOver = game_over_text.render( 'GAME OVER',True,(255,255,255))
    screen.blit(gameOver,(220,300))
    

# ---------button------------
Lred = (200,000,000)
Dred = (255,000,000)
Action = "fire"
def fbutton(msg,x,y,w,h,lcolor,dcolor,bulletX,playerX,Action = None):
    # mouse position
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    print(mouse)
    if (x+100 > mouse[0] > x and y+50 > mouse[1] > y) :
        pygame.draw.rect(Background, lcolor, ( x,y,w,h))
        buttonText = pygame.font.Font('freesansbold.ttf', 20)
        textover= buttonText.render(msg, True, (255,255,255))
        textrect = ((x+25),(y+18))
        screen.blit(textover,(textrect))
#         if click[0] == 1 and Action == "fire" and bullet_state == "ready":
#             bulletX = playerX
#             fbullet(playerX,bulletY)
            
    else: 
        pygame.draw.rect(Background, dcolor, ( x,y,w,h))
        buttonText = pygame.font.Font('freesansbold.ttf', 20)
        textover= buttonText.render(msg, True, (255,255,255))
        textrect = ((x+25),(y+18))
        screen.blit(textover,(textrect))
    
    

# game loop
running = True
while running:
    
    # screen color
    screen.fill((0,0,0))
    
    # Background image
    screen.blit(Background,(0,0))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # control player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_move -= 15
            if event.key == pygame.K_RIGHT:
                playerX_move += 15
            if event.key == pygame.K_UP:
                playerY_move -= 15
            if event.key == pygame.K_DOWN:
                playerY_move += 15
                
            # fire bullet
            if event.key == pygame.K_SPACE and bullet_state == "ready" :
                    bulletX = playerX
                    fbullet(bulletX,bulletY)
                
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_move = 0
                
            if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerY_move = 0
                
    #----------mouse control-------correct code you can run
#     mouse = pygame.mouse.get_pos()
#     if mouse[0] > playerX:
#         playerX = mouse[0]
#     elif mouse[0] > playerX:
#         playerX = 0
#     else :
#         playerX =mouse[0]
    
    #correct code you can run this
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if (30+100 > mouse[0] > 30 and 400+50 > mouse[1] > 400) and bullet_state == "ready" :
        if click[0] == 1 :
            bulletX = playerX
            fbullet(bulletX,bulletY)
        #------mouse colntrol
#         def mouseControl(playerX=0): 
#             mouse = pygame.mouse.get_pos()
#             if mouse[0] > playerX:
#                 playerX += 15
#             if mouse[0] < playerX:
#                 playerX -=15
     
        
        
    #update enemy position
    for i in range(no_of_enemy):
        enemyX[i] += enemyX_move[i]
        enemyY[i] += enemyY_move[i]
        if enemyX[i] >= 734:
            enemyX_move[i] -= 1
        if enemyX[i] <= 5:
            enemyX_move[i] += 1
        
        # bullet
        kill = iskill(enemyX[i], enemyY[i], bulletX, bulletY)
        if kill:
            print("kill")
            bulletY = playerY
            # cuont score
            score_count += 1
            print(score_count)
            bullet_state = "ready"
            
            #add new enemy or change the location the enemy
            enemyX[i] = random.randint(0,800)
            enemyY[i] = 0
            
        # call enemy function
        fenemy(enemyX[i],enemyY[i], i)
        
        for j in range(no_of_enemy):
            if enemyY[j] > 535:
                for j in range(no_of_enemy):
                    enemyY[j] = 1200
                gameOver()
                break
        
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
        
    if bullet_state is "fire" :
        fbullet(bulletX,bulletY)
        bulletY -= bulletY_move
        
    #update player position
    playerX += playerX_move
    playerY += playerY_move
    
    if playerX > 800:
        playerX = 0
    if playerX < 0:
        playerX = 800
        
    if playerY > 535:
        playerY = 535
    if playerY < 370:
        playerY = 370
        
    # call player function
    fplayer(playerX, playerY)
    
    # call score function
    fscore(textX,textY)
    
    #call button function
    fbutton(' Fire',30,400,100,50,Lred,Dred,bulletX,playerX,Action)
    
    # call mouse control function
#     mouseControl()
    

    # update display
    pygame.display.update()
    
    