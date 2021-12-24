import math as m



def circle_line_intersection(line_start, line_end, circle_centre, radius):
    """
    Computes the intersection points, if any between a line segment
    and a circle.
    """
    delta_x = line_end[0] - line_start[0]
    delta_y = line_end[1] - line_start[1]
    circ_x = line_start[0] - circle_centre[0]
    circ_y = line_start[1] - circle_centre[1]
    # a, b and c are coefficients of quadratic equation
    a = delta_x**2 + delta_y**2
    b = (2 * delta_x * circ_x) + (2 * delta_y * circ_y)
    c = (circ_x**2) + (circ_y**2) - radius**2
    discriminant = b*b - (4*a*c)
    if discriminant < 0: # no intersection
        return None
    else:
        # only interested in t_1
        t_1 = (-b - (discriminant**0.5)) / (2*a)
        if 0 <= t_1 <= 1:
            x_1 = line_start[0] + (t_1 * delta_x)
            y_1 = line_start[1] + (t_1 * delta_y)
            return x_1, y_1


def get_distance(vec_1, vec_2):
    """
    Computes the euclidean distance between two vectors (tuples)
    through the use of pythagoras' theorem.
    """
    delta_x = vec_2[0] - vec_1[0]
    delta_y = vec_2[1] - vec_1[1]
    return m.sqrt((delta_x**2) + (delta_y**2))
