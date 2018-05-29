"""
Created on Fri May 25 17:12:20 2018
@author: francois, jillian
"""
# j'ai fixe lives a -10 et mouvement initial du Big fish a 0 pour faciliter le developpement.

import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
blue = (19,187,255)
food_color = (255,187,19)

fish_width = 80
fish_height = 50
position = (10,0)

BigFish_width = 250
BigFish_height = 120

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A fishy situation')
clock = pygame.time.Clock()

#import fish images 
# Fish_l  = pygame.image.load('Fish_l.png')
# Fish_l  = pygame.transform.scale(Fish_l, (fish_width,fish_height))
# # Fish_lb = pygame.image.load('Fish_lb.png')
# # Fish_lb = pygame.transform.scale(Fish_lb, (fish_width,fish_height))
# # Fish_b  = pygame.image.load('Fish_b.png')
# # Fish_b  = pygame.transform.scale(Fish_b, (fish_width,fish_height))
# # Fish_rb = pygame.image.load('Fish_rb.png')
# # Fish_rb = pygame.transform.scale(Fish_rb, (fish_width,fish_height))
# Fish_r  = pygame.image.load('Fish_r.png')
# Fish_r  = pygame.transform.scale(Fish_r, (fish_width,fish_height))

BigFish = pygame.image.load('resources/Bigfish.png')
BigFish_l  = pygame.transform.scale(BigFish, (BigFish_width,BigFish_height))
BigFish_r  = pygame.transform.flip(BigFish_l,1,0)





def Myfish(x,y,orientation,score,Fish_l_raw,Fish_r_raw):
    fish_width = 80
    fish_height = 50
    Fish_l, Fish_r = fish_evolution(score,Fish_l_raw,Fish_r_raw)
    if orientation == 'l':
        gameDisplay.blit(Fish_l,(x,y))
        pygame.draw.rect(gameDisplay,red,(x,y,fish_width,fish_height),2)
    if orientation == 'r':
        gameDisplay.blit(Fish_r,(x,y))
        pygame.draw.rect(gameDisplay,red,(x,y,fish_width,fish_height),2)

def fish_evolution(score,Fish_l_raw,Fish_r_raw):
    fish_width = 80
    fish_height = 50

    if score >=5:
        fish_width += 20
        fish_height += 20
    if score >=10:
        fish_width += 20
        fish_height += 20

    Fish_l = pygame.transform.scale(Fish_l_raw, (fish_width,fish_height))
    Fish_r = pygame.transform.scale(Fish_r_raw, (fish_width,fish_height))
    return Fish_l, Fish_r

def food(foodx,foody,foodw,color):
    pygame.draw.circle(gameDisplay,color,(foodx,foody),foodw)

def extra_food(extra_food_x,extra_food_y,foodw,color):
    for i in range(len(extra_food_y)):
        pygame.draw.circle(gameDisplay,color,(extra_food_x[i],extra_food_y[i]),foodw)

def Display_Score(count1,count2,count3):
    font = pygame.font.SysFont(None,25)
    text1 = font.render("Highscore: " + str(count1),True,black)
    gameDisplay.blit(text1,(3,3))
    text2 = font.render("Score: " + str(count2),True,black)
    gameDisplay.blit(text2,(3,23))
    text3 = font.render("Lives left " + str(count3),True,black)
    gameDisplay.blit(text3,(3,43))

def GameOver_Display(texte):
    textefont = pygame.font.SysFont('comicsansms',72)
    textSurface = textefont.render(texte,True,black)
    TextSurf , TextRect = textSurface,textSurface.get_rect()
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.fill(blue)
    gameDisplay.blit(TextSurf,TextRect)
    pygame.display.flip()

def mort():
    GameOver_Display('No more lives left :(')

def Bigfish(Bigfish_x,Bigfish_y,orientation_bigfish):
	
    if orientation_bigfish == 'l':
        gameDisplay.blit(BigFish_l,(Bigfish_x,Bigfish_y))
        pygame.draw.rect(gameDisplay,red,(Bigfish_x,Bigfish_y+30,BigFish_width,BigFish_height-50),2)
    if orientation_bigfish == 'r':
        gameDisplay.blit(BigFish_r,(Bigfish_x,Bigfish_y))
        pygame.draw.rect(gameDisplay,red,(Bigfish_x,Bigfish_y+30,BigFish_width,BigFish_height-50),2)

