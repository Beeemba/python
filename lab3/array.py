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


if __name__ == '__main__':
    from pprint import pprint
    print('Рекурсия:')
    pprint(create_n_dim_array(2, 3))
    pprint(create_n_dim_array(3, 2))
    print('Без рекурсии:')
    pprint(create_n_dim_array_iter(2, 3))
    pprint(create_n_dim_array_iter(3, 2))