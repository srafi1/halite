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
    global framenum
    if s.strength < s.production * 5:
        return Move(s, STILL)

    for d, n in enumerate(game_map.neighbors(s)):
        if s.strength > n.strength and n.owner != myID:
            return Move(s, d)

    side = 0
    dist = None
    ns = game_map.neighbors(s)
    for d, n in enumerate(ns):
        ctr = 1
        strength = 0
        prod = 0
        enemy = False
        while n.owner == myID and ctr < 45:
            ctr += 1
            n = game_map.get_target(n, d)
            strength = n.strength
            prod = n.production
            enemy = n.owner != 0 and n.owner != myID
        if framenum < 100:
            ctr -= prod/3
            ctr += strength/50
        else:
            ctr -= prod/2
            ctr += strength/70            
        if enemy:
            ctr -= 2
        if dist == None or ctr < dist:
            dist = ctr
            side = d
    n = game_map.get_target(s, side)
    if n.owner != myID and n.strength > s.strength:
        return Move(s, STILL)
    return Move(s, side)

def move_early(s):
    global done
    if s.x == x and s.y == y:
        done = True
    if done:
        return move(s)
    go = 0
    t = None
    wait = 15
    for d, n in enumerate(game_map.neighbors(s)):
        if game_map.get_distance(target, n) < game_map.get_distance(target, s):
            if t != None and t.strength < n.strength:
                continue
            go = d
            t = n
            if n.owner == myID:
                wait = 5
    if t.strength < s.strength and t.owner != myID:
        return Move(s, go)
    if s.strength < s.production * wait:
        return Move(s, STILL)
    return Move(s, go)

#execute
hlt.send_init("DistanceBot_fighter")
global framenum
framenum = 0
while True:
    global framenum
    game_map.get_frame()
    framenum += 1
    if done:
        moves = [move(s) for s in game_map if s.owner == myID]
    else:
        moves = [move_early(s) for s in game_map if s.owner == myID]        
    hlt.send_frame(moves)
