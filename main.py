import pygame
import sys
import random


class Player(pygame.sprite.Sprite):                                             # Using Sprite
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Trex_clone/images/hk2.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.g = 0

        self.jumpsound = pygame.mixer.Sound('Trex_clone\sound\jump_sound_effect.mp3')
        self.jumpsound.set_volume(0.7)                                           # Arguments: from 0(muted) to 1(highest)

    def player_input(self):
        keys = pygame.key.get_pressed()                                          # List of all keys
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:                     # Adding JUMP
            self.g = -20
            self.jumpsound.play()

    def gravity(self):
        self.g += 1                                                              # Stimulating gravity (not accurate)
        self.rect.y += self.g
        if self.rect.bottom >= 300:                                              # Not letting player fall through the screen
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.gravity()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_surf = pygame.image.load('Trex_clone/images/3.png').convert_alpha()
            self.frame = fly_surf
            y_pos = 100
        elif type == 'rabbit':
            rabbit_surf = pygame.image.load('Trex_clone/images/rabbit2.png').convert_alpha()
            self.frame = rabbit_surf
            y_pos = 300
        

        self.image = self.frame
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),y_pos))

    def destroy(self):                                                         # Removes the enemies as they pass the screen
        if self.rect.x <= -100: 
            self.kill()

    def update(self):
        self.rect.x -= 6
        self.destroy()
    



def display_score():
    current_time = int((pygame.time.get_ticks()/1000) - start_time)
    score_surf = test_font.render("Score: " + str(current_time), False, ("Red")) # Arguments: (Text, Anti Aliasing, color)
    score_rec = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rec)
    return current_time
 
def collision(player,enemies):                                                   # Checking for collisions
    if enemies:
        for rectangle in enemies:
            if player.colliderect(rectangle):
                return False
    return True

def collision_sprite():                                                          # Arguments for spritecollide: (sprite, group, bool) 
                                                                                 # True: rabbit will be deleted once the player collides                                                                             
                                                                                 # False: Rabbit will not be deleted
    if pygame.sprite.spritecollide(player.sprite,enemy_group,False):
        enemy_group.empty()                                                      # Remove the sprites once the game ends                                  
        return False
    else:
        return True                                                                             






pygame.init()                                                                    # Starts Pygame



### Screen ###
w = 800
h = 400
screen = pygame.display.set_mode((w,h)) 
pygame.display.set_caption("Trex Clone")                                         # Title of the screen
clock = pygame.time.Clock() 
test_font = pygame.font.Font('Trex_clone/font/Pixeltype.ttf', 50)                # Arguments: (font type, font size)
game_active = True
start_time = 0                                                                   # To reset score

bgmusic = pygame.mixer.Sound('Trex_clone\sound\cruising-down-8bit-lane.mp3')
bgmusic.play(loops = -1)                                                         # To loop this song forever loops = -1



player = pygame.sprite.GroupSingle()
player.add(Player())


enemy_group = pygame.sprite.Group()



sky_surface = pygame.image.load('Trex_clone/images/Sky.png').convert()           # loading image 
ground_surface = pygame.image.load('Trex_clone/images/ground.png').convert()








### Timer ###

enemy_timer = pygame.USEREVENT + 1                                                    # Custom user event
pygame.time.set_timer(enemy_timer,900)                                                # Arguments : (Event you want to trigger, time (in miliseconds))





while True: 


    ### EVENT LOOP ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:                                                  # To quit pygame
            pygame.quit()
            sys.exit()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                              
        if event.type == enemy_timer and game_active:                                  # Creating a list of enemy          
            enemy_group.add(Enemy(random.choice(['fly','rabbit','rabbit'])))
        
            



    if game_active:
        
        screen.blit(sky_surface,(0,0))                                                 # Arguments: (Surface, position(x,y))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        display_score()


        
        ### Player Sprite ###
        player.draw(screen)
        player.update()

        ### Enemy Sprite ###
        enemy_group.draw(screen)
        enemy_group.update()

        ### COLLISION ###
        game_active = collision_sprite()



    else:
        retry_prompt = test_font.render("Retry ? ", False, ("Black")) 
        prompt_rec = retry_prompt.get_rect(center = (400,200))
        screen.blit(retry_prompt,prompt_rec)
        start_time = pygame.time.get_ticks()/1000                                  # To reset score
                                            


   

    pygame.display.update()
    clock.tick(60) # Setting the FPS. [The while loop should not run faster than 60 times per second]


