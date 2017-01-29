import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

myID, game_map = hlt.get_init()
hlt.send_init("DistanceBot_vanilla")

#f = open("lastlog.log", 'w')

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
        while n.owner == myID and (ctr < dist or dist == 0) and ctr < 30:
            ctr += 1
            n = game_map.get_target(n, d)
        if ctr < dist or dist == 0:
            dist = ctr
            side = d
    n = game_map.get_target(s, side)
    if n.owner != myID and n.strength > s.strength:
        return Move(s, STILL)
    return Move(s, side)

while True:
    game_map.get_frame()
    moves = [move(s) for s in game_map if s.owner == myID]
    hlt.send_frame(moves)

#f.close();
