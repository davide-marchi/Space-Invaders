import pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

import random
import time
import g2d_pyg as g2d
from actor import *


class Invader(Actor):
    def __init__(self, x: int, y: int, dx: int, maxL: int, maxR: int, sprites: int()):
        self._x = x
        self._y = y
        self._dx = dx
        self._maxL = maxL
        self._maxR = maxR
        self._w = 52    ##
        self._h = 32    ##
        self._sprites = sprites
        
    def move(self):
        if self._maxL <= self._x + self._dx <= self._maxR - self._w:
            self._x += self._dx
        else:
            self._dx = -self._dx
            self._y = self._y + abs(self._dx)
            if self._y >= arena._h-160-32:
                arena.remove(cannone)

        if random.randint(0, 10*len(arena._actors)) == 0:
            arena.add(Bomba(arena, self._x+20, self._y+self._h))

    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._w, self._h

    def collide(self, other):
        pass

    def symbol(self) -> (int, int, int, int):
        global nUpdate
        #print(nUpdate)
        if int(nUpdate%30) < 15:
            return int(self._sprites[0]), int(self._sprites[1]), self._w/2, self._h/2
        else:
            return int(self._sprites[2]), int(self._sprites[3]), self._w/2, self._h/2


class Cannon(Actor):
    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 28, 32    ##
        self._speed = 4
        self._dx, self._dy = 0, 0
        self._arena = arena
        self.sparo = 0
        arena.add(self)
        
    def move(self):
        arena_w, arena_h = self._arena.size()

        self._x += self._dx
        if self._x < 120:
            self._x = 120
        elif self._x > arena_w - (self._w + 120):
            self._x = arena_w - (self._w + 120)

    def go_left(self):
        self._dx = -self._speed
        
    def go_right(self):
        self._dx = +self._speed
        
    def stay(self):
        self._dx, self._dy = 0, 0

    def shoot(self):
        if (nUpdate-self.sparo)>20:
            self._arena.add(Missile(self._arena, self._x+12, self._y-28))##
            self.sparo = nUpdate

    def position(self):
        return self._x, self._y, self._w, self._h
    
    def collide(self, other):
        self._arena.remove(self)

    def symbol(self) -> (int, int, int, int):
        return 195, 626, self._w/2, self._h/2


class Shield(Actor):
    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 62, 32
        self._arena = arena
        arena.add(self)

    def move(self):
        pass

    def position(self):
        return self._x, self._y, self._w, self._h
    
    def collide(self, other):
        self._arena.remove(other)
        self._arena.remove(self)

    def symbol(self) -> (int, int, int, int):
        return 223, 617, self._w/2, self._h/2


class Missile(Actor):
    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 4, 28    ##
        self._speed = 8
        self._dy = 0
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y -= self._speed
        
        if self._y < 0:
            self._arena.remove(self)

    def position(self):
        return self._x, self._y, self._w, self._h
    
    def collide(self, other):
        self._arena.remove(other)
        self._arena.remove(self)

    def symbol(self) -> (int, int, int, int):
        return 202, 604, self._w/2, self._h/2    ##


class Bomba(Actor):
    def __init__(self, arena, x, y):
        self._x, self._y = x, y
        self._w, self._h = 12, 24    ##
        self._speed = 8
        self._dy = 0
        self._arena = arena
        arena.add(self)

    def move(self):
        arena_w, arena_h = self._arena.size()
        self._y += self._speed

        if self._y > arena._h:
            self._arena.remove(self)

    def position(self):
        return self._x, self._y, self._w, self._h
    
    def collide(self, other):
        pass

    def symbol(self) -> (int, int, int, int):
        global nUpdate
        #print(nUpdate)
        if int(nUpdate%10) < 5:
            return 172, 607, self._w/2, self._h/2
        else:
            return 172, 628, self._w/2, self._h/2


def keydown(code: str):
    if code == "ArrowRight":
        cannone.go_right()
    elif code == "ArrowLeft":
        cannone.go_left()
    elif code == "Space":
        cannone.shoot()
    
def keyup(code: str):
    if code == "ArrowRight" or code == "ArrowLeft":
        cannone.stay()

def update():
    g2d.fill_canvas((0, 0, 0))
    nemici = False
    giocatore = False
    if any(isinstance(item, Cannon) for item in arena.actors()):
        giocatore = True
    if any(isinstance(item, Invader) for item in arena.actors()):
        nemici = True
    
    if giocatore and nemici:
        global nUpdate
        nUpdate += 1
        arena.move_all()
        for a in arena._actors:
            g2d.draw_image_clip(img, a.position(), a.symbol())
    elif not giocatore and nemici:
        g2d.draw_image_clip(g2d.load_image("GameOver.png"), (120, 120, 528, 432), (300, 0, 1320, 1080))
        #g2d.draw_text("GAME OVER!", (255, 255, 255), (arena._w/5, arena._h/2-50), 75)
    else:
        g2d.draw_image_clip(g2d.load_image("WellDone.png"), (120, 120, 528, 432), (300, 0, 1320, 1080))
        #g2d.draw_text("YOU WIN!", (255, 255, 255), (arena._w/5, arena._h/2-50), 75)
    g2d.draw_image_clip(img, (0, 0, arena._w, arena._h), (6, 991, 256, 224))
    
        

def main():
    g2d.init_canvas((arena._w, arena._h))
    g2d.play_audio(msc, True)
    g2d.handle_keyboard(keydown, keyup)
    g2d.main_loop(update, 1000 // 30)


rows = int(4)       #
cols = int(6)       #

nUpdate = int(0)

img = g2d.load_image("invaders-transp.png")
msc = g2d.load_audio("Music.ogg")

arena = Arena(768, 672)

sprites = [(9, 601, 49, 601), (9, 631, 49, 631), (87, 604, 127, 604), (86, 630, 128, 630)]

for k in range(0, rows):
    for i in range(0, cols):
        arena.add(Invader(140+i*72, 125+k*62, 3, 140+i*72, (arena._w-120)-72*(cols-i)+52, sprites[k]))

cannone = Cannon(arena, int(arena._w/2-14), arena._h-160)

shield1 = Shield(arena, 120+(528-62*3)/4, arena._h-230)
shield2 = Shield(arena, 120+((528-62*3)/4)*2+62, arena._h-230)
shield3 = Shield(arena, 120+((528-62*3)/4)*3+62*2, arena._h-230)
        
main()
