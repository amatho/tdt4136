from queue import PriorityQueue
from typing import List, Optional


class AStar:
    def __init__(self, map_obj) -> None:
        self.map_obj = map_obj

    def find_path(self) -> "Node":
        open_nodes = PriorityQueue()

        # Create the start node
        start_pos = self.map_obj.get_start_pos()
        start_node = Node(self, State(
            start_pos[0], start_pos[1]), self.map_obj.get_cell_value(start_pos), None, [])

        open_nodes.put(start_node)

        # Loop until there are no open nodes left
        while not open_nodes.empty():
            node = open_nodes.get()

            # Check if the node is the goal
            goal_pos = self.map_obj.get_goal_pos()
            goal_state = State(goal_pos[0], goal_pos[1])
            if node.state == goal_state:
                break

            # Iterate through this node's successors
            successors = self.successors(node)
            for s in successors:
                # Return early if this successor is the goal
                if s.state == goal_state:
                    return s

                # Check if this successor already exists in the open nodes queue
                exists = any(n for n in open_nodes.queue if n.state == s.state)
                if exists:
                    s = next(filter(lambda n: n.state ==
                                    s.state, open_nodes.queue))

                node.children.append(s)

                if not exists:
                    open_nodes.put(s)
                # If the successor already existed but we found a better path, update it
                elif node.g + s.cost < s.g:
                    s.set_parent(node)

    # Generates all successors for parent, which means the nodes north, south, west, and east (if they are not walls)
    def successors(self, parent) -> List["Node"]:
        l = []

        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            next_state = State(parent.state.x + dx, parent.state.y + dy)
            cost = self.map_obj.get_cell_value(next_state.to_list())
            if cost != -1:
                # Create the node and set its parent
                node = Node(self, next_state, cost, parent, [])
                l.append(node)

        return l


# A node's state is uniquely defined by a 2D position on the map
class State:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def to_list(self) -> List[int]:
        return [self.x, self.y]

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y


# A node consists of a state, cost, parent, and children
class Node:
    def __init__(self, astar: AStar, state: State, cost: int, parent: Optional["Node"], children: List["Node"]) -> None:
        self.astar = astar
        self.state = state
        self.cost = cost
        self.children = children

        self.h = self.get_estimate()
        self.set_parent(parent)

    def set_parent(self, parent):
        self.parent = parent

        if self.parent is None:
            self.g = self.cost
        else:
            # Calculate the combined g using the parent's g
            self.g = self.cost + self.parent.g

        self.f = self.g + self.h

    def get_estimate(self) -> List[int]:
        return abs(self.astar.map_obj.get_goal_pos()[0] - self.state.x) + abs(self.astar.map_obj.get_goal_pos()[1] - self.state.y)

    def __str__(self) -> str:
        return f"Node <state: {self.state}, f: {self.f}, g: {self.g}, h: {self.h}>"

    def __lt__(self, obj) -> bool:
        return self.f < obj.f

    def __le__(self, obj) -> bool:
        return self.f <= obj.f

    def __eq__(self, obj) -> bool:
        return self.f == obj.f

    def __ne__(self, obj) -> bool:
        return self.f != obj.f

    def __gt__(self, obj) -> bool:
        return self.f > obj.f

    def __ge__(self, obj) -> bool:
        return self.f >= obj.f
