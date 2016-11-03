from maps import Map, Tile
from random import randint
import logging
from math import floor
import beastiary
from fighter import Fighter

logging.basicConfig(filename="example.log", level=logging.DEBUG)

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
  def __init__(self, maxX, maxY, things, player, max_residents=3):
    self.maxX = maxX
    self.maxY = maxY
    self.max_residents = max_residents
    self.map = Map(maxX, maxY)
    logging.info("maxX, maxY = %s, %s" % (str(maxX), str(maxY)))
    self.things = things
    self.player = player
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
    num = randint(0, self.max_residents)
    for n in range(num):
      x = randint(room.x1+1, room.x2-1)
      y = randint(room.y1+1, room.y2-1)
      
      if randint(0, 100) < 80:
        monster = beastiary.Monster(x, y,'o','orc','Orc','An Angry Orc',fighter_comp=Fighter(10,1))
      else:
        monster = beastiary.Monster(x,y,'T','troll','Troll','An Ugly Troll',fighter_comp=Fighter(30,2))
      self.things.append(monster)
      
  
  def create_map(self, min_size, max_size, max_rooms):
    rooms = []
    for r in range(max_rooms):
      w = randint(min_size, max_size)
      h = randint(min_size, max_size)
      x = randint(0, self.maxX - w - 1)
      y = randint(0, self.maxY - h - 1)
      new_room = Rect(x, y, w, h)
      logging.info("Room #%s" % str(r))
#      logging.info("x1 = %s" % str(x))
#      logging.info("y1 = %s" % str(y))
#      logging.info("x2 = %s" % str(x+w))
#      logging.info("y2 = %s" % str(y+h))
      
      failed = False
      if not failed:
        for other_room in rooms:
          if new_room.intersect(other_room):
            failed = True
            break
      
      if not failed:
        self.create_room(new_room)
        new_x, new_y = new_room.center()
        
        if len(rooms) == 0:
          self.player.x = int(floor(new_x))
          self.player.y = int(floor(new_y))
          
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