def game_loop():

	##### LOCAL VARIABLES #####

	# Images
    Fish_l_raw  = pygame.image.load('resources/Fish_l.png')
    Fish_r_raw  = pygame.image.load('resources/Fish_r.png')
    # frames per second
    fps = 60
    # My fish starting point:
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    orientation = 'l'
    # fish position change
    x_change = 0
    y_change = 0
    # food position
    food_x = random.randrange(0, display_width)
    food_y = 0
    food_radius = 5
    food_speed = 2
    # Score
    score = 0
    highscore = 0
    lives = 3
    # Big fish starting point
    Bigfish_x = (display_width * 0.40)
    Bigfish_y = (display_width * 0.45)
    Bigfish_x_change = 0#2
    Bigfish_y_change = 0#-2
    tracking_x = 0
    tracking_y = 0
    orientation_bigfish = 'l'

	# extra food special
    extrafood=0
    extra_food_x = []
    extra_food_y = []

    framecount = 0
    gameExit = False
    
    while not gameExit:
        
        ###### KEYS #####

        # Quit key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
                # Movement keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5                  
                    orientation = 'l'
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                    orientation = 'r'
                if event.key == pygame.K_UP:
                    y_change = -5
                if event.key == pygame.K_DOWN:
                    y_change = 5
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change = 0
                if event.key == pygame.K_RIGHT: 
                    x_change = 0
                if event.key == pygame.K_UP:
                    y_change = 0
                if event.key == pygame.K_DOWN:
                    y_change = 0
        x += x_change
        y += y_change
        
        ##### BOUNDARIES #####

        # define boundaries for fish movement on on display
        if x > display_width - fish_width:
            x = display_width - fish_width
        if  x < 0:
            x = 0
        if  y > display_height - fish_height:
            y = display_height - fish_height
        if  y < 0:
            y = 0

        #####  DISPLAY #####

        gameDisplay.fill(blue)
        if extrafood != 1:
            food(food_x,food_y,food_radius,food_color)
        Myfish(x,y,orientation,score,Fish_l_raw,Fish_r_raw)
        Bigfish(Bigfish_x,Bigfish_y,orientation_bigfish)
        Display_Score(highscore,score,lives)


        ##### EVENTS #####

        # Create food
        if food_y > display_height:
            # food_y = -random.randrange(0,display_width) - food_radius
            food_y = 0 - food_radius
            food_x = random.randrange(0,display_width)
        food_y += food_speed
        
        # Extra food special
        if score == 5:
            extrafood = 1
            start_time = time.clock()
            
        if extrafood ==1:
            elapsed_time = time.clock() - start_time 
            
            if elapsed_time < 2 and framecount == 1 or elapsed_time < 2 and framecount == 15 or elapsed_time < 2 and framecount == 30 or elapsed_time < 2 and framecount == 45:
                extra_food_x.append(random.randrange(0, display_width))
                extra_food_y.append(0)
            extra_food_y=[a+1 for a in extra_food_y]
            extra_food(extra_food_x,extra_food_y,food_radius,food_color)
            
            if  elapsed_time > 2 and min(extra_food_y) > display_height:
                extrafood = 0
        
        # fish catches food
        if extrafood==1:
            for i in range(len(extra_food_x)):
                if extra_food_x[i] > x  and  extra_food_x[i] < x + fish_width and extra_food_y[i] > y  and extra_food_y[i] < y + fish_height:
                    extra_food_y[i] = display_height
                    score +=1
      		
        else:
        	if food_x > x  and  food_x < x + fish_width and food_y > y  and food_y < y + fish_height:
        		food_y = display_height
        		score +=1
        
        # Big fish
        if Bigfish_x_change > 0:
            orientation_bigfish = 'r'
        else:
            orientation_bigfish = 'l'
        
        if Bigfish_x > display_width - BigFish_width or tracking_x > random.randrange(0,display_width):
            Bigfish_x_change = -3
            tracking_x = 0
        if  Bigfish_x < 0 or tracking_x > random.randrange(0,display_width):
            Bigfish_x_change = 3
            tracking_x = 0
        if  Bigfish_y > display_height - BigFish_height or tracking_y > random.randrange(0,display_height):
            Bigfish_y_change = -3
            tracking_y = 0
        if  Bigfish_y < 0 or tracking_y > random.randrange(0,display_height):
            Bigfish_y_change = 3
            tracking_y = 0
            
        # Bigfish_x += Bigfish_x_change
        # Bigfish_y += Bigfish_y_change
        tracking_x += abs(Bigfish_x_change)/fps
        tracking_y += abs(Bigfish_y_change)/fps
             
        # Bigfish catches myfish
        if x+fish_width > Bigfish_x  and  x < Bigfish_x + BigFish_width and y + fish_height> Bigfish_y+30  and y < Bigfish_y + BigFish_height-20:
            y = 0
            x = 0
            lives -=1

        # Highscore calculation   
        if score > highscore:
           highscore = score

        # out of lives
        if lives < -10:
            mort()
            time.sleep(2)
            pygame.quit()
            quit()


        # frame counter
        if framecount > 59:
            framecount=0
        else:
            framecount+=1

        pygame.display.update()
        clock.tick(fps)
        
game_loop()
pygame.quit()
quit()
