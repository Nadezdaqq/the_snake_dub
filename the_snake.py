from random import choice, randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет отравленного яблока
POISON_COLOR = (245, 255, 250)

# Цвет надписи
WHITE = (255, 255, 102)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Центр игрового экрана
CENTRE = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Настройка отображения надписи счёта
pg.font.init()
score_font = pg.font.SysFont('comicsansms', 20)


class GameObject:
    """Основной класс программы."""

    def __init__(self, position=CENTRE, body_color=None) -> None:
        """Конструктор основного класса."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Макет метода, отвечающего за отрисовку."""
        raise NotImplementedError('Данный метод неприменим.')


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, position=None, body_color=APPLE_COLOR,
                 occupied_cells=None):
        """Конструктор класса яблока."""
        super().__init__(position, body_color)
        self.occupied_cells = occupied_cells
        if occupied_cells is None:
            occupied_cells = []
        self.randomize_position(occupied_cells=occupied_cells)

    def randomize_position(self, occupied_cells):
        """Генерирует положения яблока."""
        while True:
            self.position = (
                randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
            )
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Отрисовывает объекты классса яблока."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class PoisonApple(Apple):
    """Класс отравленного яблока."""

    def __init__(self, position=None, body_color=POISON_COLOR,
                 occupied_cells=None):
        """Конструктор отравленного яблока."""
        super().__init__(position, body_color, occupied_cells)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, position=CENTRE, body_color=SNAKE_COLOR):
        """Конструктор класса змейки."""
        super().__init__(position, body_color)
        self.lenght = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]

    def draw(self):
        """Отрисовывает змейку."""
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        while len(self.positions) > self.lenght:
            remove_tail = pg.Rect(self.positions.pop(), (
                GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, remove_tail)

    def update_direction(self):
        """Обновление направления ззмейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Отвечает за передвижение змейки по полю."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_position = (
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_position)
        self.last = self.positions.pop() if len(
            self.positions) > self.lenght else None

    def get_head_position(self):
        """Определение положения головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возврат змейки на стартовое положение."""
        self.lenght = 1
        self.positions = [self.position]
        direction_list = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(direction_list)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиши."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def get_score(score):
    """Выводит текущий счёт на экран."""
    value = score_font.render('Your score: ' + str(score) + ' ', True, WHITE)
    score_rectangle = value.get_rect()
    pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, score_rectangle)
    screen.blit(value, score_rectangle)


def main():
    """Отвечает за основной цикл игры."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)
    poison_apple = PoisonApple(occupied_cells=[
        snake.positions, apple.position])
    score = 0

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        get_score(score)
        current_occupied_cells = [
            snake.positions, apple.position, poison_apple.position]

        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            score += 1
            apple.randomize_position(current_occupied_cells)

        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(current_occupied_cells)
            poison_apple.randomize_position(current_occupied_cells)
            score = 0

        elif snake.get_head_position() == poison_apple.position:
            if snake.lenght > 1:
                snake.lenght -= 1
            score -= 1
            poison_apple.randomize_position(current_occupied_cells)

        snake.draw()
        apple.draw()
        poison_apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
