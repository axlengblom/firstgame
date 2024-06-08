import pygame
import random
import math

# a basic layout for the game

# initialize the game
pygame.init()

spritesheet = pygame.image.load("pygame/first/assets/player/roguelikeChar_transparent.png")

# create a screen
screen = pygame.display.set_mode((800, 600))

# River area
clean_x = 100
clean_y = 500
clean_width = 700
clean_height = 100

def draw_river(screen, frame):
    river_color = (0, 0, 255)
    wave_amplitude = 5
    wave_frequency = 50
    river_points = [
        (100, 500 + wave_amplitude * math.sin(frame / wave_frequency + 0)),
        (200, 400 + wave_amplitude * math.sin(frame / wave_frequency + 1)),
        (300, 450 + wave_amplitude * math.sin(frame / wave_frequency + 2)),
        (400, 350 + wave_amplitude * math.sin(frame / wave_frequency + 3)),
        (500, 400 + wave_amplitude * math.sin(frame / wave_frequency + 4)),
        (600, 300 + wave_amplitude * math.sin(frame / wave_frequency + 5)),
        (700, 350 + wave_amplitude * math.sin(frame / wave_frequency + 6)),
        (800, 250 + wave_amplitude * math.sin(frame / wave_frequency + 7)),
        (800, 600), 
        (0, 600)
        ]
    pygame.draw.polygon(screen, river_color, river_points)
# set the title of the game

def clean_dirt():
    global dirt, silver, gold, gems

    if dirt > 0:
        for i in range(0, 100):
            draw_progress_bar(screen, clean_x, clean_y - 20, i)
        dirt -= 1
        item = random.randint(1, 100)
        print(item)
        if 35 < item < 70:
            silver += 1
            print("Silver added to inventory total amount of silver: ", silver)
        elif 70 < item < 90:
            gold += 1
            print("Gold added to inventory total amount of gold: ", gold)
        elif 90 < item < 100:
            gems += 1
            print("Gems added to inventory total amount of gems: ", gems)
        else:
            print("No item was found")
    else:
        for i in range(0, 100):
            draw_progress_bar(screen, clean_x, clean_y - 20, i)
            pygame.time.wait(1)
        print("No dirt in inventory")

def draw_progress_bar(screen, x, y, progress):
    pygame.draw.rect(screen, (255, 255, 255), (x, y, progress, 10))
    pygame.display.flip()
    pygame.time.wait(10)

pygame.display.set_caption("My First Game")

#variables for the player 
#function to get a sprite from a spritesheet
def get_sprite(x, y, width, height):
    sprite = pygame.Surface((width, height))
    sprite.set_colorkey((0,0,0))
    sprite.blit(spritesheet, (0, 0), (x, y, width, height))
    return sprite
character_sprite = get_sprite(0, 102, 16, 16)

player_x = screen.get_width() / 2
player_y = screen.get_height() / 2
player_width = 16   
player_height = 16



#variables for a digging area that is randomized at the start of the game
dig_x = random.randint(0, screen.get_width())
dig_y = random.randint(0, screen.get_height())
dig_width = 100 
dig_height = 100



#variables for the players inventory
dirt = 0    #amount of dirt in the players inventory
gold = 0    #amount of gold in the players inventory
gems = 0    #amount of gems in the players inventory
silver  = 0 #amount of silver in the players inventory

#handle the time
clock = pygame.time.Clock()
dt = 1000/60

frame = 0
# game loop
running = True
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the background looking like dark green grass
    screen.fill((0, 100, 0))


    #create a loop that check that the entire digging area is inside the screen and redraws the area until is inside the screen
    while dig_x + dig_width > screen.get_width() or dig_y + dig_height > screen.get_height():
        dig_x = random.randint(0, screen.get_width())
        dig_y = random.randint(0, screen.get_height())



    #draw the digging area as a brown area
    pygame.draw.rect(screen, (139,69,19), (dig_x, dig_y, dig_width, dig_height))

    #draw the cleaning area as a dark blue area running like a river running through the map
    draw_river(screen, frame)


    #draw the player as a character using an image
    #transform the image to the size of the player
    character_sprite = pygame.transform.scale(character_sprite, (player_width, player_height))
    screen.blit(character_sprite, (player_x - (player_width/2), player_y - (player_height/2)))  #draw the player

    #draw the players inventory
    font = pygame.font.Font(None, 36)
    text = font.render("Dirt: " + str(dirt), True, (255, 255, 255))
    screen.blit(text, (10, 10))
    text = font.render("Gold: " + str(gold), True, (255, 255, 255))
    screen.blit(text, (10, 50))
    text = font.render("Gems: " + str(gems), True, (255, 255, 255))
    screen.blit(text, (10, 90))
    text = font.render("Silver: " + str(silver), True, (255, 255, 255))
    screen.blit(text, (10, 130))


    #movement for the character using the wasd keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= 3
    if keys[pygame.K_s]:
        player_y += 3
    if keys[pygame.K_a]:
        player_x -= 3
    if keys[pygame.K_d]:
        player_x += 3
    
    #when the player is in the diggin area and the player presses the space key, the amount of dirt in the players inventory will increase by 1 after 3 seconds of hold the space key
    if player_x > dig_x and player_x < dig_x + dig_width and player_y > dig_y and player_y < dig_y + dig_height:
        if keys[pygame.K_SPACE]:
            for i in range(0, 100):
                pygame.draw.rect(screen, (255, 255, 255), (dig_x, dig_y - 20, i, 10))
                pygame.display.flip()
                pygame.time.wait(10)
            dirt += 1
            print("Dirt added to inventory total amount of dirt: ", dirt)

    
    if clean_x < player_x < clean_x + clean_width and clean_y < player_y < clean_y + clean_height:
        if keys[pygame.K_SPACE]:
            clean_dirt()
            
    # update the screen
    pygame.display.flip()

    dt = clock.tick(60)/1000
    frame += 1
# quit the game

pygame.quit()
