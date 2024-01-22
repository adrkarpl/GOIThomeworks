import time
from multiprocessing import Pool, cpu_count

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def factorize_synchronous(*numbers):
    result = []
    start_time = time.time()
    for number in numbers:
        result.append(factorize(number))
    sync_time = time.time() - start_time
    return sync_time, result

def factorize_parallel(*numbers):
    result = []
    start_time = time.time()
    with Pool(processes=cpu_count()) as pool:
        result = pool.map(factorize, numbers)
    parallel_time = time.time() - start_time
    return parallel_time, result

if __name__ == '__main__':
    #synchronous version
    (synchronous_time, [a, b, c, d]) = factorize_synchronous(128, 255, 99999, 10651060)
    print(f"Synchronous version:\n{a}\n{b}\n{c}\n{d}\n")
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f"Time: {synchronous_time} s\n")

    #parallel version
    (parallel_time, [e, f, g, h]) = factorize_parallel(128, 255, 99999, 10651060)
    print(f"Parallel version:\n{e}\n{f}\n{g}\n{h}\n")
    assert e == [1, 2, 4, 8, 16, 32, 64, 128]
    assert f == [1, 3, 5, 15, 17, 51, 85, 255]
    assert g == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert h == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print(f"Time: {parallel_time} s\n")

    if parallel_time > synchronous_time:
        print("The synchronous version is faster.\n")
    else:
        print("The parallel version is faster.\n")
