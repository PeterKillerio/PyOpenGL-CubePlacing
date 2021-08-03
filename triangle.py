# Scene implementation wrappers
from base import Position, Color, Dimensions, get_grid_position, get_largest_length, get_vector_length, grid_positions_from_points
# Import objects and entity (entity is made of objects)
from cube_obj import Cube

# This function returns list of cube-objects (or grid_centroids <Position>s of grid_cubes
# -> specify in argument "return_positions"=True)
# which represent filled surface
# with 3 <Cube>s as corners as arguments
# - arg:'objects' has to be list of 3 objects A,B,C
def get_triangle_side(objects, grid_dimensions, cube_ids =-1, transparent=False, color=Color(R=255,G=0,B=0), uni_color=False, return_positions=False):
    # Order A,B,C
    new_objects_positions = [ get_grid_position(position=objects[0].position, grid_dimensions=grid_dimensions),
        get_grid_position(position=objects[1].position, grid_dimensions=grid_dimensions),
        get_grid_position(position=objects[2].position, grid_dimensions=grid_dimensions)]
    # 3D vector A->B
    A_to_B_vector_tup = tuple(map(lambda i, j: i - j, new_objects_positions[1].get_tuple(), new_objects_positions[0].get_tuple()))
    # 3D vector A->C
    A_to_C_vector_tup = tuple(map(lambda i, j: i - j, new_objects_positions[2].get_tuple(), new_objects_positions[0].get_tuple()))
    # 3D vector B->C
    B_to_C_vector_tup = tuple(map(lambda i, j: i - j, new_objects_positions[2].get_tuple(), new_objects_positions[1].get_tuple()))

    # Step size for iteration will be the smallest edge of a cube /2
    iteration_step_length = min(grid_dimensions.get_tuple())/2
    # Total number of iterations in the first direction will be determined by the longest
    # of vectors A->B, A->C so we don't have empty places
    iteration_count_first = get_largest_length([A_to_B_vector_tup, A_to_C_vector_tup])/iteration_step_length
    # Total number of itereation in the second direction will be determined by
    # the length of a vector B->C
    iteration_count_second = get_vector_length(B_to_C_vector_tup)/iteration_step_length

    # Now get the 3D differences these iterations will move by. Basically divide the
    # particular 3D vector into pieces, preciselly 'interation_count_first/second' pieces
    A_to_B_direction_diff = [A_to_B_vector_tup[0]/iteration_count_first,
        A_to_B_vector_tup[1]/iteration_count_first,
        A_to_B_vector_tup[2]/iteration_count_first]
    B_to_C_direction_diff = [B_to_C_vector_tup[0]/iteration_count_second,
        B_to_C_vector_tup[1]/iteration_count_second,
        B_to_C_vector_tup[2]/iteration_count_second]

    # Now iterate the triangle surface, iterating in the direction o A->B is
    # easy. When iterating to B->C we can use the knowledge of proporional position
    # of A-B to determine how much should we iterate (if this wasnt used it would
    # be problematic to find intersection of vector B->C and A->C), its a trick.
    # Get the "blanket"/surface of a triangle in 3D as bunch of points, then
    # calculate the cubes on those position without repeating the cubes
    saved_positions = [] # of <Position>
    for iteration_a in range(round(iteration_count_first)):
        iteration_a_percentage = iteration_a/iteration_count_first
        iteration_b_limit = iteration_a_percentage*iteration_count_second
        for iteration_b in range(round(iteration_b_limit)):
            position_x = (A_to_B_direction_diff[0]*iteration_a)+(B_to_C_direction_diff[0]*iteration_b)
            position_y = (A_to_B_direction_diff[1]*iteration_a)+(B_to_C_direction_diff[1]*iteration_b)
            position_z = (A_to_B_direction_diff[2]*iteration_a)+(B_to_C_direction_diff[2]*iteration_b)
            triangle_point = Position(x=position_x, y=position_y, z=position_z)
            saved_positions.append(triangle_point)

    # Clean possible grid points -> remove duplicates
    cleaned_grid_cubes_positions = grid_positions_from_points(position_points=saved_positions, grid_dimensions=grid_dimensions)

    if return_positions==True:
        return cleaned_grid_cubes_positions
    else:
        # Return list of cubes created from those points
        # Cube objects
        cube_objects = []
        for centroid_position in cleaned_grid_cubes_positions:
            # Create cube
            cube = Cube(
                object_id=cube_ids,
                color=color,
                uni_color=uni_color,
                transparent=transparent,
                scale=1.0,
                centroid_position=centroid_position,
                grid_dimensions=grid_dimensions)
            cube_objects.append(cube)
        return cube_objects
