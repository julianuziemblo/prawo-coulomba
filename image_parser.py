import numpy as np


def cast_ray(x: int, y: int, image: np.ndarray, direction: int):
    pass


def is_inside(x: int, y: int, image: np.ndarray) -> bool:
    intersections = 0
    last_color = True
    for i in range(x, image.shape[0]):
        # print(i, end=", ")
        if last_color and not image[y][i]:
            intersections += 1
        last_color = image[y][i]
    return intersections % 2 == 0


def get_inside(image: np.ndarray):
    arr = np.zeros(image.shape)
    print(arr)
    for i, row in enumerate(image):
        for j, cell in enumerate(row):
            arr[i][j] = int(is_inside(j, i, image))
    save_to_file(arr)
    return arr


def save_to_file(arr: np.ndarray):
    with open("table.txt", "w+") as f:
        for i in arr:
            for j in i:
                f.write(str(int(j)) + ' ')
            f.write('\n')
