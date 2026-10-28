from functools import reduce


def combine_sequences(strategy, *sequences):
    """Генератор: объединяет последовательности по стратегии.

    strategy:
      'interleave' - элементы по очереди из каждой последовательности
      'chain'      - последовательности одна за другой
    """
    if strategy == 'interleave':
        max_len = max(len(s) for s in sequences)
        for i in range(max_len):
            for s in sequences:
                if i < len(s):
                    yield s[i]
    elif strategy == 'chain':
        for s in sequences:
            yield from s
    else:
        raise ValueError(f'Неизвестная стратегия: {strategy}')


def fold_by_type(gen):
    """Свертка генератора в зависимости от типа данных:
    числа -> сумма, строки -> объединение через пробел."""
    gen = iter(gen)
    first = next(gen)  
    if isinstance(first, (int, float)):
        return reduce(lambda a, b: a + b, gen, first)
    if isinstance(first, str):
        return reduce(lambda a, b: a + ' ' + b, gen, first)
    raise TypeError(f'Неподдерживаемый тип данных: {type(first)}')


if __name__ == '__main__':
    nums_a = [1, 2, 3]
    nums_b = [10, 20, 30, 40]
    words_a = ['cat', 'dog']
    words_b = ['fox', 'owl', 'bee']

    print('--- Числа, стратегия interleave ---')
    print('Последовательность:', list(combine_sequences('interleave', nums_a, nums_b)))
    print('Свертка (сумма):', fold_by_type(combine_sequences('interleave', nums_a, nums_b)))

    print('--- Строки, стратегия chain ---')
    print('Последовательность:', list(combine_sequences('chain', words_a, words_b)))
    print('Свертка (объединение):', fold_by_type(combine_sequences('chain', words_a, words_b)))

    print('--- filter + reduce к генератору ---')
    even_gen = filter(lambda x: x % 2 == 0, combine_sequences('interleave', nums_a, nums_b))
    print('Четные числа:', list(even_gen))
    even_sum = reduce(lambda a, b: a + b,
                      filter(lambda x: x % 2 == 0,
                             combine_sequences('interleave', nums_a, nums_b)))
    print('Сумма четных:', even_sum)

    print('--- map + fold к генератору ---')
    upper_gen = map(str.upper, combine_sequences('chain', words_a, words_b))
    print('Верхний регистр:', list(upper_gen))
    print('Свертка после map:', fold_by_type(map(str.upper, combine_sequences('chain', words_a, words_b))))