def b_recursive(k, x):
    if k == 0:
        return 1 / (2 * x)
    return b_recursive(k - 1, x) * x ** 2


def y_recursive(k, x):
    if x == 0:
        raise ValueError('x не должен быть равен 0')
    if k == 0:
        return 1.0
    return b_recursive(k, x) * y_recursive(k - 1, x)


def y_iterative(k, x):
    if x == 0:
        raise ValueError('x не должен быть равен 0')
    y = 1.0
    b = 1 / (2 * x)
    for _ in range(k):
        b = b * x ** 2
        y = b * y
    return y


if __name__ == '__main__':
    x = 2
    for k in range(5):
        print(f'k={k}: рекурсия = {y_recursive(k, x)}, без рекурсии = {y_iterative(k, x)}')