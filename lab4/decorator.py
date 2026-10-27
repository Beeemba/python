import io
from contextlib import redirect_stdout
from functools import wraps


def suppress_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with redirect_stdout(io.StringIO()):
            return func(*args, **kwargs)
    return wrapper


def hero_hp(initial=100):
    hp = max(0, min(100, initial))  

    def change_hp(amount):
        nonlocal hp
        hp += amount  
        hp = max(0, min(100, hp))  
        print(f'HP героя: {hp}')
        return hp

    return change_hp


if __name__ == '__main__':
    print('--- Замыкание без декоратора (вывод есть) ---')
    hero = hero_hp(50)
    hero(30)     
    hero(-50)    
    hero(200)    
    hero(-500)   

    print('--- Декоратор на обычной функции ---')

    @suppress_output
    def noisy():
        print('Этот текст подавлен и не появится на консоли')
        return 42

    result = noisy()  
    print(f'Функция вернула: {result}')

    print('--- Декоратор применён к замыканию ---')
    silent_hero = suppress_output(hero_hp(50))
    hp = silent_hero(30)     
    print(f'Тихое лечение, HP = {hp}')
    hp = silent_hero(-1000)  
    print(f'Тихий урон, HP = {hp}')