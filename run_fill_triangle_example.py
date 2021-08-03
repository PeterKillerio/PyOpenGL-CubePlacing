################################################################################
# This is the example how to fill a triangle defined by its corner vertices    #
# with cubes in 3D, then render the triangle. This implementation is           #
# most likely not very optimal, however one can try to utilize 3D convex hull  #
# algorithms on a set of points and from the resulting triangles               #
# wrap the entire object with cubes (possibly fill it with cubes etc...)- but  #
# for that one needs to implement functionality of multiple triangle creation  #
# and combination.                                                             #
# Mouse rotation + 'w','s','a','d' for movement + 'e','q' for elevation        #
# is already implemented in SceneManager in "core.py"                          #
################################################################################

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Scene implementation wrappers
from base import Position, Color, Dimensions, get_grid_position, get_largest_length, get_vector_length, grid_positions_from_points
from core import SceneManager
# Import objects and entity (entity is made of objects)
from cube_obj import Cube
from entity import Entity
# Import config variables
from config import DISPLAY_RESOLUTION,INITIAL_CAMERA_POSITION,POV_ANGLE,ASPECT_RATIO,ZNEAR,ZFAR, GRID_DIMENSIONS

# Triangle filling function
from triangle import get_triangle_side

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

    # Create 3 cubes from arbitrary points
    triangle_positions = [
        Position(x=10,y=-5,z=1),
        Position(x=0,y=6,z=0),
        Position(x=0,y=1,z=9)]
    triangle_cubes = []
    for position in triangle_positions:
        cube = Cube(
            object_id=1,
            color=Color(R=255,G=0,B=0),
            uni_color=False,
            transparent=False,
            scale=1.0,
            centroid_position=position,
            grid_dimensions=GRID_DIMENSIONS)
        triangle_cubes.append(cube)

    # Get the cubical triangle specified by it corners i.e. triangle_cubes
    cubical_triangle_objects = get_triangle_side(triangle_cubes, GRID_DIMENSIONS, return_positions=False)

    # Create entity from cubical triangle
    entity_id = 0
    entity_color = Color(R=255, G=0, B=0)
    cubical_entity = Entity(
        entity_id=entity_id,
        entity_color=entity_color,
        grid_dimensions=GRID_DIMENSIONS,
        entity_objects=cubical_triangle_objects)

    SCENE_MANAGER.entities.append(cubical_entity)

    while True:
        # Check user events
        SCENE_MANAGER.event_check()

        # Rotate scene
        # glRotatef(1, 3, 1, 1)

        print(f"Triangle is made out of: {len(cubical_triangle_objects)} cubes")

        # Render objects and entities
        SCENE_MANAGER.display_scene(ms_delay=5)
main()
