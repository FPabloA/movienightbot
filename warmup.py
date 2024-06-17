#import and init pygame
import pygame

pygame.init()

#create display window
screen = pygame.display.set_mode([500,500])

#run until user clicks exit
running = True

while running:
    
    #was exit clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #white background
    screen.fill((255,255,255))

    #draw a solid circle in center
    pygame.draw.circle(screen, (0,0,255), (250,250), 75)

    #flips/updates display
    pygame.display.flip()

pygame.quit()