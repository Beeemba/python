def get_M(n):
    """Возвращает произведение 5 наименьших делителей N (не считая 1), или 0, если их меньше 5."""
    divs = []
    
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    
    divs.append(n)
    divs.sort()
    
    if len(divs) < 5:
        return 0
    
    m_val = 1
    for d in divs[:5]:
        m_val *= d
        
    return m_val


def solve_task2():
    results = []
    n = 200_000_001
    
    print("Поиск 5 наименьших чисел N > 200 000 000, для которых 0 < M(N) < N...")
    print("=" * 60)
    
    while len(results) < 5:
        m_val = get_M(n)
        if 0 < m_val < n:
            results.append((n, m_val))
            print(f"Найдено: N = {n}, M(N) = {m_val}")
        n += 1
        
    
    return results


if __name__ == "__main__":
    solve_task2()