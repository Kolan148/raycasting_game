import pygame as pg
from settings import *
from world_map import *


class SpriteObject:
    def __init__(self, game, x, y, scale, image):
        self.x = x * TILE
        self.y = y * TILE
        self.scale = scale
        self.image = image
        self.w = image.get_width()
        self.h = image.get_height()
        self.sc = game.screen
    def render(self, player, objects):
        dx = self.x - player.x
        dy = self.y - player.y
        theta = math.atan2(dy, dx)
        delta = theta - player.angle
        if dx > 0 and player.angle > math.pi:
            delta += math.tau
        delta_rays = delta / DELTA_ANGLE
        x = (NUM_RAYS/2 + delta_rays) * SCALE
        dist = math.hypot(dx, dy)
        norm_dist = dist * math.cos(delta)
        if -self.w/2 < x < (WIDTH - self.w/2) and norm_dist > 0.5:
            proj = SCREEN_DIST / norm_dist * self.scale
            proj_width = proj * (self.w/self.h)
            proj_height = proj
            y =HALF_HEIGHT - max(proj_height, 0.0001)/2 + 0.0
            #pg.draw.rect(self.sc, self.colour, (x, y, proj_width, proj_height))
            img = pg.transform.scale(self.image, (proj_width, proj_height))
            #self.sc.blit(img, (x, y))
            objects.append((dist, (x, y-player.offset_angle*SCALE+player.height*SCALE), img))


class Enemy:
    def __init__(self, game, x, y, scale, image, hp=100, speed=1, damage=2, dist=50):
        self.x = x * TILE
        self.y = y * TILE
        self.scale = scale
        self.image = image
        self.w = image[0].get_width()
        self.h = image[0].get_height()
        self.sc = game.screen
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.i = 0
        self.frameCount = 0
        self.dist = dist
        self.game = game
    def render(self, player, objects):
        dx = self.x - player.x
        dy = self.y - player.y
        theta = math.atan2(dy, dx)
        delta = theta - player.angle
        if dx > 0 and player.angle > math.pi:
            delta += math.tau
        delta_rays = delta / DELTA_ANGLE
        x = (NUM_RAYS/2 + delta_rays) * SCALE
        dist = math.hypot(dx, dy)
        norm_dist = dist * math.cos(delta)
        if -self.w/2 < x < (WIDTH - self.w/2) and norm_dist > 0.5:
            proj = SCREEN_DIST / norm_dist * self.scale
            proj_width = proj * (self.w/self.h)
            proj_height = proj
            y =HALF_HEIGHT - max(proj_height, 0.0001)/2 + 0.0
            #pg.draw.rect(self.sc, self.colour, (x, y, proj_width, proj_height))
            img = pg.transform.scale(self.image[self.i], (proj_width, proj_height))
            #self.sc.blit(img, (x, y))
            objects.append((dist, (x-img.get_width()/2, y-player.offset_angle*SCALE+player.height*SCALE), img))
    def check_collision(self, dx, dy):
        if (self.x+dx//TILE, self.y+dy//TILE) in world_map:
            return True
        return False
    def update(self, player):
        h = True
        for x, y in world_map:
            rect = pg.Rect(x*TILE, y*TILE, TILE, TILE)
            if rect.clipline((self.x, self.y, player.x, player.y)):
                h = False
                break
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)
        if h and dist > 5:
            dx, dy = 0, 0
            if self.x > player.x:
                dx -= self.speed
                self.i = 1
            else:
                dx += self.speed
                self.i = 1
            if self.y > player.y:
                dy -= self.speed
                self.i = 1
            else:
                dy += self.speed
                self.i = 1
        else:
            self.i = 0
        if dist < self.dist:
            if self.frameCount % 25 == 0:
                self.i = 2
                player.hp -= self.damage
                dx, dy = 0, 0
            else:
                self.i = 0
        if h and dist > 5:
            if not self.check_collision(dx, dy):
                self.x += dx
                self.y += dy
                if self.frameCount % 50 == 0:
                    self.image[1] = pg.transform.flip(self.image[1], True, False)
        #pg.draw.line(self.sc, (255, 255, 255), (self.x, self.y-5), (player.x, player.y-5), 3)
        self.frameCount += 1
        if player.ray and dist <= player.dists[player.weapon]:
            rect = pg.Rect(self.x, self.y, 25, 25)
            if rect.clipline((player.x, player.y, player.x + WIDTH * math.cos(player.angle), player.y + WIDTH * math.sin(player.angle))):
                self.hp -= player.damage
        if self.hp <= 0 :
            del self.game.enemys[self.game.enemys.index(self)]

