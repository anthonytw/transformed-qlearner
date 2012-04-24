import pygame
from agent import Agent
from tileset import Tileset
from configparser import ConfigParser
import copy

class World:
    # Defines valid values for the site state.
    class SiteState:
        Useless             = 0
        Mineral_Deposit     = 1
        Minerals_Exposed    = 2
        Minerals_Separated  = 3
        Good_Soil           = 4
        Tilled              = 5
        Bamboo_Planted      = 6
        Bamboo_Sprouted     = 7
        
    # Defines valid values for the arrows state.
    class ArrowState:
        Not_Started         = 0
        Tips_Formed         = 1
        Fins_Formed         = 2
        Shafts_Formed       = 3
        Arrows_Complete     = 4
        
    # Defines possible actions.
    class Action:
        Move_Down           =  0
        Move_Left           =  1
        Move_Right          =  2
        Move_Up             =  3
        Dig                 =  4
        Separate            =  5
        Extract             =  6
        Till                =  7
        Plant               =  8
        Harvest             =  9
        Form_Tips           = 10
        Form_Fins           = 11
        Form_Shafts         = 12
        Connect_Parts       = 13
        
    # Defines a state.
    class State:
        def __init__(self, world):
            self._world     = world
            self.x          = 0
            self.y          = 0
            self.minerals   = 0
            self.bamboo     = 0
            self.arrows     = World.ArrowState.Not_Started
            
        def site_state(self):
            return self._world.world_state[self.y][self.x]
    
    # Initialize.
    def __init__(self, config_filename):
        assert(config_filename != "")
        
        # Define world variables.
        self.agent_state = World.State(self)
        
        # Define some parameters
        self.needed_minerals = 50
        self.needed_bamboo   = 50
        
        # Initialize bamboo growing queue.
        self.bamboo_grow_delay = 5.0
        self.bamboo_queue = []
        
        # Other parameters.
        self._cell_pixel_width  = 32
        self._cell_pixel_half_width = self._cell_pixel_width / 2
        self._cell_pixel_height = 32
        self._cell_pixel_half_height = self._cell_pixel_height / 2
        
        # Load configuration.
        self.load_configuration(config_filename)
        
    # Load world from configuration file.
    def load_configuration(self, filename):
        configc = ConfigParser(filename)
        config = configc.elements['config']
        
        # Configuration stuff.
        self.draw_grid = config['draw_grid']
        
        # Set world variables.
        self.cell_width = config['map']['width']
        self.cell_height = config['map']['height']
        self.world_state = copy.deepcopy(config['map']['states'])
        
        self.agent_state.x = config['agent']['x']
        self.agent_state.y = config['agent']['y']
        
        # Load agent sprite.
        self.agent_sprite = Agent(config['agent']['filename'])
        
        # Other parameters.
        self._surface_width  = self._cell_pixel_width * self.cell_width
        self._surface_height = self._cell_pixel_height * self.cell_height
        self._surface = pygame.Surface((self._surface_width, self._surface_height))
        
        self._tileset = Tileset(
            config['tileset']['filename'], self._cell_pixel_width, self._cell_pixel_height)
        self._dirty = True
        
    # Get world width / height.
    def get_width(self):
        return self._surface_width
    def get_height(self):
        return self._surface_height
    
    # Determine if the world needs to be redrawn.
    def is_dirty(self):
        return self._dirty
        
    # Redraw surface.
    def redraw(self):
        self._dirty = True
        tileset_surface = self._tileset.get_surface()
        for y in xrange(self.cell_height):
            for x in xrange(self.cell_width):
                self._surface.blit(
                    tileset_surface,
                    (x*self._cell_pixel_width, y*self._cell_pixel_height),
                    self._tileset.get_tile_area(self.world_state[y][x]) )
    
    # Draw the world to a surface.
    def draw_to(self, surface, offset, clean = True):
        # Draw terrain.
        surface.blit(self._surface, (offset[0], offset[1]))
        self._dirty = False if clean else self._dirty
        
        # Draw grid.
        if self.draw_grid:
            for grid_row in xrange(self.cell_height):
                for grid_col in xrange(self.cell_width):
                    cellRect = pygame.Rect(
                        grid_col * self._cell_pixel_width,
                        grid_row * self._cell_pixel_height,
                        self._cell_pixel_width, self._cell_pixel_height )
                    pygame.draw.rect(
                        surface,
                        pygame.Color(0, 0, 0),
                        cellRect,
                        1 )
        
        # Draw agent.
        self.agent_sprite.draw_to(
            surface,
            (offset[0] + self.agent_state.x*self._cell_pixel_width + self._cell_pixel_half_width,
                offset[1] + self.agent_state.y*self._cell_pixel_height + self._cell_pixel_half_height) )
    
    # Handle elapsed time.
    def elapse_time(self, time_elapsed):
        # Decrement grow queue.
        grow_queue = self.bamboo_queue
        self.bamboo_queue = []
        for elem in grow_queue:
            elem[1] -= time_elapsed
            if elem[1] <= 0.0:
                self.world_state[elem[0][1]][elem[0][0]] = World.SiteState.Bamboo_Sprouted
            else:
                self.bamboo_queue.append(elem)
    
    # Handle an action.
    def perform_action(self, action):
        # ----------- MOVEMENT #
        # Move down.
        if   World.Action.Move_Down == action:
            if self.agent_state.y < (self.cell_height - 1):
                self.agent_state.y += 1
            self.agent_sprite.handle_move(action)
        elif World.Action.Move_Left == action:
            if self.agent_state.x > 0:
                self.agent_state.x -= 1
            self.agent_sprite.handle_move(action)
        elif World.Action.Move_Right == action:
            if self.agent_state.x < (self.cell_width - 1):
                self.agent_state.x += 1
            self.agent_sprite.handle_move(action)
        elif World.Action.Move_Up == action:
            if self.agent_state.y > 0:
                self.agent_state.y -= 1
            self.agent_sprite.handle_move(action)
        
        # ----------- MINERALS #
        elif World.Action.Dig == action:
            if self.agent_state.site_state() == World.SiteState.Mineral_Deposit:
                self.world_state[self.agent_state.y][self.agent_state.x] = \
                    World.SiteState.Minerals_Exposed
        elif World.Action.Separate == action:
            if self.agent_state.site_state() == World.SiteState.Minerals_Exposed:
                self.world_state[self.agent_state.y][self.agent_state.x] = \
                    World.SiteState.Minerals_Separated
        elif World.Action.Extract == action:
            if self.agent_state.site_state() == World.SiteState.Minerals_Separated:
                self.world_state[self.agent_state.y][self.agent_state.x] = \
                    World.SiteState.Useless
                self.agent_state.minerals += 50
        
        # ----------- BAMBOO #
        elif World.Action.Till == action:
            if self.agent_state.site_state() == World.SiteState.Good_Soil:
                self.world_state[self.agent_state.y][self.agent_state.x] = \
                    World.SiteState.Tilled
        elif World.Action.Plant == action:
            if self.agent_state.site_state() == World.SiteState.Tilled:
                self.world_state[self.agent_state.y][self.agent_state.x] = \
                    World.SiteState.Bamboo_Planted
                self.bamboo_queue.append(
                    [(self.agent_state.x, self.agent_state.y), self.bamboo_grow_delay])
        elif World.Action.Harvest == action:
            if self.agent_state.site_state() == World.SiteState.Bamboo_Sprouted:
                self.world_state[self.agent_state.y][self.agent_state.x] = \
                    World.SiteState.Useless
                self.agent_state.bamboo += 50
        
        # ----------- ARROWS #
        elif World.Action.Form_Tips == action:
            if (self.agent_state.arrows == World.ArrowState.Not_Started) and \
                (self.agent_state.minerals >= self.needed_minerals) and \
                (self.agent_state.bamboo >= self.needed_bamboo):
                self.agent_state.arrows = World.ArrowState.Tips_Formed
        elif World.Action.Form_Fins == action:
            if self.agent_state.arrows == World.ArrowState.Tips_Formed:
                self.agent_state.arrows = World.ArrowState.Fins_Formed
        elif World.Action.Form_Shafts == action:
            if self.agent_state.arrows == World.ArrowState.Fins_Formed:
                self.agent_state.arrows = World.ArrowState.Shafts_Formed
        elif World.Action.Connect_Parts == action:
            if self.agent_state.arrows == World.ArrowState.Shafts_Formed:
                self.agent_state.arrows = World.ArrowState.Arrows_Complete
                print "WIN!"
                raise
        
        # ----------- SOMETHING ELSE?!?! #
        else:
            print "Invalid action sent: " + str(action)
            raise