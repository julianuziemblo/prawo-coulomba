import numpy as np
import matplotlib.pyplot as plt
from point import Point
from PIL import Image
from image_parser import is_inside
from image_parser import get_inside

image_path = r'C:\Users\Julian\Desktop\bitmapa.bmp'


def load_image(img_path):
    img = Image.open(img_path)
    arr = np.asarray(img)
    # print(arr.shape)
    # print(is_inside(20, 20, arr))
    print(get_inside(arr))
    # print(arr.size)
    # print(arr.shape)
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    load_image(image_path)
