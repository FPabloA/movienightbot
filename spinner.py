import pygame
from pygame import gfxdraw
from pygame_recorder import PygameRecord
import random
import math

#adapting code from Itisz DecisionWheel: https://github.com/ltisz/DecisionWheel
valueList = ["test", "rehersal", "trial", "practice", "experiment", 'one', 'two']

class Spinner():
    def __init__(self):
        self.degrees = 0
        self.surf = surf = pygame.Surface((100,100))
        self.surf.fill((255,255,255))
        self.surf.set_colorkey((255,255,255))
        self.surf = pygame.image.load('arrow.png').convert_alpha()
        self.where = 10, 180
        self.rotation_speed = random.randint(15,30)
        self.last_animated = 0
    
    def update(self, screen):
        self.blittedRect = screen.blit(self.surf, self.where)

    def rotate(self, screen):
        now = pygame.time.get_ticks()
        if now - self.last_animated > 50:
            self.oldCenter = self.blittedRect.center
            rotatedSurf = pygame.transform.rotate(self.surf, self.degrees)

            self.rotRect = rotatedSurf.get_rect()
            self.rotRect.center = self.oldCenter
            self.degrees += self.rotation_speed
            self.rotation_speed -= .1

            screen.blit(rotatedSurf, self.rotRect)
            if self.rotation_speed <= 0:
                #do more complex quit process
                return False
            return True
        
def getWinner(list, degrees):
    #TODO issue is probably that the sections don't start cleanly at 0 degrees, need to figure out how to calculate the offset
    
    sliceAngle = 360 / len(list)

    ind = int((degrees%360) // sliceAngle)
    print(list[ind])
    

if __name__ == "__main__":
    FPS = 24
    #init pygame & recorder
    recorder = PygameRecord('output.gif', FPS)
    pygame.init()

    font = pygame.font.SysFont(None, 28)

    screen = pygame.display.set_mode((400,400))
    
    spinner = Spinner()

    clock = pygame.time.Clock()
    n_frames = 150

    resultlist = []

    running = True
    cx = cy = r = 200
    dividers = len(valueList)
    radconv = math.pi/180
    divs = int(360/dividers)
    
    #can maybe improve this by scrambling then popping from end?
    for i in range(len(valueList)):
        resultlist.append(random.choice(valueList))
        valueList.remove(resultlist[i])

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        screen.fill([255,255,255])

        spinner.update(screen)
        
        screen.fill([255,255,255])
        pygame.draw.circle(screen, (0,0,0), (cx, cy), r, 3)
        for i in range(dividers):
            gfxdraw.pie(screen, cx, cy, r, i*divs, divs, (0,0,0))
        i = 1
        iters = range(1,dividers*2, 2)
        for i in iters:
            textChoice = font.render(resultlist[iters.index(i)], False, (0,0,0))
            textWidth = textChoice.get_rect().width
            textHeight = textChoice.get_rect().height
            textChoice = pygame.transform.rotate(textChoice,(i-(2*i))*(360/(dividers*2)))
            textwidth = textChoice.get_rect().width
            textheight = textChoice.get_rect().height
            screen.blit(textChoice,(
                                (cx-(textwidth/2))
                                +((r-100)*math.cos(((i*(360/(dividers*2))))*radconv)),
                                (cy-(textheight/2))
                                +((r-100)*math.sin(((i*(360/(dividers*2))))*radconv))
                                )
                            )
            textChoice = ''

        running = spinner.rotate(screen)

        recorder.add_frame()
        clock.tick(FPS)
        # Used here to limit the size of the GIF, not necessary for normal usage. **For this purpose must be under discord 8mb limit
        n_frames -= 1

        
        
        pygame.display.flip()
        
    for i in range(24):
        recorder.add_frame()
        
    recorder.save()
    getWinner(list(reversed(resultlist)), spinner.degrees)
    pygame.quit()