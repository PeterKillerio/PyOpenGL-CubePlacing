import math

class Dimensions:
    def __init__(self, x=0, y=0, z=0): # x,y,z : <int: "(-inf, inf)">
        self.x = x
        self.y = y
        self.z = z
    def get_tuple(self):
        return (self.x, self.y, self.z)

class Position(Dimensions):
    def __init__(self, x=0, y=0, z=0): # x,y,z : <int: "(-inf, inf)">
        self.x = x
        self.y = y
        self.z = z
    def get_tuple(self):
        return (self.x, self.y, self.z)

class Color:
    def __init__(self, R=255, G=255, B=255): # R,G,B : <int: <0, 255> >
        self.R = R
        self.G = G
        self.B = B
    def get_tuple(self):
        return (self.R, self.G, self.B)

# This function converts arbitrary coordinates to grid (center of grid cube)
# coordinates for those particular coordinates i.e. it tries to find the closest
# "grid cube" (world/grid is made of grid cubes) and returns its center.
def get_grid_position(position, grid_dimensions): 
    # Get closest point on x,y,z-axis
    position_tuple = position.get_tuple()
    grid_tuple = grid_dimensions.get_tuple()
    i_closest = []

    for i in range(3):
        i_axis_floor = position_tuple[i] // grid_tuple[i]
        i_closest.append(i_axis_floor*grid_tuple[i] + (grid_tuple[i]/2))

    return Position(x=i_closest[0], y=i_closest[1], z=i_closest[2])

# Returns length of a vector, arguments: vector tuple (x,y,z)
def get_vector_length(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

# This function returns the size of the longest vector
# Arguments needed are list of tuples (size 3) of size at least 1 tuple in the list
def get_largest_length(vectors):
    record_size = 0
    # For each vector calculate its size and keep track of the record
    for vector in vectors:
        vector_length = get_vector_length(vector)
        if vector_length > record_size: record_size = vector_length
    return record_size

# This function returns series of points (grid cube centroids) from
# series of points <Position> so that there wont be any duplicates
def grid_positions_from_points(position_points, grid_dimensions):
    position_points_dictionary = {} # Fill it with points and ignore duplicates
    for point in position_points:
        grid_position = get_grid_position(position=point, grid_dimensions=grid_dimensions)
        position_points_dictionary[grid_position.get_tuple()] = 1 # Mark existence

    cleaned_position_points_array = []
    for position in position_points_dictionary:
        cleaned_position_points_array.append(Position(x=position[0], y=position[1], z=position[2]))

    return cleaned_position_points_array
