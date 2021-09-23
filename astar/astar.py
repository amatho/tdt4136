from io import open_code
from queue import PriorityQueue


class AStar:
    def __init__(self, map_obj) -> None:
        self.map_obj = map_obj

    def path(self):
        open_nodes = PriorityQueue()
        closed_nodes = []
        start_pos = self.map_obj.get_start_pos()
        start_node = Node(self, State(
            start_pos[0], start_pos[1]), self.map_obj.get_cell_value(start_pos), None, None)
        open_nodes.put(start_node)

        while not open_nodes.empty():
            print(open_nodes.queue)
            node = open_nodes.get()

            goal_pos = self.map_obj.get_goal_pos()
            goal_state = State(goal_pos[0], goal_pos[1])
            if node.state == goal_state:
                break

            successors = self.successors(node)
            for s in successors:
                if s.state == goal_state:
                    return s

                if s.state in map(lambda n: n.state, open_nodes.queue) and next(filter(lambda n: n.f < s.f, open_nodes.queue)) is not None:
                    continue
                elif s.state in map(lambda n: n.state, closed_nodes) and next(filter(lambda n: n.f < s.f, closed_nodes)) is not None:
                    continue
                else:
                    print(s)
                    open_nodes.put(s)

            closed_nodes.append(node)

    def successors(self, parent):
        l = []

        for dx, dy in [[0, 1], [0, -1], [1, 0], [1, -1]]:
            next_state = State(parent.state.x + dx, parent.state.y + dy)
            cost = self.map_obj.get_cell_value(next_state.to_list())
            if cost != -1:
                node = Node(self, next_state, cost, parent, None)
                l.append(node)

        return l


class State:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def to_list(self):
        return [self.x, self.y]


class Node:
    def __init__(self, astar, state, cost, parent, children) -> None:
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

    def get_estimate(self):
        return [abs(self.astar.map_obj.get_goal_pos()[0] - self.state.x),
                abs(self.astar.map_obj.get_goal_pos()[1] - self.state.y)]

    def __lt__(self, obj):
        return self.f < obj.f

    def __le__(self, obj):
        return self.f <= obj.f

    def __eq__(self, obj):
        return self.f == obj.f

    def __ne__(self, obj):
        return self.f != obj.f

    def __gt__(self, obj):
        return self.f > obj.f

    def __ge__(self, obj):
        return self.f >= obj.f
