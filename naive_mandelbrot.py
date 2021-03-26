import time
from PIL import Image, ImageDraw


def mandelbrot(c):
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

    return i



def precalculate_coordinates(width, height):
    #plot window scaling
    real_min, real_max = -2.5, 1
    imag_min, imag_max = -1, 1
    real_factor = (real_max - real_min) / width
    imag_factor = (imag_max - imag_min) / height
    reals = [(real_min + x * real_factor, x) for x in range(width)]
    imags = [(imag_min + y * imag_factor, y) for y in range(height)]

    return reals, imags


if __name__ == '__main__':
    start_time = time.process_time()
    max_iterations = 256
    # Image size (pixels)
    width = 640
    height = 480

    color_factor = 255 / max_iterations

    im = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    reals, imags = precalculate_coordinates(width, height)

    for r, x in reals:
        for i, y in imags:
            c = complex(r, i)
            m = mandelbrot(c)
            color = 255 - int(m * color_factor)
            draw.point([x, y], (color, color, color))

    process_time = time.process_time() - start_time
    print(process_time)
    with open('timing.txt', 'a') as outfile:
        outfile.write(f'{process_time}, {width}, {height}, back to complex' + '\n')
    im.show('output.png', 'PNG')
    im.save('output.png', 'PNG')
