import pygame

grass = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Ground\\Tilemap_Flat.png')
banner = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\UI\\Banners\\Banner_Connection_Up.png')
banner = pygame.transform.scale(banner, (64,64))
bridge = pygame.image.load('Tiny Swords\\Tiny Swords (Update 010)\\Terrain\\Bridge\\Bridge_All.png')

# 10 * 5.625
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
            if collum == 2:
                crop_height = 0
                crop_width = 128
                if row_num != 3: crop_height = 64
                if collum_num != 4: crop_width = 64
                screen.blit(grass, (640-64*collum_num, 360-64*row_num), (crop_width, crop_height, 64, 64))
            if collum == 1:
                if collum_num == 3:
                    screen.blit(bridge, (640-64*collum_num, 360-64*row_num), (16, 0, 64, 64))
                else:
                    screen.blit(bridge, (640-64*collum_num, 360-64*row_num), (64, 0, 64, 64))

def frame_count_check(fx, fy, ff, fy_min, fy_max):
    ff += 1
    if ff > 5:
        ff = 0
        fx += 1
    if fx > 5:
        fx = 0
        fy += 1
        if fy > fy_max:
            fy = fy_min
            return fx, fy, ff, True
    return fx, fy, ff, False