def scale(value, start, end):
    return start + value * (end - start) / 100


def naive_scaled(it, start, end):
    return (scale(value, start, end) for value in it)


def bound_scale(it):
    """
    Ensures that:
    * values are bound between [0, 100]
    * value is never less than previous value
    * last value is 100
    """
    last = 0
    for value in it:
        value = min(max(last, value), 100)
        yield value
        last = value
    if last < 100:
        yield 100


def safe_scaled(it, start, end):
    return naive_scaled(bound_scale(it), start, end)


# ---------------------

def sub_task_1():
    yield 1
    yield 30
    yield 75
    yield 100


def sub_task_2():
    yield from range(10, 100, 21)


def sub_task_3():
    yield -5
    yield 55
    yield 23
    yield 98


def task_1():
    yield 10

    yield from safe_scaled(sub_task_1(), 10, 30)

    yield from safe_scaled(sub_task_2(10, 100, 25), 30, 45)

    yield from safe_scaled(sub_task_3(), 45, 80)
    yield 80
    yield 99


def main():
    for i in safe_scaled(main(), 0, 100):
        print(i)
    

if __name__ == "__main__":
    main()