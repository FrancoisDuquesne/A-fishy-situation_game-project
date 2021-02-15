import pygame
import settings

SCORE = 0
HIGHSCORE = 0


def Display_Score(screen, highscore, score, lives):
    font = pygame.font.SysFont('calibri', 25)
    text1 = font.render("Highscore: " + str(highscore), True, settings.BLACK)
    screen.blit(text1, (3, 3))
    text2 = font.render("Score: " + str(score), True, settings.BLACK)
    screen.blit(text2, (3, 23))
    for i in range(lives):
        screen.blit(pygame.transform.scale(pygame.image.load('resources/life.png'), (20, 20)), (3+i*30, 43))


def GameOver_Display(screen, texte):
    textefont = pygame.font.SysFont('comicsansms', 72)
    textSurface = textefont.render(texte, True, settings.BLACK)
    TextSurf,  TextRect = textSurface, textSurface.get_rect()
    TextRect.center = ((settings.DISPLAY_WIDTH/2), (settings.DISPLAY_HEIGHT/2))
    screen.fill(settings.BLUE)
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()
