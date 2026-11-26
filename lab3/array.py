from copy import deepcopy


def create_n_dim_array(n, size):
    def build(level):
        if level == n:  
            return [f'level {n}'] * size
        return [build(level + 1) for _ in range(size)]
    return build(1)


def create_n_dim_array_iter(n, size):
    result = [f'level {n}'] * size  
    for _ in range(n - 1):  
        result = [deepcopy(result) for _ in range(size)]
    return result


def _fmt(obj, level, comma):
    """Рекурсивный форматтер: списки из списков печатает в несколько строк
    с отступом 4 пробела на уровень, простые списки - в одну строку."""
    pad = '    ' * level
    tail = ',' if comma else ''
    if not isinstance(obj, list):
        return pad + repr(obj) + tail
    if all(not isinstance(x, list) for x in obj):
        return pad + '[' + ', '.join(repr(x) for x in obj) + ']' + tail
    out = [pad + '[']
    n = len(obj)
    for i, x in enumerate(obj):
        child_comma = True if level >= 1 else i < n - 1
        out.append(_fmt(x, level + 1, child_comma))
    out.append(pad + ']' + tail)
    return '\n'.join(out)


def print_array(arr):
    print(_fmt(arr, 0, False))


if __name__ == '__main__':
    print('>>> create_n_dim_array(2, 3)')
    print_array(create_n_dim_array(2, 3))
    print('>>> create_n_dim_array(3, 2)')
    print_array(create_n_dim_array(3, 2))
    print('>>> create_n_dim_array_iter(2, 3)')
    print_array(create_n_dim_array_iter(2, 3))
    print('>>> create_n_dim_array_iter(3, 2)')
    print_array(create_n_dim_array_iter(3, 2))