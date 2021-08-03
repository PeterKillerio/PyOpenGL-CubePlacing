import pygame
from pygame.locals import *
import numpy as np
import math

from OpenGL.GL import *
from OpenGL.GLU import *
# Import scene modules
from base import Position, Color, Dimensions
# Import objects
from cube_obj import Cube

class SceneManager:
    def __init__(
        self,
        display_resolution,
        initial_camera_position,
        pov_angle,
        aspect_ratio,
        znear,
        zfar,
        grid_dimensions):

        self.display_resolution = display_resolution
        self.initial_camera_position = initial_camera_position
        ### Perspective
        self.pov_angle=pov_angle
        self.aspect_ratio=aspect_ratio
        ## Near and far cliping distances (when to ignore the object)
        self.znear=znear
        self.zfar=zfar
        # 3D grid dimensions
        self.grid_dimensions = grid_dimensions
        # Every object/entity in the scene will be in this list in order to be rendered
        self.scene_objects = []
        self.entities = []

    def initialize_scene(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.display_resolution, DOUBLEBUF | OPENGL)

        glMatrixMode(GL_PROJECTION)
        gluPerspective(self.pov_angle,(self.aspect_ratio),self.znear,self.zfar)
        glTranslatef(self.initial_camera_position.x, self.initial_camera_position.y, self.initial_camera_position.z )
        glEnable(GL_DEPTH_TEST)

        # Movement implementation initialization
        glMatrixMode(GL_MODELVIEW)
        self.view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
        #
        self.display_center = [self.screen.get_size()[i] // 2 for i in range(2)]
        pygame.mouse.set_pos(self.display_center)
        self.up_down_angle = 0.0
        self.mouse_move = [0, 0]

    def mouse_movement(self, event):
        # init model view matrix
        glLoadIdentity()
        # Mouse movement
        if event.type == pygame.MOUSEMOTION:
            self.mouse_move = [event.pos[i] - self.display_center[i] for i in range(2)]
        pygame.mouse.set_pos(self.display_center)
        # get keys
        keypress = pygame.key.get_pressed()
        # init model view matrix
        glLoadIdentity()
        # apply the look up and down
        self.up_down_angle += self.mouse_move[1]*0.1
        glRotatef(self.up_down_angle, 1.0, 0.0, 0.0)
        # init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # apply the movment
        if keypress[pygame.K_w]:
            glTranslatef(0,0,0.1)
        if keypress[pygame.K_s]:
            glTranslatef(0,0,-0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1,0,0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1,0,0)
        if keypress[pygame.K_e]:
            glTranslatef(0,-0.1,0)
        if keypress[pygame.K_q]:
            glTranslatef(0,0.1,0)

        # apply the left and right rotation
        glRotatef(self.mouse_move[0]*0.1, 0.0, 1.0, 0.0)
        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(self.view_matrix)
        self.view_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        # apply view matrix
        glPopMatrix()
        glMultMatrixf(self.view_matrix)

    # Here implement your additional keyboard controls
    def event_check(self):
        for event in pygame.event.get():

            self.mouse_movement(event=event)

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   pygame.quit()
                   quit()

    # Display scene and render all objects
    def display_scene(self, ms_delay):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        for entity in self.entities:
            entity.render()
        for object in (self.scene_objects):
            object.render()

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(ms_delay)

    # Add cube into the scene
    def add_cube(self, cube_centroid_position,  # <class> Position
        cube_color, # <class> Color
        uni_color, # Use 1 color (True) or default multiple colors (False)
        object_id, # <int>
        transparent, # <True, False>
        scale): # <0.0 , 1,0>

        cube = Cube(
            object_id=object_id,
            color=cube_color,
            uni_color=uni_color,
            transparent=transparent,
            scale=scale,
            centroid_position=cube_centroid_position,
            grid_dimensions=self.grid_dimensions
        )
        self.scene_objects.append(cube)

        return cube

    # Add cube to the "grid structure" so that all the added cubes will clip right next to each other
    # and the minimum x/y/z-axis distance between cubes will be the size of the x/y/z-axis
    # grid sizes
    def add_cube_on_grid(self, cube_centroid_position,  # <class:Position>
        cube_color, # <class:Color>
        uni_color, # <bool> Use 1 color (True) or default multiple colors (False)
        object_id, # <int>
        transparent, # <bool>
        scale): # <float: 0.0 to 1.0>

        new_cube_centroid_position = Position(floor(x=cube_centroid_position.x/grid_dimensions.x),
            floor(y=cube_centroid_position.y/grid_dimensions.y),
            floor(z=cube_centroid_position.z/grid_dimensions.z))

        cube = Cube(
            object_id=object_id,
            color=cube_color,
            uni_color=uni_color,
            transparent=transparent,
            scale=scale,
            centroid_position=cube_centroid_position,
            grid_dimensions=self.grid_dimensions
        )

        self.scene_objects.append(cube)
        return cube
