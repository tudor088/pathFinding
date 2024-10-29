import pygame
from queue import PriorityQueue
from collections import deque
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    count = 0
    while current in came_from:
        current = came_from[current]
        print("({}, {})".format(current.row, current.col))
        count += 1
        current.make_path()
        draw()

    print("Total length: {}".format(count))


def reconstruct_path_DFSBFS(came_from, current, draw):
    count = -1
    while current is not None:  # Continue until current is None
        print("({}, {})".format(current.row, current.col))  # Print the current node position
        current.make_path()  # Mark the current node as part of the path
        count += 1  # Increment count
        current = came_from.get(current)  # Move to the parent
        draw()

    print("Total length: {}".format(count))  # Print total length


def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    # The g_score of each node is set to infinity initially, except the start node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}  # Keep track of items in the priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Get the current node from the priority queue
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:  # Path found, reconstruct it
            reconstruct_path(came_from, end, draw)
            return True

        # Explore each neighbour of the current node
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1  # Dijkstra's increments cost by 1 per move

            if temp_g_score < g_score[neighbour]:  # A shorter path to neighbour is found
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False  # No path found


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def bfs(draw, grid, start, end):
    queue = deque([start])  # Initialize the queue with the start node
    came_from = {start: None}  # To reconstruct the path

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()  # Dequeue the first element

        # Check if we've reached the end node
        if current == end:
            reconstruct_path_DFSBFS(came_from, end, draw)
            return True

        for neighbour in current.neighbours:
            if neighbour not in came_from:  # Check if it has been visited
                queue.append(neighbour)  # Enqueue the neighbor
                came_from[neighbour] = current  # Set the current node as the parent
                neighbour.make_open()  # Mark it as open

        draw()

        if current != start:
            current.make_closed()

    return False



def dfs(draw, grid, start, end):
    stack = [start]  # Initialize the stack with the start node
    came_from = {start: None}  # To reconstruct the path

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()  # Pop the last element (LIFO)

        # Check if we've reached the end node
        if current == end:
            reconstruct_path_DFSBFS(came_from, end, draw)
            return True

        for neighbour in current.neighbours:
            if neighbour not in came_from:  # Check if it has been visited
                stack.append(neighbour)  # Push the neighbor onto the stack
                came_from[neighbour] = current  # Set the current node as the parent
                neighbour.make_open()  # Mark it as open

        draw()

        if current != start:
            current.make_closed()

    return False




def ucs(draw, grid, start, end):
    # Priority queue to store the nodes to be explored, initialized with the start node
    open_set = PriorityQueue()
    open_set.put((0, start))  # (cost, node)

    came_from = {}
    cost_so_far = {start: 0}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_cost, current = open_set.get()

        # Check if we've reached the end node
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            # Calculate the cost to reach the neighbor
            new_cost = cost_so_far[current] + 1  # Assuming uniform cost of 1 for all edges

            # If the new cost is lower than any previously recorded cost for the neighbor
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                priority = new_cost  # UCS uses total cost for priority
                open_set.put((priority, neighbour))
                came_from[neighbour] = current
                neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False