class Item:
    def __init__(self, game, x, y, scale, image, type_="health", num=52):
        self.x = x * TILE
        self.y = y * TILE
        self.scale = scale
        self.image = image
        self.w = image.get_width()
        self.h = image.get_height()
        self.sc = game.screen
        self.type_ = type_
        self.num = num
        self.game = game
    def render(self, player, objects):
        dx = self.x - player.x
        dy = self.y - player.y
        theta = math.atan2(dy, dx)
        delta = theta - player.angle
        if dx > 0 and player.angle > math.pi:
            delta += math.tau
        delta_rays = delta / DELTA_ANGLE
        x = (NUM_RAYS/2 + delta_rays) * SCALE
        dist = math.hypot(dx, dy)
        norm_dist = dist * math.cos(delta)
        if -self.w/2 < x < (WIDTH - self.w/2) and norm_dist > 0.5:
            proj = SCREEN_DIST / norm_dist * self.scale
            proj_width = proj * (self.w/self.h)
            proj_height = proj
            y =HALF_HEIGHT - max(proj_height, 0.0001)/2 + 0.0
            #pg.draw.rect(self.sc, self.colour, (x, y, proj_width, proj_height))
            img = pg.transform.scale(self.image, (proj_width, proj_height))
            #self.sc.blit(img, (x, y))
            objects.append((dist, (x-img.get_width()/2, y-player.offset_angle*SCALE+player.height*SCALE), img))
    def check_collision(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        dist = math.hypot(dx, dy)
        if dist < 10:
            return True
        return False
    def update(self, player):
        if self.check_collision(player):
            if self.type_ == "health":
                player.hp += self.num
            elif self.type_ == "afto":
                if not "afto" in player.weapons:
                    player.weapons.append("afto")
                    player.ammos["afto"] = 25
                else:
                    player.ammos["afto"] += 25
            elif self.type_ == "gren":
                if not "gren" in player.weapons:
                    player.weapons.append("gren")
                    player.ammos["gren"] = 1
                else:
                    player.ammos["gren"] += 1
            elif self.type_ == "rpg":
                if not "rpg" in player.weapons:
                    player.weapons.append("rpg")
                    player.ammos["rpg"] = 1
                else:
                    player.ammos["rpg"] += 2
            elif self.type_ == "pist_ammo":
                player.ammos["pist"] += self.num
            elif self.type_ == "afto_ammo":
                if "afto" in player.weapons:
                    player.ammos["afto"] += self.num
            elif self.type_ == "rpg_ammo":
                if "rpg" in player.wepaons:
                    player.ammos["rpg"] += self.num
            del self.game.items[self.game.items.index(self)]



class Soldier(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 52, game.sprites1["sold"], hp=100, speed=1, damage=5, dist=75)
class Heavy(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 52, game.sprites1["heav"], hp=200, speed=0.75, damage=10, dist=100)
class Power(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 52, game.sprites1["powe"], hp=400, speed=0.5, damage=20, dist=150)


class Aptechka(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["apte"], type_="health", num=75)

class Afto(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["afto"], type_="afto", num=1)

class Grenade(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["gren"], type_="gren", num=1)

class Rpg(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["rpg"], type_="rpg", num=1)

class PistAmmo(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["piam"], type_="pist_ammo", num=15)

class AftoAmmo(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["afam"], type_="afto_ammo", num=25)

class RpgAmmo(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 25, game.sprites1["rpam"], type_="rpg_ammo", num=1)
