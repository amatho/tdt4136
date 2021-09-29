from astar import AStar
from Map import Map_Obj


# Apply the path found to the map by recursively visiting each parent node
def apply_path(astar, node):
    pos = node.state
    val = astar.map_obj.str_map[pos.x][pos.y]
    if not (val == ' S ' or val == ' G '):
        astar.map_obj.str_map[pos.x][pos.y] = -2

    if node.parent is not None:
        apply_path(astar, node.parent)


def main():
    task = int(input("Enter the number of the task to run: "))
    map = Map_Obj(task=task)
    astar = AStar(map)

    node = astar.find_path()
    apply_path(astar, node)
    astar.map_obj.show_map()


if __name__ == "__main__":
    main()
