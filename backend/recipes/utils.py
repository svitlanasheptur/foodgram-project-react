import random


def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
