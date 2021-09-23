from astar import AStar
from Map import Map_Obj

map = Map_Obj()
astar = AStar(map)

print(astar.path())
