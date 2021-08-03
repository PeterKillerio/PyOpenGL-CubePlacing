from base import Position, Color, Dimensions

## Scene configuration
DISPLAY_RESOLUTION = (1200, 1000)
INITIAL_CAMERA_POSITION = Position(x=0, y=0, z=-25)
POV_ANGLE = 45
ASPECT_RATIO = DISPLAY_RESOLUTION[0] / DISPLAY_RESOLUTION[1]
# Clipping planes (when to stop render object) near and far limits
ZNEAR = 0.05
ZFAR = 400.0
## Grid world definition
GRID_DIMENSIONS = Dimensions(x=1,y=1,z=1) # x_size, y_size, z_size
