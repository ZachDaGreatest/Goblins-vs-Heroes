import pygame 
import random
foam = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Water\\Foam\\Foam.png') #needs to be resized to 512, 64
foam = pygame.transform.scale(foam,(512,64))

big_water_rock = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Water\\Rocks\\Rocks_03.png') #needs to be resized to 512, 64
big_water_rock = pygame.transform.scale(big_water_rock,(512,64))

small_water_rock =pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Water\\Rocks\\Rocks_01.png') #needs to be resized to 512, 64
small_water_rock = pygame.transform.scale(small_water_rock,(512,64))

med_water_rock=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Water\\Rocks\\Rocks_02.png')
med_water_rock = pygame.transform.scale(med_water_rock,(512,64))

grass=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Ground\\Tilemap_Flat.png')
grass = pygame.transform.scale(grass,(64,64))

bush=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\09.png')
bush = pygame.transform.scale(bush,(32,32))

mushroom=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\02.png')
mushroom = pygame.transform.scale(mushroom,(64,64))

rock=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\05.png')
rock = pygame.transform.scale(rock,(64,64))

bone=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\15.png')
bone = pygame.transform.scale(bone,(64,64))

pumpkin=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Deco\\13.png')
pumpkin = pygame.transform.scale(pumpkin,(64,64))

tree=pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Resources\\Trees\\Tree.png')
tree = pygame.transform.scale(tree,(64,64))
sub_tile_dic = {
    'rock': [] #number 

}

fps_index = 0 # the frame we are on will count the time till we do all frames of animations for items and then reset to 0
frame_index = 0

sub_tile_map = [ #1 = foam, 3 = big water rock, 2 = med water rock, 4 = small water rock
    [0, 4, 0, 0, 4, 0, 0, 0, 0, 0],
    [0, 0, 2, 0, 2, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
]

top_tile_map = [ #1 = grass, 2 = bush, 3 = tree, 4 = small mushroom, 5 = small rock, 6 = bone, 7 = pumpkin
     #first list gives position for drawing, going from left to right, down to up
    [[0,1],[4]], 
    [[2,0],[5]],
    [[4,1],[6]],
    [[1,2],[2]],
    [[6,2],[7]]
]

def render_static(screen, item, pos):
    
    screen.blit(item,(pos[0]*64,380 - (pos[1]+1)*64))


def animate_render(screen,item,pos):
    
    global frame_index
    x = pos[0]*64
    y = 380 - (pos[1])*64#gives the top left cords of the grid going from down up 
    #animate the item 
    if item == grass:

        screen.blit(item,(x,y),(64*frame_index,0,64,64),(16, 0, 64, 64))
    else:
        screen.blit(item,(x,y),(64*frame_index,0,64,64))

    
def render_fore_decorations(screen):
     #for each thing render the item at the pos, if its a tree, render it as animated 
    
    for list in top_tile_map:
        for item in list[1]:#all the things to be drawn or animated in the second list of each row
            match item:
                case 1: 
                    render_static(screen,grass,list[0])
                case 2: 
                    render_static(screen,bush,list[0])

                case 4:
                    render_static(screen,mushroom,list[0])
                case 5:
                    render_static(screen,rock,list[0])
                case 6:
                    render_static(screen,bone,list[0])
                case 7:
                    render_static(screen,pumpkin,list[0])
       

    


def render_subtile_map(screen): #screen is 640 by 380
    global frame_index
    global fps_index
    row_index =0
    collum_index =0
    #if its time to animate the items, animate them and render them at their cords 
    
    
    #render things
    for row in sub_tile_map:
        for collum in row:
            if collum == 1 : #its foam
                animate_render(screen,foam,(collum_index,5-row_index))
            elif collum == 3:#big water rock
                animate_render(screen,big_water_rock,(collum_index,5-row_index))
            elif collum == 2: #med water rock
                animate_render(screen,med_water_rock,(collum_index,5-row_index))
            elif collum == 4: #small water cok
                animate_render(screen,small_water_rock,(collum_index,5-row_index))
            
            collum_index +=1

        collum_index = 0
        row_index +=1
    
    if fps_index%5 == 0: #we upadte animation one frame every 20 fps, so 1 animation takes 2 and 2/3 seconds to loop back
        #its an animation frame, so animate everything 
        frame_index +=1    
    if fps_index == 30:
        #we animated the 8th frame so loop back now
        fps_index = 0
        frame_index =0
        return
    
    fps_index+=1