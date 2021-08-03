################################################################################
# This is an example how to convert point-cloud to cubes in 3D space utilizing #
# the Entity class                                                             #
# Mouse rotation + 'w','s','a','d' for movement + 'e','q' for elevation is     #
# already implemented in SceneManager in "core.py"                             #
################################################################################

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
# Scene implementation wrappers
from base import Position, Color, Dimensions
from core import SceneManager
# Import objects and entity (entity is made out of objects)
from cube_obj import Cube
from entity import Entity, get_grid_position
# Import config variables
from config import DISPLAY_RESOLUTION,INITIAL_CAMERA_POSITION,POV_ANGLE,ASPECT_RATIO,ZNEAR,ZFAR, GRID_DIMENSIONS
# Import testing points
from test_points import test_points

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

    # Initialize entity
    entity_id = 0
    entity_color = Color(R=255, G=0, B=0)
    cubical_entity = Entity(
        entity_id=entity_id,
        entity_color=entity_color,
        grid_dimensions=GRID_DIMENSIONS,
        entity_objects=[])

    # Use points/point-cloud to craete 3D entity object made out of cubes
    # even if the points are dense there will be 1 cube per 1  3D grid cube no
    # matter how many points per grid cube are in the point-cloud which is specified
    # in the "test_points.py" file.
    cubical_entity.update_from_points(position_points=test_points,
                entity_id=cubical_entity.entity_id,
                entity_color=cubical_entity.entity_color,
                grid_dimensions=cubical_entity.grid_dimensions,
                uni_color=False,
                transparent=False)

    SCENE_MANAGER.entities.append(cubical_entity)

    while True:
        # Check user events
        SCENE_MANAGER.event_check()

        # Rotate scene
        # glRotatef(1, 3, 1, 1)

        print(f"Total entity objects <len(cubical_entity.objects)>: {len(cubical_entity.entity_objects)}")

        # Render objects and entities
        SCENE_MANAGER.display_scene(ms_delay=5)
main()
