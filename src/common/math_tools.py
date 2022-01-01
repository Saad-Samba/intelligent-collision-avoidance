import math as m
#Math that I didn't try to understand and chose just to work with.

def circle_line_intersection(S, E, C, r):
    """
    (C,r) : Centre and Radius of the circle.
    (S, E) : Start and end of line segment.
    Computes the intersection point between a line segment
    and a circle.
    """
    dx = E[0] - S[0]
    dy = E[1] - S[1]
    circ_x = S[0] - C[0]
    circ_y = S[1] - C[1]
    # a, b and C are coefficients of quadratic equation
    a = dx**2 + dy**2
    b = (2 * dx * circ_x) + (2 * dy * circ_y)
    C = (circ_x**2) + (circ_y**2) - r**2
    discriminant = b*b - (4*a*C)
    if discriminant < 0: # no intersection
        return None
    else:
        # only interested in t_1
        t_1 = (-b - (discriminant**0.5)) / (2*a)
        if 0 <= t_1 <= 1:
            x_1 = S[0] + (t_1 * dx)
            y_1 = S[1] + (t_1 * dy)
            return x_1, y_1


def get_distance(vec_1, vec_2):
    """
    Computes the euclidean distance between two vectors (tuples)
    through the use of pythagoras' theorem.
    """
    dx = vec_2[0] - vec_1[0]
    dy = vec_2[1] - vec_1[1]
    return m.sqrt((dx**2) + (dy**2))
