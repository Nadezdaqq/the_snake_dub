from random import choice, randint

import pygame

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

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.


class GameObject:
    """Основной класс программы."""

    def __init__(self):
        """Конструктор основного класса."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Макет метода, отвечающего за отрисовку."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Конструктор класса яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Генерирует положения яблока."""
        self.position = (
            randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
            randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        )
        return self.position

    def draw(self):
        """Отрисовывает объекты классса яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class PoisonApple(Apple):
    """Класс отравленного яблока."""

    def __init__(self):
        """Конструктор отравленного яблока."""
        super().__init__()
        self.body_color = (245, 255, 250)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, lenght=1):
        """Конструктор класса змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.lenght = lenght
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = [self.position]

    def draw(self):
        """Отрисовывает змейку."""
        position = self.position
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновление направления ззмейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Отвечает за передвижение змейки по полю."""
        head_x, head_y = self.get_head_position()
        self.position = (
            (head_x + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, self.position)
        if len(self.positions) > self.lenght:
            self.last = self.positions[-1]
        while len(self.positions) > self.lenght:
            self.remove_tail()

    def remove_tail(self):
        """Убирает хвост."""
        remove_tail = pygame.Rect(self.positions.pop(),
                                  (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, remove_tail)

    def get_head_position(self):
        """Определение положения головы змейки."""
        return self.position

    def reset(self):
        """Возврат змейки на стартовое положение."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.lenght = 1
        self.positions = [self.position]
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        direction_list = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(direction_list)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


pygame.font.init()
score_font = pygame.font.SysFont('comicsansms', 20)
white = (255, 255, 102)


def get_score(score):
    """Выводит текущий счёт на экран."""
    value = score_font.render('Your score: ' + str(score) + ' ', True, white)
    score_rectangle = value.get_rect()
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, score_rectangle)
    screen.blit(value, score_rectangle)


def main():
    """Отвечает за основной цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    poison_apple = PoisonApple()
    score = 0

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        apple.draw()
        snake.draw()
        poison_apple.draw()
        get_score(score)

        if snake.get_head_position() == apple.position:
            snake.lenght += 1
            score += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()
            score = 0

        if snake.get_head_position() == poison_apple.position:
            if snake.lenght > 1:
                snake.lenght -= 1
            score -= 1
            poison_apple.randomize_position()

        while apple.position in snake.positions:
            apple.randomize_position()

        while apple.position in poison_apple.position:
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
