import threading
import time
from PIL import Image
import matplotlib.pyplot as plt

def mandelbrot_calc(z, c, max_iter):
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    return n

def mandelbrot_section(pixels, width, height, x_min, x_max, y_min, y_max, max_iter, y_start, y_end):
    x_step = (x_max - x_min) / width
    y_step = (y_max - y_min) / height
    for y in range(y_start, y_end):
        for x in range(width):
            c = complex(x_min + x * x_step, y_min + y * y_step)
            z = 0
            color = mandelbrot_calc(z, c, max_iter)
            pixels[y * width + x] = color

def mandelbrot_image(width, height, x_min, x_max, y_min, y_max, max_iter, num_threads):
    pixels = [0] * (width * height)
    img = Image.new('RGB', (width, height))
    threads = []
    chunk_height = height // num_threads

    for i in range(num_threads):
        y_start = i * chunk_height
        if i == num_threads - 1:
            y_end = height
        else:
            y_end = y_start + chunk_height
        thread = threading.Thread(target=mandelbrot_section, args=(pixels, width, height, x_min, x_max, y_min, y_max, max_iter, y_start, y_end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    img.putdata([255 - min(int(abs(px) * 255 / max_iter), 255) for px in pixels])
    return img

def calc_speedup(first, second):
    if first > second:
        return first / second
    return second / first


def create_and_mesure_mandelbrot(num_threads):
    global start, img, end
    start = time.time()
    img = mandelbrot_image(width, height, x_min, x_max, y_min, y_max, max_iter, num_threads)
    end = time.time()
    result = (end - start) * 10 ** 3
    print(num_threads, ' threads Time:', result, "ms")
    #img.show()
    img.save('mandelbrot_cpu.png')
    return result


def draw_speedup_graph(results):

    x = [2 ** i for i in range(1, 9)]
    y = [results[0] / result for result in results]
    plt.plot(x, y)
    plt.xlabel('Number of threads')
    plt.ylabel('Speedup')
    plt.title('Speedup graph')
    plt.show()




def benchmark():

    print("Benchmarking...")
    results = []
    for i in range(1, 9):
        num_threads = 2 ** i
        result = create_and_mesure_mandelbrot(num_threads)
        results.append(result)
    for i in range(7):
        speedup = calc_speedup(results[i], results[i + 1])
        print("Speedup between", 2 ** (i + 1), "and", 2 ** (i + 2), "threads:", speedup)

    draw_speedup_graph(results)
    print("Benchmark finished")


if __name__ == '__main__':
    width = 800
    height = 800
    x_min = -2
    x_max = 2
    y_min = -2
    y_max = 2

    max_iter = 512 # 2^9
    benchmark()




