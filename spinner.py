import pygame
from pygame_recorder import PygameRecord
from random import randint

#class adapted from u/WuxiaScrub on r/pygame post
class Spinner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('temp_spinner.png')
        self.image = pygame.image.load('temp_spinner.png')
        #self.image = pygame.transform.rotate(self.original_image, randint(0, 359))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.rotation_speed = randint(15, 30)
        self.last_animated = 0
        self.total_degrees_spun = 0
        self.spinning = False

    def update(self):
        if self.spinning:
            self.spin()
    
    def spin(self):
        now = pygame.time.get_ticks()
        if now -self.last_animated > 50:
            self.image = pygame.transform.rotate(self.original_image, -self.total_degrees_spun)
            self.rect = self.image.get_rect(center=(self.x, self.y))
            self.total_degrees_spun += self.rotation_speed
            self.rotation_speed -= .1
            if self.rotation_speed <=0:
                self.spinning = False
                self.rotation_speed = randint(15, 25)


if __name__ == "__main__":
    FPS = 24
    #init pygame & recorder
    recorder = PygameRecord('output.gif', FPS)
    pygame.init()

    screen = pygame.display.set_mode((500,500))
    running = True
    clock = pygame.time.Clock()
    n_frames = 150

    bg = pygame.image.load("MovieWheelBG.png")

    all_sprites = pygame.sprite.Group()
    spinner = Spinner(250,250)
    all_sprites.add(spinner)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))
        screen.blit(bg, (0,0))
        spinner.spinning = True
        #save frame
        all_sprites.update()
        all_sprites.draw(screen)  
        pygame.display.update()
        recorder.add_frame()
        clock.tick(FPS)
        # Used here to limit the size of the GIF, not necessary for normal usage. **For this purpose must be under discord 8mb limit
        n_frames -= 1
        if spinner.spinning == False:
            for i in range(24):
                recorder.add_frame()
            print('stopped')
            break
    recorder.save()
    pygame.quit()