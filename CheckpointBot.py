import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myID, game_map = hlt.get_init()
        
#init
global checkpoints
checkpoints = []
for s in game_map:
    value = s.production * 30 - s.strength
    if value > 150:
        checkpoints.append(s)
for s in checkpoints:
    for sq in checkpoints:
        if game_map.get_distance(s, sq) < 4 and s != sq:
            checkpoints.remove(s)
            break

def move(s):
    if s.strength < s.production*5:
        return Move(s, STILL)
    global checkpoints
    closest = None
    d = 0
    for sq in checkpoints:
        dist = game_map.get_distance(s, sq)
        if closest == None or (dist < d and sq.owner != myID):
            closest = sq
            d = dist
    if closest == None or d > 8:
        return move_expand(s)
    return move_target(s, closest)

def move_target(s, s2):
    closest = s
    d = game_map.get_distance(s, s2)
    ret = 0
    for r, n in enumerate(game_map.neighbors(s)):
        dist = game_map.get_distance(n, s2)
        if dist <= d and (n.strength < closest.strength or closest == s):
            closest = n
            d = dist
            ret = r
    return Move(s, ret)

def move_expand(s):
    return Move(s, random.choice((NORTH, SOUTH, WEST, EAST, STILL)))
    
#execute
hlt.send_init("DistanceBot_fighter")
while True:
    game_map.get_frame()
    moves = [move(s) for s in game_map if s.owner == myID]
    hlt.send_frame(moves)
