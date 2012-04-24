import pygame
import world

class Agent:
    # Initialize.
    def __init__(self, sprite_set_filename ):
        assert(sprite_set_filename != "")
        
        # Load spriteset.
        self._sprite_surface = pygame.image.load(sprite_set_filename)
        
        # Set dimensions.
        self.width = self._sprite_surface.get_width() / 3
        self.height = self._sprite_surface.get_height() / 4
        self.base = (self.width / 2, self.height * 3 / 4)
        self.base_offset = self.base
        
        # Set drawing rectangle.
        self.handle_move(world.World.Action.Move_Down)
        
    # Draw.
    def draw_to(self, surface, offset):
        surface.blit(
            self._sprite_surface,
            (offset[0] - self.base_offset[0], offset[1] - self.base_offset[1]),
            self.draw_rect )
        
    # Change image for a move.
    def handle_move(self, action):
        assert((action >= 0) and (action < 4))
        
        # Adjust base offset.
        bx = 0
        by = 0
        quarter_offset = self.width / 4
        if world.World.Action.Move_Left == action:
            bx -= quarter_offset + 6
        elif world.World.Action.Move_Right == action:
            bx += quarter_offset + 6
        elif world.World.Action.Move_Down == action:
            by += quarter_offset + 12
        elif world.World.Action.Move_Up == action:
            by -= quarter_offset
        bx = 0
        by = 0
        self.base_offset = (self.base[0] + bx, self.base[1] + by)
        
        self.draw_rect = pygame.Rect(
            self.width*1, action*self.height,
            self.width, self.height )