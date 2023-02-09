import numpy as np
from PIL import Image


def cast_rays(x: int, y: int, image: np.ndarray):
    intersections = 0
    last_color = True

    # Top
    for i in range(y, 0):
        if last_color and not image[i][x]:
            intersections += 1
        last_color = image[i][x]
    yield intersections % 2 == 0

    intersections = 0
    last_color = True

    # Right
    for i in range(x, image.shape[0]):
        if last_color and not image[y][i]:
            intersections += 1
        last_color = image[y][i]
    yield intersections % 2 == 0

    intersections = 0
    last_color = True

    # Bottom
    for i in range(y, image.shape[1]):
        if last_color and not image[i][x]:
            intersections += 1
        last_color = image[i][x]
    yield intersections % 2 == 0

    intersections = 0
    last_color = True

    # Left
    for i in range(x, 0):
        if last_color and not image[y][i]:
            intersections += 1
        last_color = image[y][i]
    yield intersections % 2 == 0


def is_inside(x: int, y: int, image: np.ndarray) -> bool:
    # top -> right -> bottom -> left
    if not image[y][x]:
        return False
    rays = list(cast_rays(x, y, image))
    # print(rays)
    t = 0
    f = 0
    for i in rays:
        if i:
            t += 1
        else:
            f += 1
    return t > f if t != f else False


def get_inside(image: np.ndarray):
    arr = np.zeros(image.shape)
    # TODO: add second loop-through to eliminate cells with no neighbors
    for i, row in enumerate(image):
        for j, cell in enumerate(row):
            arr[i][j] = int(is_inside(j, i, image))
    save_to_file(arr)
    return arr


def save_to_file(arr: np.ndarray):
    new_arr = np.ndarray(arr.shape, bool)
    new_arr[arr == 1.] = True
    new_arr[arr == 0.] = False
    im = Image.fromarray(new_arr)
    print("new_arr:")
    print(new_arr)
    im.save("your_file.bmp")
