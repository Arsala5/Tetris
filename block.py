import pygame
from colors import Colors
from position import Position

class Block:
    def __init__(self, id):
        # Each block type has a unique id (used for color + grid representation)
        self.id = id                    
        self.cells = {}                 # Rotation states: key = rotation, value = list of Positions
        self.cell_size = 30             # Size of each tile in pixels
        self.rotation_state = 0         # Start at rotation state 0
        self.row_offset = 0             # Vertical offset from top
        self.column_offset = 0          # Horizontal offset from left

    def move(self, rows, columns):
        # Shift block by (rows, columns) in the grid
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        # Return actual positions of all tiles after applying offsets
        tiles = self.cells[self.rotation_state]
        return [
            Position(t.row + self.row_offset, t.column + self.column_offset)
            for t in tiles
        ]

    def rotate(self):
        # Go to next rotation state (wrap around using modulo)
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)

    def undo_rotation(self):
        # Revert to previous rotation (used if new rotation doesn't fit)
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)

    def draw(self, screen, offset_x, offset_y):
        # Draw each cell of this block on the screen with correct color
        color = Colors.get_cell_colors()[self.id]
        for pos in self.get_cell_positions():
            rect = pygame.Rect(
                offset_x + pos.column * self.cell_size,
                offset_y + pos.row * self.cell_size,
                self.cell_size - 1,
                self.cell_size - 1
            )
            pygame.draw.rect(screen, color, rect)
