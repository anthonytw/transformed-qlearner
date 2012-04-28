import pygame, sys
from pygame.locals import *
from world import World
import transforms

# Initialize pygame.
pygame.init()

fps_clock   = pygame.time.Clock()
fps         = 10
tpt         = 1.0 / fps

# Determine action interval.
action_interval_s = 0.5
action_interval_t = int(fps * action_interval_s)

# Initialize world.
full_transform = True#False

if full_transform:
    world = World.from_file("resources/initial_state_2x1.xml")
else:
    world = World.from_file("resources/initial_state_10x10.xml")
world.redraw()

# Initialize transforms.
transform_set = transforms.TransformSet("resources", world, full_transform)

# Initialize window.
padding = (world._cell_pixel_width, 2*world._cell_pixel_height)
window_surface = pygame.display.set_mode((world.get_width() + 2*padding[0], world.get_height() + 2*padding[1]))
pygame.display.set_caption('CAP 6671 - Final Project')

# Execute application.
ticks_to_next_action = action_interval_t
won = False
running_policy = False
while True:
    # Time for action?
    if running_policy:
        # Decrement action ticker.
        ticks_to_next_action -= 1
        
        # Take action when time.
        if ticks_to_next_action <= 0:
            ticks_to_next_action = action_interval_t
            if not won:
                action, q_value = transform_set.get_best_action(world.agent_state)
                world.agent_state = world.perform_action(world.agent_state, action)
                print "Performed action %s for Q-value %d" % (World.Action.name[action], q_value)
                print
                
                # Won?
                if world.agent_state.arrows == World.ArrowState.Arrows_Complete:
                    won = True
                    running_policy = False
                    print "Finished!"
    
    # Draw world.
    world.redraw();
    window_surface.fill((0,0,0))
    world.draw_to(window_surface, padding)
    
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
                world.agent_state = world.perform_action(world.agent_state, World.Action.Move_Up)
            elif event.key == K_DOWN:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Move_Down)
            elif event.key == K_LEFT:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Move_Left)
            elif event.key == K_RIGHT:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Move_Right)
                
            # Minerals.
            elif event.key == K_d:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Dig)
            elif event.key == K_s:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Separate)
            elif event.key == K_e:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Extract)
                
            # Bamboo.
            elif event.key == K_t:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Till)
            elif event.key == K_p:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Plant)
            elif event.key == K_h:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Harvest)
                
            # Arrows.
            elif event.key == K_1:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Form_Tips)
            elif event.key == K_2:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Form_Fins)
            elif event.key == K_3:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Form_Shafts)
            elif event.key == K_4:
                world.agent_state = world.perform_action(world.agent_state, World.Action.Connect_Parts)
                
            # Start policy runner.
            elif event.key == K_RETURN:
                print "Begin running policy..."
                running_policy = True
    
    pygame.display.update()
    fps_clock.tick( fps )
