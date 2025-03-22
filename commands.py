import pygame

# all of the sprites are loaded in while the banner is resized to fit the screen
grass = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Ground\\Tilemap_Flat.png')
banner = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Banners\\Banner_Connection_Up.png')
banner = pygame.transform.scale(banner, (64,64))
bridge = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Bridge\\Bridge_All.png')

# 10 * 5.625 64 pixel squares
# the tile map shows the program where to draw everything and is inverted both horizontaly and verticaly
tile_map = [
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 3, 3, 3]
]

# go through bit map and blit images to screen
def render_forground(screen):
    # HEIGHT is 360 and WIDTH is 640
    row_num = 0
    for row in tile_map:
        collum_num = 0
        row_num += 1
        for collum in row:
            collum_num += 1
            # 2 is the placeable ground
            if collum == 2:
                # crop height and width is to change the sprite for the edges of the island
                crop_height = 0
                crop_width = 128
                if row_num != 3: crop_height = 64
                if collum_num != 4: crop_width = 64
                screen.blit(grass, (640-64*collum_num, 360-64*row_num), (crop_width, crop_height, 64, 64))
            # 1 is the bridge goblins run across
            if collum == 1:
                # if the bridge is at the end of the row it has poles in the sprite
                if collum_num == 3:
                    screen.blit(bridge, (640-64*collum_num, 360-64*row_num), (16, 0, 64, 64))
                else:
                    screen.blit(bridge, (640-64*collum_num, 360-64*row_num), (64, 0, 64, 64))
            # 3 is a place holder for the shop ui
            if collum == 3:
                screen.blit(banner, (640-64*collum_num, 328-64*row_num), (0, 0, 64, 64))

# this iterating through the images of an animation where all sprites are on one png
def frame_count_check(fx, fy, ff, fy_min, fy_max):
    # the frame count is updated
    ff += 1
    # the sprite is changed every 6 frames
    if ff >= 6:
        ff = 0
        fx += 1
    # if the image is the last image in the row, the row is moved down and the collum is set to the beginning
    if fx > 5:
        fx = 0
        fy += 1
        if fy > fy_max:
            fy = fy_min
            # the frame that the image is set back to the beginning it returns true alongside the updated values
            return fx, fy, ff, True
    return fx, fy, ff, False