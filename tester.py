import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myID, game_map = hlt.get_init()
startdir = 0
        
#init
f = open("lastlog.log", 'w')
inits = []
ids = []
myStart = None
for s in game_map:
    if s.owner == myID:
        myStart = s
    if not s.owner in ids and s.owner != myID and s.owner != 0:
        ids.append(s.owner)
        inits.append(s)
closest = inits[0]
for n in inits[1:]:
    if game_map.get_distance(myStart, n) < game_map.get_distance(myStart, closest):
        closest = n

values = {}
for s in game_map:
    if abs(s.x - myStart.x) > 4 or abs(s.y - myStart.y) > 4:
        continue
    values[s] = s.production*30 - s.strength
targets = values.keys()
target = None
for s in targets:
    if target == None or values[s] > values[target]:
        target = s
f.write(str(target) + '\n')
global done
done = False
x = target.x
y = target.y
f.write("%d, %d\n" % (x, y))
f.close()

def move(s):
    if s.strength < s.production * 5:
        return Move(s, STILL)

    for d, n in enumerate(game_map.neighbors(s)):
        if s.strength > n.strength and n.owner != myID:
            return Move(s, d)

    side = 0
    dist = 0
    ns = game_map.neighbors(s)
    for d, n in enumerate(ns):
        ctr = 1
        strength = 0
        prod = 0
        while n.owner == myID and ctr < 45:
            ctr += 1
            n = game_map.get_target(n, d)
            strength = n.strength
            prod = n.production
        ctr -= prod/3
        ctr += strength/50
        if ctr < dist or dist == 0:
            dist = ctr
            side = d
    n = game_map.get_target(s, side)
    if n.owner != myID and n.strength > s.strength:
        return Move(s, STILL)
    return Move(s, side)

def move_early(s):
    global done
    if s.strength < s.production * 5:
        return Move(s, STILL)
    if s.x == x and s.y == y:
        done = True
    if done:
        return move(s)
    for d, n in enumerate(game_map.neighbors(s)):
        if game_map.get_distance(target, n) < game_map.get_distance(target, s):
            return Move(s, d)
    return move(s)

#execute
hlt.send_init("DistanceBot_selection")
framenum = 0
while True:
    game_map.get_frame()
    framenum += 1
    if done:
        moves = [move(s) for s in game_map if s.owner == myID]
    else:
        moves = [move_early(s) for s in game_map if s.owner == myID]        
    hlt.send_frame(moves)
