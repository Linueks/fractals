import time
from PIL import Image, ImageDraw
from math import log, log2
import numpy as np
from imageio import imwrite


def mandelbrot(c, renormalize_escape=True):
    """
    two coords instead of complex implementation, something is wrong with it dunno
    z_r = 0
    z_i = 0
    for i in range(max_iterations):
        z_r_squared = z_r * z_r
        z_i_squared = z_i * z_i
        z_r = z_r_squared - z_i_squared + c_r
        z_i = 2 * z_r * z_i + c_i
        if z_r_squared + z_i_squared > 4:
            return i
    """
    z = 0
    for i in range(max_iterations):
        if abs(z) > 2:
            return i
        z = z**2 + c

    if renormalize_escape:
        return i + 1 - log(abs(z)) / log(2)

    else:
        return i



def numpy_mandelbrot(width, height):
    x = np.linspace(-2.5, 1, width).reshape((1, width))
    y = np.linspace(-1, 1, height).reshape((height, 1))
    c = np.tile(x, (height, 1)) + 1j * np.tile(y, (1, width))

    z = np.zeros(c.shape, dtype=np.complex128)
    #divergence_time = np.zeros(z.shape, dtype=int)
    divergence_mask = np.full(z.shape, True, dtype=bool)
    for i in range(max_iterations):
        z[divergence_mask] = z[divergence_mask]*z[divergence_mask] + c[divergence_mask]
        #diverged = np.greater(np.abs, 2, out=np.full(z.shape, False))
        #divergence_time[diverged] = i
        #print(i)
        divergence_mask[np.abs(z) > 2] = False

    imwrite('plots/numpy_output.png', np.uint8(np.flipud(1 - divergence_mask) * 255))


def precalculate_coordinates(width, height):
    #plot window scaling
    real_min, real_max = -2.5, 1
    imag_min, imag_max = -1, 1
    real_factor = (real_max - real_min) / width
    imag_factor = (imag_max - imag_min) / height
    reals = [(real_min + x * real_factor, x) for x in range(width)]
    imags = [(imag_min + y * imag_factor, y) for y in range(height)]

    return reals, imags



def run_naive():
    hue_factor = 255 / max_iterations
    saturation = 255

    im = Image.new('HSV', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    reals, imags = precalculate_coordinates(width, height)

    for r, x in reals:
        for i, y in imags:
            c = complex(r, i)
            m = mandelbrot(c)
            hue = int(hue_factor * m)
            value = 255 if m < max_iterations else 0
            draw.point([x, y], (hue, saturation, value))

    #im.show('output.png', 'PNG')
    im.convert('RGB').save('plots/output.png', 'PNG')


if __name__ == '__main__':
    max_iterations = 256
    # Image size (pixels)
    width = 3840
    height = 2160
    start_time = time.process_time()
    numpy_mandelbrot(width, height)
    process_time = time.process_time() - start_time
    print(process_time)
    with open('timing.txt', 'a') as outfile:
        outfile.write(f'{process_time}, {width}, {height}, {max_iterations}, 4k numpy' + '\n')
