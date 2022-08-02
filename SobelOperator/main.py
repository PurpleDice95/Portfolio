import numpy as np
from PIL import Image, ImageFilter
import copy
import getopt
import sys


def ApplyKernel(kernel, img):
    pic = copy.deepcopy(img)

    # iterate, avoiding edges
    for i in range(1, img.shape[1]-2):
        for j in range(1, img.shape[0]-2):
            pixel = img[j-1:j+2, i-1:i+2]

            Gx = np.multiply(pixel, kernel).sum()/9
            Gy = np.multiply(np.rot90(kernel, 1), pixel).sum()/9
            pic[j, i] = np.sqrt((Gx**2)+(Gy**2))

    return pic


if __name__ == "__main__":
    inpFile = 'Picture.png'
    outFile = 'EdgeX.png'

    try:
        options, args = getopt.getopt(sys.argv[1:], 'i:o:')
    except getopt.GetoptError:
        print("-i <inpFile> -o <outFile>")
        sys.exit(2)

    for option, arg in options:
        if option =='-i':
            inpFile = arg
        elif option == '-o':
            outFile = arg


    picture = Image.open(inpFile)
    picture = np.array(picture.convert(mode="L").filter(ImageFilter.GaussianBlur(radius=2)))

    sobel_operator = np.array([[-3, 0, 3],
                            [-10, 0, 10],
                            [-3, 0, 3]])

    Image.fromarray(ApplyKernel(sobel_operator, picture)).save(outFile)


