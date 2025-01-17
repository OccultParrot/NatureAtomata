import pygame
import random
import math

from enum import Enum


# --- Constants ---
WIDTH = 1000
HEIGHT = 1000
CELL_SIZE = 10

MAX_INFLUENCE = 10
NUM_CENTERS = 100

def get_rows() -> int:
    return HEIGHT // CELL_SIZE

def get_cols() -> int:
    return WIDTH // CELL_SIZE

# TODO: Define the types and define the colors
COLOR_MAP = {
    "dirt": (150, 70, 70),  # Dirt Cells
    "grass": (70, 150, 70),   # Grass Cells
    "prey": (70, 70, 150),   # Prey Cells
}
# --- Classes ---

class Cell:
    """
    Represents a cell in the grid, with a type (used to determine color).
    """
    type: str = "dirt"
    def __init__(self, cell_type: str = "dirt"):
        self.type = cell_type

    def update(self, pos_x, pos_y):
        """
        Updates the cell state. Placeholder for future logic.
        """
        neighbors = get_neighbors(pos_x, pos_y)

        # TODO: Write update logic and set of rules

# --- Functions ---
def blob_noise(x: int, y: int, seed: int = 42) -> float:
    """
    Generates blob-like noise using sine waves with random offsets.
    """
    random.seed(seed)

    # Generate random blob centers
    blob_centers = [
        (random.uniform(0, get_cols()), random.uniform(0, get_rows()))
        for _ in range(NUM_CENTERS)
    ]

    # Calculate influence from all blobs
    value = 0
    for bx, by in blob_centers:
        # Calculate distance to blob center
        dx = x - bx
        dy = y - by
        dist = math.sqrt(dx * dx + dy * dy)

        # Add smooth falloff based on distance
        if dist < MAX_INFLUENCE:
            value += 1 - (dist / MAX_INFLUENCE)

    # Normalize value between 0 and 1
    return min(1.0, value)


def init_cells():
    """
    Initializes the grid of cells with blob-like patterns of dirt and grass.
    :return: 2D list of Cell objects.
    """
    rows = get_rows()
    cols = get_cols()

    # Initialize the grid
    grid = []

    for i in range(rows):
        row = []
        for j in range(cols):
            # Generate noise value
            noise_val = blob_noise(j, i)

            # Use threshold to determine cell type
            # Adjust threshold to control grass/dirt ratio
            cell_type = "grass" if noise_val > 0.5 else "dirt"
            row.append(Cell(cell_type))
        grid.append(row)

    return grid



def generate_uv_gradient():
    """
    Generates a UV gradient for testing:
    - Red is based on column index (x-coordinate).
    - Green is based on row index (y-coordinate).
    - Blue is fixed to 0.

    :return: A 2D list of RGB tuples representing the gradient.
    """
    
    return [
        [
            (int((j / (get_cols() - 1)) * 255), int((i / (get_rows() - 1)) * 255), 0)
            for j in range(get_cols())
        ]
        for i in range(get_rows())
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
