import pygame
from settings import *
from world_map import *

def ray_casting(sc, player_pos, player_angle, textures, offset_angle, height):
    cur_angle = player_angle - HALF_FOV
    xo, yo = player_pos
    objects = []
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        depth = 0
        step = TILE
        while depth < MAX_DEPTH:
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            #pygame.draw.line(sc, WHITE, player_pos, (x, y), int(step/100))
            if (x // TILE, y // TILE) in world_map:
                if step < 2:
                    depth *= math.cos(player_angle - cur_angle)
                    proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)
                    offset = ((x/TILE-int(x/TILE))+(y/TILE-int(y/TILE)))/2
                    #if offset >= 1 or offset == 0:
                    #    offset = y/TILE-int(y/TILE)
                    #print(offset > 1)
                    texture = text_map[int(y//TILE)][int(x//TILE)]
                    wall_column = textures[texture].subsurface(offset*100, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
                    wall_column = pygame.transform.scale(wall_column, (SCALE, abs(proj_height)))
                    #sc.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
                    objects.append((depth, (ray * SCALE, HALF_HEIGHT - proj_height // 2-offset_angle*SCALE+height*SCALE), wall_column))
                    break
                else:
                    depth -= step
                    step /= 2
            depth += step
        cur_angle += DELTA_ANGLE
    return objects
