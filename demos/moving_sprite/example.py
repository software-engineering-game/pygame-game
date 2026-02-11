import pygame
# Pygame is a set of Python modules designed for writing games. It is written on top of the excellent SDL library. 
#in Pygame +x goes right, +y goes down
pygame.init()

screen = pygame.display.set_mode((640, 640))

cat_img = pygame.image.load('cat.png').convert()

cat_img = pygame.transform.scale(cat_img, 
                                (cat_img.get_width() * .5,
                                 cat_img.get_height() * .5))

running = True
x = 0
clock = pygame.time.Clock()

delta_time = 0.1
while running:
    screen.fill((255,255,255))
    
    screen.blit(cat_img, (x,30))
    
    x += 50 * delta_time

    for event in pygame.event.get():
     if event.type == pygame.QUIT:
        running = False
        
    pygame.display.flip() #Allows us to actually show sprite on window
        
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001,min(0.1,delta_time))
pygame.quit()