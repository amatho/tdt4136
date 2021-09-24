from io import open_code
from queue import PriorityQueue
from typing import Iterable, List, Optional


class AStar:
    def __init__(self, map_obj) -> None:
        self.map_obj = map_obj

    def path(self) -> "Node":
        open_nodes = PriorityQueue()
        closed_nodes = []
        start_pos = self.map_obj.get_start_pos()
        start_node = Node(self, State(
            start_pos[0], start_pos[1]), self.map_obj.get_cell_value(start_pos), None, [])
        open_nodes.put(start_node)

        while not open_nodes.empty():
            node = open_nodes.get()

            goal_pos = self.map_obj.get_goal_pos()
            goal_state = State(goal_pos[0], goal_pos[1])
            if node.state == goal_state:
                break

            successors = self.successors(node)
            for s in successors:
                if s.state == goal_state:
                    return s

                exists = any(n for n in open_nodes.queue if n.state == s.state)
                if exists:
                    s = next(filter(lambda n: n.state ==
                             s.state, open_nodes.queue))

                node.children.append(s)

                if not exists:
                    open_nodes.put(s)
                elif node.g + s.cost < s.g:
                    s.parent = node
                    s.g = node.g + s.cost
                    s.f = s.g + s.h

            closed_nodes.append(node)

    def successors(self, parent) -> List["Node"]:
        l = []

        for dx, dy in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            next_state = State(parent.state.x + dx, parent.state.y + dy)
            cost = self.map_obj.get_cell_value(next_state.to_list())
            if cost != -1:
                node = Node(self, next_state, cost, parent, [])
                l.append(node)

        return l


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


class Node:
    def __init__(self, astar: AStar, state: State, cost: int, parent: Optional["Node"], children: List["Node"]) -> None:
        self.astar = astar
        self.state = state
        self.cost = cost
        self.parent = parent
        self.children = children
        self.open = True

        if parent is None:
            self.g = cost
        else:
            self.g = cost + parent.g

        self.h = self.get_estimate()
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


def iter_is_empty(iter: Iterable) -> bool:
    try:
        next(iter)
    except StopIteration:
        return True
    else:
        return False
