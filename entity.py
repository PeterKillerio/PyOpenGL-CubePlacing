import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from base import Position, Color, Dimensions, get_grid_position
# Import objects
from cube_obj import Cube

class Entity:
    def __init__(
        self,
        entity_id,          # <int>
        entity_color,       # <class:Color>
        grid_dimensions,    # <class:Dimensions>
        entity_objects=[]): # <class:Cube> List of objects (f.e. cubes) which this entity is made of

        self.entity_id = entity_id
        self.entity_color = entity_color
        self.occupancy_dictionary = {} # This dictionary contains unique tuples for
        # each occupied grid space cube {(0,1,1): entity_id, ... }
        self.entity_objects = entity_objects
        self.grid_dimensions = grid_dimensions

        # If input objects present, update occupancy dictionaty
        if len(self.entity_objects):
            occupancy_dictionary = {}
            # Updata occupancy_dictionary

            for object in self.entity_objects:
                grid_position = get_grid_position(position=object.position, grid_dimensions=self.grid_dimensions)
                occupancy_dictionary[grid_position.get_tuple()] = self.entity_id

    # Will be called by SceneManager while rendering objects
    def render(self):
        for object in self.entity_objects:
            object.render()

    # This function converts 3D position points (list of <class:Position>) to objects
    # used by this entity so that even if there are 10 points per 1 grid cube, we will have 1 grid cube in a grid
    # world - no duplicates. Removes old objects!
    def update_from_points(self, position_points,
                entity_id,             # <int>
                entity_color,          # <class:Color>
                grid_dimensions,       # <class:Dimensions>
                uni_color=False,       # <bool>
                transparent=False):    # <bool>

        # Updata attributes
        self.entity_id = entity_id
        self.entity_color = entity_color
        self.grid_dimensions = grid_dimensions

        occupancy_dictionary = {} # Fill it with points and ignore duplicates
        for point in position_points:
            grid_position = get_grid_position(position=point, grid_dimensions=self.grid_dimensions)
            occupancy_dictionary[grid_position.get_tuple()] = self.entity_id

        # Now iterate the dictionary again and create cubes for the entity
        objects = []
        for position in occupancy_dictionary:
            # Create cube
            cube = Cube(
                object_id=self.entity_id,
                color=self.entity_color,
                uni_color=uni_color,
                transparent=transparent,
                scale=1.0,
                centroid_position=Position(x=position[0], y=position[1], z=position[2]),
                grid_dimensions=self.grid_dimensions)
            self.entity_objects.append(cube)
        return

    # Remove old entity objects - add new, change id
    def update_from_objects(self,
                objects,     # <list<Class:Cube>>
                entity_id):  # <int>
        self.entity_objects = objects
        self.entity_id = entity_id
