import pygame

class Tileset:
    # Initialize.
    def __init__(self, filename, tile_width, tile_height):
        self._filename = filename
        self._tile_width = tile_width
        self._tile_height = tile_height
        
        # Load tileset.
        self._tileset_surface = pygame.image.load(filename)
        self._tile_count = self._tileset_surface.get_width() / self._tile_width
        
    # Get tile area.
    def get_tile_area(self, tile_index):
        return pygame.Rect(
            (tile_index%self._tile_count)*self._tile_width,
            0, self._tile_width, self._tile_height )
        
    # Get tile surface.
    def get_surface(self):
        return self._tileset_surface