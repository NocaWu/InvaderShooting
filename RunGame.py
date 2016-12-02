import pygame
from Colors import *

# ==================================== Player Class ======================================= 
class Shooter(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self) # 'S'prite!

        self.image = pygame.Surface((16,16)) # 'S'urface!
        self.image.fill(white)
        self.rect = self.image.get_rect()

    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        for event in pygame.event.get():
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT): 
                    self.rect = self.rect.move((-20,0))
                if(event.key == pygame.K_RIGHT ): 
                    self.rect = self.rect.move((20,0))        
        if self.rect.left < 2:
            self.rect.left = 2
        if self.rect.right > 218:
            self.rect.right = 218
            
# ==================================== Bullet Class ======================================= 
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        
        pygame.sprite.Sprite.__init__(self) # 'S'prite!

        self.image = pygame.Surface((2, 4)) # 'S'urface!
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y -= 10
        # kill if off screen:
        if self.rect.bottom < 0:
            self.kill()
        
# ==================================== Invader Class ======================================= 
class Invader(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self) # 'S'prite!

        self.image = pygame.Surface((16, 16)) # 'S'urface!
        self.image.fill(white)
        self.rect = self.image.get_rect()

    def set_position(self,x,y):
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        if (self.rect.y < 400):
            self.rect.y += 4
                       
        # if (self.rect.y > 400):
        #     self.kill()

class Ground(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self) 

        self.image = pygame.Surface((220, 20)) 
        self.image.fill(gray)
        self.rect = self.image.get_rect()
        self.rect.centerx = 110
        self.rect.centery = 400

# ==================================== Main  ======================================= 
def main():
# first side of the board

# we muat initialize at the beginning
    pygame.init()

# set up basic game, window size, game name, cursor, bg color
    window_size = window_width, window_height = 220,400
    window = pygame.display.set_mode(window_size, pygame.NOFRAME) 
    
    pygame.display.set_caption('Shooter Invader') 
    pygame.mouse.set_visible(0) 

# setting up the frame rate
    clock = pygame.time.Clock()

    all_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    invader_group = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()

    player = Shooter()
    player.set_position(102, 350)  
    all_group.add(player) 

    ground = Ground()
    all_group.add(ground)
    ground_group.add(ground)

    for i in range (11):
        inv = Invader()
        inv.set_position(i*20,20*(-1-i%3)) 
        all_group.add(inv)
        invader_group.add(inv) 

# ==================================== While Running ======================================= 
# keep the game running 
    running = True
    x = 0
    hit_ground = 0

    font = pygame.font.SysFont("Arial",16)
    text = font.render("SHOOT TO KEEP THEM AWAY",True,white)

    while (running):
        # player always move and shoot
        player.update()
        bull = Bullet(player.rect.centerx, player.rect.centery)
        all_group.add(bull)
        bullet_group.add(bull)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False       

        # frame rate
        clock.tick(6)
      
        if (x<5): x += 1
        if (x==5): 
            invader_group.update()
            x = 0

        all_group.update()

        # check if bullet collide with invaders:
        hit_list = pygame.sprite.groupcollide(bullet_group,invader_group, True, False)
	for key, value in hit_list.iteritems():
	    for inv in value:
	        inv.rect.y -= 20
	#if hit_list:
         #   for inv in invader_group:
          #      for bullet in bullet_group:
           #         if(inv.rect.centerx > bull.rect.centerx-10) and inv.rect.centerx < bull.rect.centerx+10:
            #                inv.rect.y -= 2

        hit_ground_list = pygame.sprite.groupcollide(invader_group, ground_group, True, False)
        if hit_ground_list:
            for hit in hit_ground_list:
                hit_ground += 1
            
        if (hit_ground >8):
            text = font.render("GAME OVER",True,white)
            
        window.fill(black)
        all_group.draw(window)

        window.blit(text,(window_width/2 - text.get_rect().width/2,4))

        pygame.display.flip()

# ==================================== Quit ======================================= 
    pygame.quit()

if __name__ == '__main__':
    main()
