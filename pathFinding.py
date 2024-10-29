import pygame
import time
from algorithms import astar, dijkstra, dfs, bfs, ucs

pygame.init()

#INITIALIZE WINDOW
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH + 200, WIDTH))  # Increase window width to make space for buttons
pygame.display.set_caption('Pathfinding')

# COLORS
RED = (85, 127, 170)
GREEN = (0, 198, 255)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (50, 50, 50)
BLACK = (200, 200, 200)
PURPLE = (0, 0, 128)
ORANGE = (255, 165, 0)
GREY = (75, 75, 75)
TURQUOISE = (255, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 149, 237)
TEXT_COLOR = (255, 255, 255)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    #GETTERS
    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def is_path(self):
        return self.color == PURPLE


    #MAKE
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    #DRAW
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN A ROW
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP A ROW
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #right A ROW
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #left A ROW
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid



def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)

    # Draw buttons
    draw_button(win, "A STAR", WIDTH + 25, 150, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(win, "DIJKSTRA", WIDTH + 25, 210, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(win, "DFS", WIDTH + 25, 270, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(win, "BFS", WIDTH + 25, 330, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(win, "UCS", WIDTH + 25, 390, BUTTON_COLOR, BUTTON_HOVER_COLOR)
    draw_button(win, "CLEAR", WIDTH + 25, 450, BUTTON_COLOR, BUTTON_HOVER_COLOR)

    pygame.display.update()

def draw_button(win, text, x, y, color, hover_color, width=150, height=50):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if mouse is hovering over the button
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(win, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(win, color, (x, y, width, height))

    # Draw text on the button
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    win.blit(text_surf, text_rect)


def button_clicked(x, y, button_x, button_y, button_width=100, button_height=50):
    return button_x < x < button_x + button_width and button_y < y < button_y + button_height


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    # Check if the click is within the bounds of the grid
    if 0 <= row < rows and 0 <= col < rows:
        return row, col
    else:
        return None, None  # Return None if clicked outside the grid

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  # Left Mouse Button
                pos = pygame.mouse.get_pos()
                if button_clicked(pos[0], pos[1], WIDTH + 25, 150):  # A STAR button
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    start_time = time.time()
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    end_time = time.time()

                    print(f"A* Algorithm Time: {end_time - start_time:.4f} seconds")

                    started = False

                elif button_clicked(pos[0], pos[1], WIDTH + 25, 210):  # DIJKSTRA button
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    start_time = time.time()
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    end_time = time.time()

                    print(f"Dijkstra Time: {end_time - start_time:.4f} seconds")

                    started = False

                elif button_clicked(pos[0], pos[1], WIDTH + 25, 270):  # DFS button
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    start_time = time.time()
                    dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    end_time = time.time()

                    print(f"DFS Time: {end_time - start_time:.4f} seconds")

                    started = False

                elif button_clicked(pos[0], pos[1], WIDTH + 25, 330):  # BFS button
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    start_time = time.time()
                    bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    end_time = time.time()

                    print(f"BFS Time: {end_time - start_time:.4f} seconds")

                    started = False

                elif button_clicked(pos[0], pos[1], WIDTH + 25, 390):  # UCS button
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    start_time = time.time()
                    ucs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    end_time = time.time()

                    print(f"UCS Time: {end_time - start_time:.4f} seconds")

                    started = False

                elif button_clicked(pos[0], pos[1], WIDTH + 25, 450):  # CLEAR button
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                else:  # Grid interactions
                    row, col = get_clicked_pos(pos, ROWS, width)
                    if row is not None and col is not None:  # Check if within grid bounds
                        node = grid[row][col]
                        if not start and node != end:
                            start = node
                            start.make_start()
                        elif not end and node != start:
                            end = node
                            end.make_end()
                        elif node != end and node != start:
                            node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right Mouse Button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)