import tkinter as tk
import random

# --- Собственные исключения ---
class SnakeGameException(Exception):
    """Базовое исключение для игры "Змейка"."""
    pass

class InvalidDirectionException(SnakeGameException):
    """Вызывается при попытке развернуться на 180 градусов."""
    pass

class GameCollisionException(SnakeGameException):
    """Вызывается при столкновении со стеной или хвостом."""
    pass


# --- Классы предметной области ---
class Point:
    """Класс для представления координат точки на сетке."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Snake:
    """Класс, управляющий состоянием и движением змейки."""
    def __init__(self, start_x: int, start_y: int):
        self.body = [
            Point(start_x, start_y),
            Point(start_x - 1, start_y),
            Point(start_x - 2, start_y)
        ]
        self.direction = Point(1, 0)
        self.grow_pending = False

    def set_direction(self, dx: int, dy: int) -> None:
        if self.direction.x == -dx and self.direction.y == -dy:
            raise InvalidDirectionException("Разворот на 180 градусов запрещён")
        self.direction = Point(dx, dy)

    def get_next_head(self) -> Point:
        """Возвращает следующую позицию головы без перемещения."""
        head = self.body[0]
        return Point(head.x + self.direction.x, head.y + self.direction.y)

    def move(self) -> None:
        """Перемещает змейку на одну клетку."""
        new_head = self.get_next_head()
        
        if new_head in self.body:
            raise GameCollisionException("Столкновение с хвостом")
        
        self.body.insert(0, new_head)
        if not self.grow_pending:
            self.body.pop()
        else:
            self.grow_pending = False

    def grow(self) -> None:
        self.grow_pending = True


class Food:
    """Класс, управляющий позицией еды на поле."""
    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = Point(0, 0)

    def randomize(self, snake_body: list[Point] = None) -> None:
        while True:
            self.position = Point(
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            )
            if snake_body is None or self.position not in snake_body:
                break


# --- Класс GUI-приложения ---
class SnakeGameApp(tk.Tk):
    """Главный класс приложения."""
    def __init__(self):
        super().__init__()
        self.title("Змейка (Snake Game)")
        self.resizable(False, False)
        
        self.grid_width = 20
        self.grid_height = 20
        self.cell_size = 20
        
        self.canvas_width = self.grid_width * self.cell_size
        self.canvas_height = self.grid_height * self.cell_size
        
        # Верхняя панель управления
        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.score_label = tk.Label(control_frame, text="Счёт: 0", font=("Arial", 14, "bold"))
        self.score_label.pack(side=tk.LEFT)
        
        self.restart_btn = tk.Button(
            control_frame, text="🔄 Перезапустить", 
            command=self._restart_game, font=("Arial", 12),
            bg="#eceff1", activebackground="#cfd8dc"
        )
        self.restart_btn.pack(side=tk.RIGHT)
        
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(padx=10, pady=10)
        
        # Фокус на окно для обработки клавиш
        self.focus_set()
        
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2)
        self.food = Food(self.grid_width, self.grid_height)
        self.food.randomize(self.snake.body)
        
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.is_frozen = True
        self.speed = 140
        
        self.bind("<KeyPress>", self._on_key_press)
        self._game_loop()

    def _unfreeze(self) -> None:
        self.is_frozen = False

    def _on_key_press(self, event: tk.Event) -> None:
        if self.game_over:
            if event.keysym in ("Return", "space", "Space"):
                self._restart_game()
            return
        
        if not self.game_started:
            self.game_started = True
            self.is_frozen = True
            self.after(1000, self._unfreeze)
            
        try:
            if event.keysym in ("Up", "w", "W", "ц", "Ц"):
                self.snake.set_direction(0, -1)
            elif event.keysym in ("Down", "s", "S", "ы", "Ы"):
                self.snake.set_direction(0, 1)
            elif event.keysym in ("Left", "a", "A", "ф", "Ф"):
                self.snake.set_direction(-1, 0)
            elif event.keysym in ("Right", "d", "D", "в", "В"):
                self.snake.set_direction(1, 0)
        except InvalidDirectionException:
            pass

    def _game_loop(self) -> None:
        if self.game_over:
            return
            
        if self.game_started and not self.is_frozen:
            try:
                self._update()
            except GameCollisionException:
                self._handle_collision()
                self._draw()  # Рисуем финальное состояние
                return
                
        self._draw()
        self.after(self.speed, self._game_loop)

    def _update(self) -> None:
        # Проверяем столкновение ДО перемещения
        next_head = self.snake.get_next_head()
        
        if next_head.x < 0 or next_head.x >= self.grid_width or next_head.y < 0 or next_head.y >= self.grid_height:
            raise GameCollisionException("Столкновение со стеной")
        
        if next_head in self.snake.body:
            raise GameCollisionException("Столкновение с хвостом")
        
        # Теперь безопасно перемещаем
        self.snake.move()
        head = self.snake.body[0]
        
        if head == self.food.position:
            self.snake.grow()
            self.score += 1
            self.score_label.config(text=f"Счёт: {self.score}")
            self.food.randomize(self.snake.body)
            if self.speed > 50:
                self.speed -= 2

    def _draw(self) -> None:
        self.canvas.delete("all")
        
        # 1. Шахматное поле
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                color = "#c8e6c9" if (x + y) % 2 == 0 else "#a5d6a7"
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    fill=color, outline=""
                )
        
        # 2. Еда
        f = self.food.position
        self.canvas.create_rectangle(
            f.x * self.cell_size + 2, f.y * self.cell_size + 2,
            (f.x + 1) * self.cell_size - 2, (f.y + 1) * self.cell_size - 2,
            fill="#d32f2f", outline="#b71c1c"
        )
        
        # 3. Змейка (только в пределах поля)
        for i, p in enumerate(self.snake.body):
            if 0 <= p.x < self.grid_width and 0 <= p.y < self.grid_height:
                color = "#e65100" if i == 0 else "#ff9800"
                self.canvas.create_rectangle(
                    p.x * self.cell_size + 1, p.y * self.cell_size + 1,
                    (p.x + 1) * self.cell_size - 1, (p.y + 1) * self.cell_size - 1,
                    fill=color, outline="#bf360c", width=1
                )
        
        # 4. Текстовые оверлеи
        if not self.game_started:
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2,
                text="Нажмите любую клавишу\nдля начала игры",
                fill="#263238", font=("Arial", 16, "bold"), justify="center"
            )
        elif self.game_over:
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2,
                text=f"GAME OVER\nСчёт: {self.score}\n\nНажмите Пробел\nили кнопку 'Перезапустить'",
                fill="#263238", font=("Arial", 16, "bold"), justify="center"
            )
        elif self.is_frozen:  # ← ДОБАВИТЬ
            self.canvas.create_text(
                self.canvas_width // 2, self.canvas_height // 2,
                text="Приготовьтесь...",
                fill="#263238", font=("Arial", 18, "bold")
            )

    def _handle_collision(self) -> None:
        self.game_over = True
        self.title(f"Змейка - Игра окончена! Счёт: {self.score}")

    def _restart_game(self) -> None:
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2)
        self.food = Food(self.grid_width, self.grid_height)
        self.food.randomize(self.snake.body)
        self.score = 0
        self.game_over = False
        self.game_started = True
        self.is_frozen = True
        self.speed = 150
        self.score_label.config(text="Счёт: 0")
        self.title("Змейка (Snake Game)")
        self.focus_set()  # Возвращаем фокус
        # Перезапускаем игровой цикл
        self.after(100, self._game_loop)
        self.after(1000, self._unfreeze)


if __name__ == "__main__":
    app = SnakeGameApp()
    app.mainloop()
