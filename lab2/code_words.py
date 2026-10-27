#Вариант 7
from itertools import product

count = 0
for word in product('ABCDE', repeat=5):
    if word[0] != 'E' and word[-1] != 'A':
        count += 1

print(count)