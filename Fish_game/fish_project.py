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
fish_width = 70
fish_height = 55
position = (10,0)

BigFish_width = 100
BigFish_height = 65

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A fishy situation')
clock = pygame.time.Clock()

#import fish images 
Fish_l  = pygame.image.load('Fish_l.png')
Fish_l  = pygame.transform.scale(Fish_l, (fish_width,fish_height))
# Fish_lb = pygame.image.load('Fish_lb.png')
# Fish_lb = pygame.transform.scale(Fish_lb, (fish_width,fish_height))
# Fish_b  = pygame.image.load('Fish_b.png')
# Fish_b  = pygame.transform.scale(Fish_b, (fish_width,fish_height))
# Fish_rb = pygame.image.load('Fish_rb.png')
# Fish_rb = pygame.transform.scale(Fish_rb, (fish_width,fish_height))
Fish_r  = pygame.image.load('Fish_r.png')
Fish_r  = pygame.transform.scale(Fish_r, (fish_width,fish_height))

BigFish = pygame.image.load('Bigfish.png')
BigFish_l  = pygame.transform.scale(BigFish, (BigFish_width,BigFish_height))
BigFish_r  = pygame.transform.flip(BigFish_l,1,0)





def Myfish(x,y,orientation):
	if orientation == 'l':
		gameDisplay.blit(Fish_l,(x,y))
	if orientation == 'r':
		gameDisplay.blit(Fish_r,(x,y))

def food(foodx,foody,foodw,color):
    pygame.draw.circle(gameDisplay,color,(foodx,foody),foodw)

def Display_Score(count1,count2):
    font = pygame.font.SysFont(None,25)
    text1 = font.render("Score: " + str(count1),True,black)
    gameDisplay.blit(text1,(3,3))
    text2 = font.render("Deaths: " + str(count2),True,black)
    gameDisplay.blit(text2,(3,23))

def Bigfish(Bigfish_x,Bigfish_y,orientation_bigfish):
	if orientation_bigfish == 'l':
		gameDisplay.blit(BigFish_l,(Bigfish_x,Bigfish_y))
	if orientation_bigfish == 'r':
		gameDisplay.blit(BigFish_r,(Bigfish_x,Bigfish_y))

def game_loop():
    # My fish starting point:
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    orientation = 0
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
    deaths = 0
    # Big fish starting point
    Bigfish_x = (display_width * 0.40)
    Bigfish_y = (display_width * 0.45)
    Bigfish_x_change = 2
    Bigfish_y_change = -2
     
    gameExit = False
    
    while not gameExit:
        
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
        
        # define boundaries for fish movement on on display
        if x > display_width - fish_width:
            x = display_width - fish_width
        if  x < 0:
            x = 0
        if  y > display_height - fish_height:
            y = display_height - fish_height
        if  y < 0:
	        y = 0

        # Display on screen
        gameDisplay.fill(blue)
        food(food_x,food_y,food_radius,food_color)
        Myfish(x,y,orientation)
        Display_Score(score,deaths)

        # Create food
        if food_y > display_height:
            # food_y = -random.randrange(0,display_width) - food_radius
            food_y = 0 - food_radius
            food_x = random.randrange(0,display_width)
        food_y += food_speed
        
      	# fish catches food
        if food_x > x  and  food_x < x + fish_width and food_y > y  and food_y < y + fish_height:
            food_y = display_height
            score +=1
        
        # Big fish
        if Bigfish_x_change > 0:
        	orientation_bigfish = 'r'
        else:
        	orientation_bigfish = 'l'
        
        
        if Bigfish_x > display_width - BigFish_width:
            Bigfish_x_change = -2*random.randrange(0,10)
        if  Bigfish_x < 0:
            Bigfish_x_change = 2*random.randrange(0,10)
        if  Bigfish_y > display_height - BigFish_height:
            Bigfish_y_change = -2*random.randrange(0,10)
        if  Bigfish_y < 0:
            Bigfish_y_change = 2*random.randrange(0,10)

        Bigfish_x += Bigfish_x_change
        Bigfish_y += Bigfish_y_change
        Bigfish(Bigfish_x,Bigfish_y,orientation_bigfish)
     
        # fish catches food
        if Bigfish_x > x  and  Bigfish_x < x + fish_width and Bigfish_y > y  and Bigfish_y < y + fish_height:
            y = 0
            x = 0
            deaths +=1
            score = 0
            

        pygame.display.update()
        clock.tick(60)
        
game_loop()
pygame.quit()
quit()
    
