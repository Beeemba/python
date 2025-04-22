# Лабораторная работа 1

## Задание 1
Дан словарь городов, необходимо составить по нему словарь словарей расстояний между ними.

![image](https://github.com/user-attachments/assets/9abe09f1-b62c-441f-b258-04ba098b54bb)

## Задание 2
Дано значение радиуса круга и координаты двух точек. Необходимо вывести на консоль значение прощади этого круга с точностю до 4-х знаков после запятой и определить лежат ли точки внутри этого круга.


Для 1 точки:
```
distance_1 = (point_1[0] ** 2 + point_1[1] ** 2) ** 0.5
if distance_1 <= radius:
    print(True)
else:
    print(False)
```
Для 2 точки:
```
distance_2 = (point_2[0] ** 2 + point_2[1] ** 2) ** 0.5
if distance_2 <= radius:
    print(True)
else:
    print(False)
```
## Задание 3
## Задание 4
## Задание 5
## Задание 6
## Задание 7
## Задание 8
## Задание 9
## Задание 10
## Задание 11




$$ \frac{\pi}{2} = \prod_{i=1}^{\infty} \frac{4i^2}{4i^2 - 1}. $$

## Результаты вычислений

Очередной множитель произведения на Python:

python
def wallis_multiplier(i):
    i_squared_times_4 = 4 * i * i
    return i_squared_times_4 / (i_squared_times_4 - 1)


При разнице последних значений произведения $\pi / 2$ менее `1e-7` вычисленное значение $\pi = 3.1411963131348553$.

![Pi convergence plot](img/convergence_plot.png)

Произведение Валлиса сходится очень медленно, поэтому рекомендуется использовать более эффективные методы вычисления числа $\pi$.


## Список использованных источников:

1. [Matplotlib cheatsheets and handouts](https://matplotlib.org/cheatsheets/)
2. [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
3. [Writing mathematical expressions](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions)
