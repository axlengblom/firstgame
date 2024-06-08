import pygame
import random

# a basic layout for the game

# initialize the game
pygame.init()

spritesheet = pygame.image.load("pygame/first/assets/player/roguelikeChar_transparent.png")
map = pygame.image.load("pygame/first/assets/map/map.png")

# create a screen
screen = pygame.display.set_mode((918, 515))


# set the title of the game
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

#varibles for the cleaning area that is randomized at the start of the game
clean_x = random.randint(0, screen.get_width())
clean_y = random.randint(0, screen.get_height())
clean_width = 100 
clean_height = 100

#variables for the players inventory
dirt = 0    #amount of dirt in the players inventory
gold = 0    #amount of gold in the players inventory
gems = 0    #amount of gems in the players inventory
silver  = 0 #amount of silver in the players inventory

#handle the time
clock = pygame.time.Clock()
dt = 1000/60

# game loop
running = True
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #load the map as the background of the game
    screen.blit(map, (0, 0))


    #create a loop that check that the entire digging area is inside the screen and redraws the area until is inside the screen
    while dig_x + dig_width > screen.get_width() or dig_y + dig_height > screen.get_height():
        dig_x = random.randint(0, screen.get_width())
        dig_y = random.randint(0, screen.get_height())



    #draw the digging area as a brown area
    pygame.draw.rect(screen, (139,69,19), (dig_x, dig_y, dig_width, dig_height))


    #check that the cleaning area is not in the same position as the digging area and that the entire cleaning area is inside the screen
    while clean_x + clean_width > screen.get_width() or clean_y + clean_height > screen.get_height() or (clean_x > dig_x and clean_x < dig_x + dig_width and clean_y > dig_y and clean_y < dig_y + dig_height):
        clean_x = random.randint(0, screen.get_width())
        clean_y = random.randint(0, screen.get_height())

    #draw the cleaning area as a dark blue area running like a river running through the map
    pygame.draw.rect(screen, (0, 0, 139), (clean_x, clean_y, clean_width, clean_height))

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
                pygame.draw.rect(screen, (255, 255, 255), (player_x - 24, player_y - 20, i / 2, 10))
                pygame.display.flip()
                pygame.time.wait(10)
            dirt += 1
            print("Dirt added to inventory total amount of dirt: ", dirt)

    #when the player is in the cleaning area and has dirt in the inventory the dirt will be turned into silver gold or gems with increasing rarity and the amount of the item will be added to the inventory while the dirt will be removed, 1 dirt will be removed for each press of the key
    if player_x > clean_x and player_x < clean_x + clean_width and player_y > clean_y and player_y < clean_y + clean_height:
        if keys[pygame.K_SPACE]:
            if dirt > 0:
                for i in range(0, 100):
                    pygame.draw.rect(screen, (255, 255, 255), (player_x - 24, player_y - 20, i/2, 10))
                    pygame.display.flip()
                    pygame.time.wait(10)
                dirt -= 1
                item = random.randint(1, 100)
                print(item)
                if item > 35 and item < 70:
                    silver += 1
                    print("Silver added to inventory total amount of silver: ", silver)
                elif item > 70 and item < 90:
                    gold += 1
                    print("Gold added to inventory total amount of gold: ", gold)
                elif item > 90 and item < 100:
                    gems += 1
                    print("Gems added to inventory total amount of gems: ", gems)
                else:
                    print("No item was found")
            else:
                pygame.time.wait(100)
                print("No dirt in inventory")

            
    # update the screen
    pygame.display.flip()

    dt = clock.tick(60)/1000
# quit the game

pygame.quit()
