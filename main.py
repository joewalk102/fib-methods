from datetime import datetime


def fib_linear(num):
    """
    Compute Fib to the n-th (num) value, only storing current and last.

    Pros:
    - Memory efficient -- only 2 values are stored as the computation occurs.
    Cons:
    - Processor inefficient -- Accessing any other number requires re-computing.
        While it's not as efficient as caching, it's still linear, not exponential.
    """
    if num in {1, 2}:
        return num
    last = 0
    current = 1
    for _ in range(1, num):
        last, current = current, current + last
    return current


def fib_gen():
    """
    Same as "fib_linear" but works as a generator.
    """
    yield 0
    last = 0
    current = 1
    while True:
        yield current
        last, current = current, current + last


def fib_recursive(num):
    """
    Calculate

    Pros:
    - Simple pattern

    Cons:
    - Limited -- There is a max recursion depth
    - Processor Inefficient -- Exponential time complexity.
    """
    if num == 0:
        return 0
    elif num in {1, 2}:
        return 1
    else:
        return fib_recursive(num - 1) + fib_recursive(num - 2)


class FibCachedLinear:
    """
    Compute Fib and cache the results for constant lookup of any already-computed value

    Pros:
    - Processor Efficient -- Constant time if within a range already computed

    Cons:
    - Memory Inefficient -- Stores all results along the way
    """

    def __init__(self):
        self._gen = fib_gen()
        self._cache = list()

    def fib_cached(self, num):
        while True:
            next_num = next(self._gen)
            self._cache.append(next_num)
            try:
                return self._cache[num]
            except IndexError:
                pass


class FibCachedRecursive:
    """
    Compute Fib and cache the results for constant lookup of any already-computed value

    Pros:
    - Processor Efficient -- Constant time if within a range already computed

    Cons:
    - Memory Inefficient -- Stores all results along the way
    - Limited -- There is a max recursion depth
    """

    def __init__(self):
        self._cache = {0: 0, 1: 1}

    def fib_cached(self, num):
        if num in self._cache:
            return self._cache[num]
        self._cache[num] = self.fib_cached(num - 1) + self.fib_cached(num - 2)
        return self._cache[num]


if __name__ == '__main__':
    for i in range(8):
        print(fib_linear(i))
    print(fib_linear(300))

    gen = fib_gen()
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))

    #--------PERF TEST--------

    fcl = FibCachedLinear()
    start = datetime.now()
    fcl.fib_cached(1000)
    diff = datetime.now() - start
    print(f"Linear Cached Microseconds: {diff.microseconds}")

    fcr = FibCachedRecursive()
    start = datetime.now()
    fcr.fib_cached(800)
    diff = datetime.now() - start
    print(f"Recursive Cached Microseconds: {diff.microseconds}")

    start = datetime.now()
    fib_recursive(30)
    diff = datetime.now() - start
    print(f"Recursive Microseconds: {diff.microseconds}")
