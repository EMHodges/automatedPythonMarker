def yo(x, y, z):
    """ Part 1"""
    return x + y + z


def yop(x):
    """ Part 2"""
    return yo(x, x, x)

def g(x,y):
    """Part 2"""
    return yop(x+y)