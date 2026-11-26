def solve_task1():
    value = 4**511 + 2**511 - 511
    
    binary_str = bin(value)[2:]
    
    ones_count = binary_str.count('1')
    
    print(f"Выражение: 4^511 + 2^511 - 511")
    print(f"Длина двоичной записи: {len(binary_str)} бит")
    print(f"Количество единиц в двоичной записи: {ones_count}")
    
    return ones_count

if __name__ == "__main__":
    solve_task1()