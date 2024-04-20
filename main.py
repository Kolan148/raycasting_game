#Black Squad
from settings import *
from player import Player
import math
from world_map import world_map
from raycasting import ray_casting
from sprite import *
import pygame as pg


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.mouse.set_visible(False)
        pg.display.set_caption("Black squad")

        self.clock = pg.time.Clock()

        self.player = Player(self)
        #Wepaons
        self.weapons = {
            "knife1":pg.image.load("img/weapons/knife.png").convert_alpha(),
            "knife2":pg.image.load("img/weapons/knife2.png").convert_alpha(),
            "pist1":pg.image.load("img/weapons/pist.png").convert_alpha(),
            "pist2":pg.image.load("img/weapons/pist2.png").convert_alpha(),
            "afto1":pg.image.load("img/weapons/afto.png").convert_alpha(),
            "afto2":pg.image.load("img/weapons/afto2.png").convert_alpha(),
            "gren1":pg.image.load("img/weapons/grenade.png").convert_alpha(),
            "gren2":pg.image.load("img/weapons/grenade2.png").convert_alpha(),
            "rpg1":pg.image.load("img/weapons/rpg.png").convert_alpha(),
            "rpg2":pg.image.load("img/weapons/rpg2.png").convert_alpha(),
        }
        #TEXTURES

        self.textures = {
            '1':pg.image.load("img/textures/brick1.jpg").convert_alpha(),
            '2':pg.image.load("img/textures/wall1.jpg").convert_alpha(),
            '3':pg.image.load("img/textures/brick2.jpg").convert_alpha(),
            '4':pg.image.load("img/textures/logo.jpg").convert_alpha(),
            'P':pg.image.load("img/textures/pricel.png").convert_alpha(),
            'S':pg.image.load("img/textures/sky.jpg")
        }

        #Sprites
        self.sprites1 = {'cust':pg.image.load("img/sprites/items/custodes.png").convert_alpha(),
                         'apte':pg.image.load("img/sprites/items/aptechka.png").convert_alpha(),
                         'afto':pg.image.load("img/sprites/items/afto.png").convert_alpha(),
                         'gren':pg.image.load("img/sprites/items/grenade.png").convert_alpha(),
                         'piam':pg.image.load("img/sprites/items/pist_ammo.png").convert_alpha(),
                         'afam':pg.image.load("img/sprites/items/afto_ammo.png").convert_alpha(),
                         'rpg':pg.image.load("img/sprites/items/rpg.png").convert_alpha(),
                         'rpam':pg.image.load("img/sprites/items/rpg_ammo.png").convert_alpha(),
                         'sold':[pg.image.load("img/sprites/enemys/soldier_idle.png").convert_alpha(),
                                 pg.image.load("img/sprites/enemys/soldier_walk.png").convert_alpha(),
                                 pg.image.load("img/sprites/enemys/soldier_attack.png").convert_alpha()],
                         'heav':[pg.image.load("img/sprites/enemys/heavy_idle.png").convert_alpha(),
                                 pg.image.load("img/sprites/enemys/heavy_walk.png").convert_alpha(),
                                 pg.image.load("img/sprites/enemys/heavy_attack.png").convert_alpha()],
                         'powe':[pg.image.load("img/sprites/enemys/power_idle.png").convert_alpha(),
                                 pg.image.load("img/sprites/enemys/power_walk.png").convert_alpha(),
                                 pg.image.load("img/sprites/enemys/power_attack.png").convert_alpha()]
                         }
        self.sprites = [SpriteObject(self, 1.5, 1.5, 52, self.sprites1["cust"])]
        self.enemys = [Soldier(self, 9.5, 1.5),
                       Soldier(self, 10.5, 2.5),
                       Heavy(self, 9.5, 4.5),
                       Heavy(self, 9.5, 6.5),
                       Power(self, 2.5, 2.5)
                       ]
        self.items = [Aptechka(self, 10.5, 1.5),
                      Afto(self, 10, 4.5),
                      AftoAmmo(self, 10.5, 5.5),
                      Aptechka(self, 4.5, 6.5),
                      Rpg(self, 4, 6.5),
                      Grenade(self, 3.6, 6.5),
                      Grenade(self, 3.3, 6.5)]
        #Font
        self.font = pg.font.SysFont('Calibri', 30, 0, 0)
        self.font2 = pg.font.SysFont('Calibri', 60, 0, 0)
        self.font3 = pg.font.SysFont('Calibri', 90, 0, 0)
        #Delta time
        self.t = 0
        self.dt = 0
        self.count = 0
        print(self.textures['S'].get_width(), self.textures['S'].get_height())
    def sort(self, arr):
        arr2 = arr
        for x in range(len(arr)-1):
            for i in range(len(arr)-1):
                if arr2[i][0] < arr2[i+1][0]:
                    temp = arr[i+1]
                    arr2[i+1] = arr[i]
                    arr2[i] = temp
        return arr2
    def draw_objects(self, objects):
        for obj in objects:
            self.screen.blit(obj[2], obj[1])
    def run(self):
        while 1:
            [quit() for event in pg.event.get() if event.type == pg.QUIT]
            self.player.movement()
            self.screen.fill((0, 0, 0))
            #pg.draw.rect(self.screen, BLUE, (0, 0, WIDTH, HALF_HEIGHT))
            pg.draw.rect(self.screen, DARKGRAY, (0, 0, WIDTH, HEIGHT))
            sky_offset = -5 * math.degrees(self.player.angle) % WIDTH
            self.screen.blit(self.textures['S'], (sky_offset, (-self.player.offset_angle*SCALE+self.player.height*SCALE)-850))
            self.screen.blit(self.textures['S'], (sky_offset - WIDTH, (-self.player.offset_angle*SCALE+self.player.height*SCALE)-850))
            self.screen.blit(self.textures['S'], (sky_offset + WIDTH, (-self.player.offset_angle*SCALE+self.player.height*SCALE)-850))
            objects = ray_casting(self.screen, self.player.pos, self.player.angle, self.textures, self.player.offset_angle, self.player.height)
            [sprite.render(self.player, objects) for sprite in self.sprites]
            for enemy in self.enemys:
                enemy.render(self.player, objects)
                enemy.update(self.player)
            for item in self.items:
                item.render(self.player, objects)
                item.update(self.player)
            objects = self.sort(objects)
            self.draw_objects(objects)
            self.screen.blit(self.weapons[self.player.weapon+str(self.player.i)], (400+math.sin(self.count), 300+math.cos(self.count)))#-math.cos(self.dt*0.01)*150))
            self.screen.blit(self.textures['P'], (HALF_WIDTH-25, HALF_HEIGHT-25))
            if self.player.map:
                pg.draw.circle(self.screen, GREEN, (int(self.player.x), int(self.player.y)), 12)
                pg.draw.line(self.screen, GREEN, self.player.pos, (self.player.x + WIDTH * math.cos(self.player.angle),
                                                          self.player.y + WIDTH * math. sin(self.player.angle)), 2)
                for enemy in self.enemys:
                    pg.draw.line(self.screen, RED, self.player.pos, (int(enemy.x), int(enemy.y)), 2)
                    pg.draw.circle(self.screen, RED, (int(enemy.x), int(enemy.y)), 12)
                for item in self.items:
                    pg.draw.circle(self.screen, YELLOW, (int(item.x), int(item.y)), 12)
                for x,y in world_map:
                     pg.draw.rect(self.screen, WHITE, (x*TILE, y*TILE, TILE, TILE), 2)
            text = self.font.render(f'FPS:{int(self.clock.get_fps())}', 0, pg.Color('forestgreen'))
            self.screen.blit(text, (0, 0))
            text = self.font2.render(f'+{self.player.hp}', 0, pg.Color('red'))
            self.screen.blit(text, (0, 700))
            text = self.font2.render(f'|{self.player.ammos[self.player.weapon]}', 0, pg.Color('yellow'))
            self.screen.blit(text, (1000, 700))
            #self.screen.blit(self.weapons[self.player.weapon+str(self.player.i)], (400+math.sin(self.count), 300+math.cos(self.count)))#-math.cos(self.dt*0.01)*150))
            if not self.player.life:
                text = self.font3.render('YOU DIE', 0, pg.Color('red'))
                self.screen.blit(text, (HALF_WIDTH-100, HALF_HEIGHT-50))
            pg.display.flip()
            self.dt = self.clock.tick(60)
            self.count += 0.1
if __name__ == "__main__":
    app = Game()
    app.run()
