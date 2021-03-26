import time
from PIL import Image, ImageDraw


def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z**2 + c
        n += 1
    return n



if __name__ == '__main__':
    start_time = time.process_time()
    # Image size (pixels)
    width = 640
    height = 480

    # Plot window scaling
    reals_interval = [-2.5, 1]
    imaginary_interval = [-1, 1]

    max_iterations = 256

    im = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, width):
        for y in range(0, height):
            # Convert pixel coordinate to complex number
            c = complex(reals_interval[0] + (x / width) * (reals_interval[1] - reals_interval[0]),
                        imaginary_interval[0] + (y / height) * (imaginary_interval[1] - imaginary_interval[0]))
            # Compute the number of iterations
            m = mandelbrot(c)

            # This is where one can make it look interesting
            # The color depends on the number of iterations
            color = 255 - int(m * 255 / max_iterations)
            draw.point([x, y], (color, color, color))



    process_time = time.process_time() - start_time
    with open('test.txt', 'a') as outfile:
        outfile.write('time spent, comment')
    im.save('output.png', 'PNG')
