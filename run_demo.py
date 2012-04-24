import pygame, sys
from pygame.locals import *
from world import World

# Initialize pygame.
pygame.init()

fps_clock   = pygame.time.Clock()
fps         = 10
tpt         = 1.0 / fps

# Initialize world.
world = World("resources/initial_state.xml")
world.redraw()

# Initialize window.
window_surface = pygame.display.set_mode((world.get_width(), world.get_height()))
pygame.display.set_caption('CAP 6671 - Final Project')

# Execute application.
while True:
    # Draw world.
    world.redraw();
    world.draw_to(window_surface, (0, 0))
    
    # Elapse time.
    world.elapse_time(tpt)

    # Process events.    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.event.post( pygame.event.Event(QUIT) )
                
            # Movement.
            elif event.key == K_UP:
                world.perform_action(World.Action.Move_Up)
            elif event.key == K_DOWN:
                world.perform_action(World.Action.Move_Down)
            elif event.key == K_LEFT:
                world.perform_action(World.Action.Move_Left)
            elif event.key == K_RIGHT:
                world.perform_action(World.Action.Move_Right)
                
            # Minerals.
            elif event.key == K_d:
                world.perform_action(World.Action.Dig)
            elif event.key == K_s:
                world.perform_action(World.Action.Separate)
            elif event.key == K_e:
                world.perform_action(World.Action.Extract)
                
            # Bamboo.
            elif event.key == K_t:
                world.perform_action(World.Action.Till)
            elif event.key == K_p:
                world.perform_action(World.Action.Plant)
            elif event.key == K_h:
                world.perform_action(World.Action.Harvest)
                
            # Arrows.
            elif event.key == K_1:
                world.perform_action(World.Action.Form_Tips)
            elif event.key == K_2:
                world.perform_action(World.Action.Form_Fins)
            elif event.key == K_3:
                world.perform_action(World.Action.Form_Shafts)
            elif event.key == K_4:
                world.perform_action(World.Action.Connect_Parts)
    
    pygame.display.update()
    fps_clock.tick( fps )