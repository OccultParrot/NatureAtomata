import pygame
from enum import Enum


# --- Constants ---
WIDTH = 1000
HEIGHT = 1000
CELL_SIZE = 10

# TODO: Define the types and define the colors
COLOR_MAP = {
    0: (150, 70, 70),  # Type 0 Cells
    1: (70, 150, 70),   # Type 1 Cells
    2: (70, 70, 150),   # Type 2 Cells
}


# --- Classes ---

class Cell:
    """
    Represents a cell in the grid, with a type (used to determine color).
    """
    type: int = 0
    def __init__(self, cell_type: int = 0):
        self.type = 0

    def update(self, pos_x, pos_y):
        """
        Updates the cell state. Placeholder for future logic.
        """
        neighbors = get_neighbors(pos_x, pos_y)

        # TODO: Write update logic and set of rules
        # Temporary testing function
        if neighbors[0].type == self.type:
            self.type = 0

# --- Functions ---
def init_cells():
    """
    Initializes the grid of cells, assigning each cell a type based on its position.
    :return: 2D list of Cell objects.
    """
    rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
    return [
        [Cell(j % 3) for j in range(cols)]  # Assigning cell types based on column index
        for i in range(rows)
    ]


def generate_uv_gradient():
    """
    Generates a UV gradient for testing:
    - Red is based on column index (x-coordinate).
    - Green is based on row index (y-coordinate).
    - Blue is fixed to 0.

    :return: A 2D list of RGB tuples representing the gradient.
    """
    rows, cols = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
    return [
        [
            (int((j / (cols - 1)) * 255), int((i / (rows - 1)) * 255), 0)
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def draw_cells():
    """
    Draws the grid of cells on the screen using their assigned color.
    """
    for x in range(0, WIDTH, CELL_SIZE):
        for y in range(0, HEIGHT, CELL_SIZE):
            cell_x, cell_y = x // CELL_SIZE, y // CELL_SIZE  # Calculate the cell index
            cell = cell_arr[cell_y][cell_x]  # Get the cell
            color = COLOR_MAP.get(cell.type, (0, 0, 0))  # Default to black if no match
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))


def get_neighbors(cell_x: int, cell_y: int):
    """
    Returns the neighboring cells of a given cell (cell_x, cell_y).

    :param cell_x: The x-coordinate (column index) of the cell.
    :param cell_y: The y-coordinate (row index) of the cell.
    :return: A list of neighboring Cell objects.
    """
    neighbors = []
    directions = [
        (-1, 0), (1, 0),  # Left, Right
        (0, -1), (0, 1),  # Up, Down
        (-1, -1), (1, -1),  # Top-left, Top-right
        (-1, 1), (1, 1)   # Bottom-left, Bottom-right
    ]

    # Check each direction
    for dx, dy in directions:
        neighbor_x, neighbor_y = cell_x + dx, cell_y + dy

        # Check if the neighbor is within grid bounds
        if 0 <= neighbor_x < WIDTH // CELL_SIZE and 0 <= neighbor_y < HEIGHT // CELL_SIZE:
            neighbors.append(cell_arr[neighbor_y][neighbor_x])

    return neighbors


def update_cells():
    """
    Updates all cells in the grid by calling their update method.
    """
    for x, row in enumerate(cell_arr):
        for y, cell in enumerate(row):
            cell.update(x, y)


# --- Main Program ---
if __name__ == "__main__":
    # Initialize Pygame
    pygame.init()

    # Ensure the window dimensions are divisible by the cell size
    if WIDTH % CELL_SIZE != 0 or HEIGHT % CELL_SIZE != 0:
        raise ValueError("Window dimensions must be divisible by cell size")

    # Initialize the grid of cells
    cell_arr = init_cells()

    # Set up the Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update_cells()  # Update the cell array
        draw_cells()    # Draw the cells on the screen
        pygame.display.flip()  # Update the display

    # Quit Pygame
    pygame.quit()
