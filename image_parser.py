import numpy as np
from PIL import Image

from point import Point


def get_inside(image: np.ndarray):
    inside = []
    for i, row in enumerate(image):
        for j, cell in enumerate(row):
            if not image[i][j]:
                inside.append(Point(j, i))
    return inside

# def cast_rays(x: int, y: int, image: np.ndarray):
#     intersections = 0
#     last_color = True
#
#     # Top
#     for i in range(y, 0):
#         if last_color and not image[i][x]:
#             intersections += 1
#         last_color = image[i][x]
#     yield intersections % 2 == 0
#
#     intersections = 0
#     last_color = True
#
#     # Right
#     for i in range(x, image.shape[0]):
#         if last_color and not image[y][i]:
#             intersections += 1
#         last_color = image[y][i]
#     yield intersections % 2 == 0
#
#     intersections = 0
#     last_color = True
#
#     # Bottom
#     for i in range(y, image.shape[0]):
#         if last_color and not image[i][x]:
#             intersections += 1
#         last_color = image[i][x]
#     yield intersections % 2 == 0
#
#     intersections = 0
#     last_color = True
#
#     # Left
#     for i in range(x, 0):
#         if last_color and not image[y][i]:
#             intersections += 1
#         last_color = image[y][i]
#     yield intersections % 2 == 0
#
#
# def is_inside(x: int, y: int, image: np.ndarray) -> bool:
#     # top -> right -> bottom -> left
#     if not image[y][x]:
#         return False
#     rays = list(cast_rays(x, y, image))
#     # print(rays)
#     t = 0
#     f = 0
#     for i in rays:
#         if i:
#             t += 1
#         else:
#             f += 1
#     return t > f
#
#
# def get_neighbours(x: int, y: int, image: np.ndarray):
#     """
#     public static ArrayList<Punkt> bieliSasiedzi(Punkt punkt) {
#         int x = punkt.x;
#         int y = punkt.y;
#         ArrayList<Punkt> listaIndeksow = new ArrayList<>();
#
#         for(int k=x-1;k<=x+1;k++) {
#             for(int l=y-1;l<=y+1;l++) {
#                 if((!(k<0 || k>=plansza.length) && !(l<0 || l>=plansza[0].length))&& plansza[k][l]!=0) {
#                     listaIndeksow.add(new Punkt(k,l));
#                 }
#             }
#         }
#         return listaIndeksow;
#     }
#     """
#     pass

# def save_to_file(arr: np.ndarray):
#     new_arr = np.ndarray(arr.shape, bool)
#     new_arr[arr == 1.] = True
#     new_arr[arr == 0.] = False
#     im = Image.fromarray(new_arr)
#     print("new_arr:")
#     print(new_arr.shape)
#     im.save("your_file.bmp")
