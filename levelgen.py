from maps import Level
from random import randint
import logging
from math import floor
import beastiary
from player import Player

log = logging.getLogger(__name__)

class Rect():
    def __init__(self,x,y,w,h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1+self.x2)/2
        center_y = (self.y1+self.y2)/2
        return (center_x, center_y)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class MapGenerator:
    def __init__(self, maxX, maxY,game, time=0.0, max_residents=3):
        self.maxX = maxX
        self.maxY = maxY
        self.max_residents = max_residents
        self.game_instance = game
        self.map = Level(maxX, maxY)
        self.player = Player(0,0,self.map, self.game_instance)
        self.map.player = self.player
        self.map.add_monster(self.player)
        log.info("maxX, maxY = %s, %s" % (str(maxX), str(maxY)))
        self.create_map(6, 10, 30)

    def create_room(self,room):
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.map.lookup(x,y).unblock()

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(floor(x1), floor(x2)), max(floor(x1), floor(x2))+1):
            self.map.lookup(int(floor(x)),int(floor(y))).unblock()

    def create_v_tunnel(self, y1, y2, x):
        for y in range(int(floor(min(y1,y2))), int(floor(max(y1, y2)+1))):
            self.map.lookup(int(floor(x)),int(floor(y))).unblock()

    def place_things(self, room):
        num = randint(1, self.max_residents)
        for n in range(num):
            x = randint(room.x1+1, room.x2-1)
            y = randint(room.y1+1, room.y2-1)
            select = randint(0,1000)

            if select < 250:
                monster = beastiary.create_monster(x, y, self.game_instance,
                                                   beastiary.ORC)
            elif select > 250 and select < 450:
                monster = beastiary.create_monster(x, y, self.game_instance,
                                                   beastiary.HUMAN)
            elif select > 450 and select < 600:
                monster = beastiary.create_monster(x, y, self.game_instance,
                                                   beastiary.KOBOLD)
            elif select > 600 and select < 700:
                monster = beastiary.create_monster(x, y, self.game_instance,
                                                   beastiary.DWARF)
            elif select > 700 and select < 900:
                monster = beastiary.create_monster(x,y,self.game_instance,
                                                   beastiary.HOUND)
            else:
                monster = beastiary.create_monster(x, y, self.game_instance,
                                                  beastiary.TROLL)
            log.debug(str(monster))
            self.map.add_monster(monster)

    def create_map(self, min_size, max_size, max_rooms):
        rooms = []
        for r in range(max_rooms):
            w = randint(min_size, max_size)
            h = randint(min_size, max_size)
            x = randint(0, self.maxX - w - 1)
            y = randint(0, self.maxY - h - 1)
            new_room = Rect(x, y, w, h)

            failed = False
            if not failed:
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        failed = True
                        break

            if not failed:
                self.create_room(new_room)
                new_x, new_y = new_room.center()
                log.debug("Room: x1=%s, x2=%s, y1=%s, y2=%s" % (new_room.x1,
                                                                new_room.x2,
                                                                new_room.y1,
                                                                new_room.y2))

                if len(rooms) == 0:
                    self.player.x = floor(new_x)
                    self.player.y = floor(new_y)
                else:
                    prev_x, prev_y = rooms[len(rooms)-1].center()
                    self.place_things(new_room)
                    if randint(0,2) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)

                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                rooms.append(new_room)

if __name__ == "__main__":
    m = MapGenerator(40,40).map
    print(m.heatmap(m.player.x, m.player.y))
