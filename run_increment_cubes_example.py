################################################################################
# This is the example how to add simple cubes to the scene and render them.    #
# Mouse rotation + 'w','s','a','d' for movement + 'e','q' for elevation        #
# is already implemented in SceneManager in "core.py"                          #
################################################################################

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# Scene implementation
from base import Position, Color, Dimensions
from core import SceneManager
# Import objects
from cube_obj import Cube
# Import config variables
from config import DISPLAY_RESOLUTION,INITIAL_CAMERA_POSITION,POV_ANGLE,ASPECT_RATIO,ZNEAR,ZFAR, GRID_DIMENSIONS

def main():
    # Setup SCENE_MANAGER
    SCENE_MANAGER = SceneManager(
        display_resolution=DISPLAY_RESOLUTION,
        initial_camera_position=INITIAL_CAMERA_POSITION,
        pov_angle=POV_ANGLE,
        aspect_ratio=ASPECT_RATIO,
        znear=ZNEAR,
        zfar=ZFAR,
        grid_dimensions=GRID_DIMENSIONS)
    # Initialize scene
    SCENE_MANAGER.initialize_scene()

    # Main loop
    i = 0
    while True:
        # Check user events
        SCENE_MANAGER.event_check()

        # Rotate scene
        # glRotatef(1, 3, 1, 1)

        # Add cube every 1 unit (module is used for slower "cube adding", so
        # right now there will be new cube every ms_delay*25 milliseconds)
        i += 1
        print(f"x: {i/25}")
        if (i % 25 == 0):
            cube_centroid_position = Position(x=i/25, y=0, z=0)
            cube_color = Color(R=255, G=0, B=0)
            SCENE_MANAGER.add_cube(cube_centroid_position=cube_centroid_position, cube_color=cube_color, uni_color=False, object_id=0,
                transparent=False, scale=1.0)
            print("Adding new cube on position x: {i/25}")

        # Render objects and entities
        SCENE_MANAGER.display_scene(ms_delay=5)
main()
