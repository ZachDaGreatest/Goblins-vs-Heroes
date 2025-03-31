import pygame
import math
from Hero_handler import hero_handler

button = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Buttons\\Button_Blue_9Slides.png')
button = pygame.transform.scale(button, (64,64))

hovered_button = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Buttons\\Button_Blue_9Slides.png')
hovered_button = pygame.transform.scale(hovered_button,(64,128))

knight_image = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Factions\\Knights\\Troops\\Warrior\\Blue\\Warrior_Blue.png')
knight_image = pygame.transform.scale_by(knight_image, .5)

bottom_right_rim = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Pointers\\06.png')
bottom_right_rim = pygame.transform.scale(bottom_right_rim, (64,64))

bottom_left_rim = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Pointers\\05.png')
bottom_left_rim = pygame.transform.scale(bottom_left_rim, (64,64))

top_right_rim = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Pointers\\04.png')
top_right_rim = pygame.transform.scale(top_right_rim, (64,64))

top_left_rim= pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Pointers\\03.png')
top_left_rim= pygame.transform.scale(top_left_rim, (64,64))

health_icon = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\02.png')
health_icon = pygame.transform.scale(health_icon, (32,32))

damage_icon = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\14.png')
damage_icon = pygame.transform.scale(damage_icon, (32,32))

cost_icon = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Resources\\Resources\\G_Idle_(NoShadow).png')
cost_icon = pygame.transform.scale(cost_icon, (32,32))


item_xoffset = 16
item_yoffset = 16


selected = [False,0]


troop_data = hero_handler()
last_selected_troop = "none"
items = []
for troop in troop_data.hero_types.keys():
    items.append(str(troop))
#create a list of icons across the top of the screen for troops and power ups 

def render_icon(state,screen, posx, posy, index):
    
    if state == "idle":

        #just draw the button and what img is supposed to be on the button 
        screen.blit(button,(posx,posy)) #draw the button 
        #screen.blit(knight_image, (posx-item_xoffset,posy-item_yoffset),(0,0,96,96)) #draw the item icon there, a knight for now

    elif state == "selected":

        #draw the stretched button, add golden rims, and then item img and its stats
        

        screen.blit(top_right_rim, (posx+ 28,posy-22))
        screen.blit(top_left_rim, (posx-28,posy-22))

        screen.blit(hovered_button, (posx,posy))

        screen.blit(bottom_right_rim, (posx+ 26,128-40))
        screen.blit(bottom_left_rim, (posx-26,128-40))

        
        #screen.blit(knight_image, (posx-item_xoffset,posy-item_yoffset), (0,0,96,96)) #need only one sprite img
    else:

        #this is being hovered over, so draw the stretched button, the item's img, and its stats 
        screen.blit(hovered_button, (posx,posy))
        #screen.blit(knight_image, (posx-item_xoffset,posy-item_yoffset), (0,0,96,96)) #need only one sprite img
    
    try:
        #draw in the item images
        if items[index] == "pawn":
            #draw the pawn 
            screen.blit(troop_data.hero_types["pawn"]["image"], (posx-item_xoffset,posy-item_yoffset), (0,0,96,96)) #need only one sprite img
            
        elif items[index] == "standard":
            #draw in the knight 
            screen.blit(troop_data.hero_types["standard"]["image"], (posx-item_xoffset,posy-item_yoffset), (0,0,96,96)) #need only one sprite img
            
        elif items[index] == "archer":
            #draw in the archer and its bow 
            screen.blit(troop_data.hero_types["archer"]["image"], (posx-item_xoffset,posy-item_yoffset), (0,0,96,96)) #need only one sprite img
            screen.blit(troop_data.hero_types["archer"]["bow"], (posx-item_xoffset,posy-item_yoffset), (0,0,96,96)) #need only one sprite img
        
        #if its selected or hovered over; draw in the troop's stats 
        
        if state == "selected" or state == "hover":
            #render icons for stats
            
            screen.blit(health_icon,(posx+5,posy+52))
            screen.blit(damage_icon,(posx+5,posy+72))
            screen.blit(cost_icon,(posx+5,posy+84))
            
            # Define colors
            white = (255, 255, 255)

            # Load font and render stats
            posy -= 10
            font = pygame.font.SysFont("Arial", 14)  # Using SysFont instead of Font file

            # Render text for health
            text = font.render(f"{str(troop_data.hero_types[items[index]]["max_health"])}", True, white)  # Antialiasing set to True
            screen.blit(text, (posx+32,posy+72))

            #render text for damage
            text = font.render(f"{str(troop_data.hero_types[items[index]]["damage"])}", True, white)  # Antialiasing set to True
            screen.blit(text, (posx+32,posy+88))

            #render text for cost
            text = font.render(f"{str(troop_data.hero_types[items[index]]["cost"])}", True, white)  # Antialiasing set to True
            screen.blit(text, (posx+32,posy+104))

    except:
        #this is prob bc not enough items to fill all of the icons
        return last_selected_troop
        

def check_gui_click(x,y): # if the click was on one of button, make that button slected
    global selected
    global last_selected_troop
    try:
        for icon_num in range(0, int(math.floor(640/64))):#generate howevere many boxes can fit on the screen
            #check if mouse pos is within a 64 pixel range of this pos so we know it was clicked
            xdiff = x - icon_num*64

            if 0<= xdiff <64 and y <64:
                #we clicked this icon
                selected = [True, icon_num]
                last_selected_troop = items[icon_num]
                return items[icon_num] #let the game know we prob changed troop type
        else:
            #we didn't click on a button so return what was last selcted
            return last_selected_troop
    except:
        #we prob clicked on an empty icon, and we couldn't return anything, so return the empty value place holder
        return "none"


# # Define colors
#     white = (255, 255, 255)
#     black = (0, 0, 0)

#     # Load font
#     font = pygame.font.SysFont("Arial", 12)  # Using SysFont instead of Font file

#     # Render text
#     text = font.render("29", True, white)  # Antialiasing set to True
#     #text_rect = text.get_rect(center=(250, 250))
#     screen.blit(text, (64,0))


def render_gui(screen, cursor_pos):#640 by 328 screen
    
    for icon_num in range(0, int(math.floor(640/64))):#generate howevere many boxes can fit on the screen
        #check if mouse pos is within a 64 pixel range of this pos so we know it is being hovered over 
        xdiff = cursor_pos[0] - icon_num*64

        if (selected[0] == True) and (selected[1] == icon_num):

            render_icon("selected", screen, icon_num*64, 0, icon_num) #this one is selected so flag as selcted and render

        elif 0<=xdiff<64 and cursor_pos[1]<64:
    
            render_icon("hover", screen, icon_num*64, 0, icon_num)  #we are hovering over this icon so flag it as hovered 
        else:    
            
            render_icon("idle", screen, icon_num*64, 0, icon_num) #we aren't hovering over this one so just render it normally




