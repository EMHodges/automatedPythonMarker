from results.utils import RegisterModelAnswer


def yo(x, y, z):
    """ Part 1"""
    return x + y + z


# @RegisterModelAnswer(question_number=4, question_part=2)
def yop(x):
    return yo(x, x, x)
