import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from base import Position, Color, Dimensions

class Cube:
    def __init__(self, object_id, color, uni_color, transparent, scale,
        centroid_position, grid_dimensions):
        self.object_id = object_id
        self.color = color
        self.uni_color = uni_color # If we want to use self.colors (False) of self.color (True) for coloring the cubes
        self.transparent = transparent  # Only wireframe will be visible if True
        self.scale = scale
        self.position = centroid_position
        # Delta is "manhatan"-unidirectional distance to vertices of the cube
        # with scale 1 it is 0.5-units distance to each corner of the cube
        self.grid_dimensions = grid_dimensions
        self.x_delta = (grid_dimensions.x/2) * scale
        self.y_delta = (grid_dimensions.y/2) * scale
        self.z_delta = (grid_dimensions.z/2) * scale

        self.rescale(scale=self.scale)

        ### <GEOMETRIC DEFINITION> ###
        self.edges = (
            (0, 1),
            (0, 3),
            (0, 4),
            (2, 1),
            (2, 3),
            (2, 7),
            (6, 3),
            (6, 4),
            (6, 7),
            (5, 1),
            (5, 4),
            (5, 7),
        )
        self.surfaces = (
            (0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6),
        )

        self.normals = [
            ( 0,  0, -1),
            (-1,  0,  0),
            ( 0,  0,  1),
            ( 1,  0,  0),
            ( 0,  1,  0),
            ( 0, -1,  0)
        ]
        self.colors = (
            (1,1,1),
            (0,1,0),
            (1,0.6,0.3),
            (0,1,0),
            (0,1,0.5),
            (0.5,0.7,0.4),
            (0,1,0),
            (1,0.1,0.3),
            (0,1,0),
            (0,1,0.5),
            )

    def rescale(self, scale=1.0): # scale: <float (0.0 to 1.0) >

        self.delta = 0.5 * scale

        self.verticies = (
            (
                self.position.x +  self.x_delta,
                self.position.y + -self.y_delta,
                self.position.z + -self.z_delta,
            ),
            (
                self.position.x +  self.x_delta,
                self.position.y +  self.y_delta,
                self.position.z + -self.z_delta,
            ),
            (
                self.position.x + -self.x_delta,
                self.position.y +  self.y_delta,
                self.position.z + -self.z_delta,
            ),
            (
                self.position.x + -self.x_delta,
                self.position.y + -self.y_delta,
                self.position.z + -self.z_delta,
            ),
            (
                self.position.x +  self.x_delta,
                self.position.y + -self.y_delta,
                self.position.z +  self.z_delta,
            ),
            (
                self.position.x + self.x_delta,
                self.position.y + self.y_delta,
                self.position.z + self.z_delta,
            ),
            (
                self.position.x + -self.x_delta,
                self.position.y + -self.y_delta,
                self.position.z +  self.z_delta,
            ),
            (
                self.position.x + -self.x_delta,
                self.position.y +  self.y_delta,
                self.position.z +  self.z_delta,
            ),
        )
        ### </GEOMETRIC DEFINITION> ###

    def render(self):
        # Color surfaces if not transparent
        if not self.transparent:
            glBegin(GL_QUADS)

            for surface in self.surfaces:
                glNormal3fv(self.normals[self.surfaces.index(surface)])
                for vertex in surface:

                    if self.uni_color:
                        glColor3fv(self.color.get_tuple())
                    else:
                        glColor3fv(self.colors[self.surfaces.index(surface)])

                    glVertex3fv(self.verticies[vertex])
            glEnd()

        # Connect edges
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.verticies[vertex])
        glEnd()
