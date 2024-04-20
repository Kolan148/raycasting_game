from settings import *
from world_map import world_map
import pygame
import math

class Player:
    def __init__(self, game):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.offset_angle = 0
        self.height = 0
        self.press = False
        self.jump = False
        self.duck = False
        self.map = False
        self.press2 = False
        self.sensitivity = 0.004
        self.weapon = "knife"
        self.i = 1
        self.t = 10
        self.game = game
        self.hp = 100
        self.frameCount = 0
        self.damage = 10
        self.ray = False
        self.ammos = {"knife":100000000,
                      "pist":50}
        self.dists = {"knife":40,
                      "pist":150,
                      "afto":200,
                      "rpg":500,
                      "gren":250}
        self.weapons = ["knife", "pist"]
        self.life = True
    @property
    def pos(self):
        return (self.x, self.y)
    def check_collision(self, dx, dy):
        if ((self.x+dx*6)//TILE, (self.y+dy*6)//TILE) in world_map:
            return True
        return False
    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        self.ray = False
        if self.life:
            if keys[pygame.K_w]:
                dx += player_speed * cos_a
                dy += player_speed * sin_a
            if keys[pygame.K_s]:
                dx += -player_speed * cos_a
                dy += -player_speed * sin_a
            if keys[pygame.K_a]:
                dx += player_speed * sin_a
                dy += -player_speed * cos_a
            if keys[pygame.K_d]:
                dx += -player_speed * sin_a
                dy += player_speed * cos_a
            if keys[pygame.K_SPACE] and not self.jump and not self.duck:
                self.height = 25
                self.jump=True
            if keys[pygame.K_LSHIFT] and not self.press:
                self.press = True
                self.duck = not self.duck
                if self.duck:
                    self.height = -10
                else:
                    self.height = 0
            elif not keys[pygame.K_LSHIFT]:
                self.press = False
            if self.jump and self.height > 0:
                self.height -= 1
                if self.height <= 0:
                    self.jump = False
            if keys[pygame.K_1] and "knife" in self.weapons:
                self.weapon = "knife"
                self.i = 1
                self.t = 10
                self.damage = 10
            if keys[pygame.K_2] and "pist" in self.weapons:
                self.weapon = "pist"
                self.i = 1
                self.t = 25
                self.damage = 15
            if keys[pygame.K_3] and "afto" in self.weapons:
                self.weapon = "afto"
                self.i = 1
                self.t = 10
                self.damage = 10
            if keys[pygame.K_5] and "gren" in self.weapons:
                self.weapon = "gren"
                self.i = 1
                self.t = 30
                self.damage = 100
            if keys[pygame.K_4] and "rpg" in self.weapons:
                self.weapon = "rpg"
                self.i = 1
                self.t = 50
                self.damage = 200
            pressed1 = pygame.mouse.get_pressed()[0]
            if pressed1 and self.frameCount%self.t==0 and self.ammos[self.weapon]>0:
                self.i += 1
                if self.i > 2:
                    self.i = 1
                    self.ray = True
                    self.ammos[self.weapon]-=1
            if not self.check_collision(dx, dy):
                self.x += dx
                self.y += dy
            if self.hp <= 0:
                self.life = False
                self.duck = True
        #if keys[pygame.K_LEFT]:
        #    self.angle -= 0.02
        #if keys[pygame.K_RIGHT]:
        #    self.angle += 0.02
        self.mouse_control()
        #self.angle %= math.pi*2
        self.frameCount += 1
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_m] and not self.press2:
            self.map = not self.map
            self.press2 = True
        elif not keys[pygame.K_m]:
            self.press2 = False
    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            differenceY = pygame.mouse.get_pos()[1] - HALF_HEIGHT
            pygame.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
            self.angle += difference * self.sensitivity
            self.offset_angle += differenceY*4* self.sensitivity
            #self.angle %= math.pi*2
