from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
import random

# Define colors
COLORS = [
    (0, 1, 1, 1),  # Cyan
    (1, 0, 0, 1),  # Red
    (0, 1, 0, 1),  # Green
    (0, 0, 1, 1),  # Blue
    (1, 1, 0, 1),  # Yellow
    (1, 0.65, 0, 1),  # Orange
    (0.5, 0, 0.5, 1)  # Purple
]

# Define shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super(TetrisGame, self).__init__(**kwargs)
        self.cols = 10
        self.rows = 20
        self.block_size = min(Window.width / self.cols, Window.height / self.rows)
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False

        self.score_label = Label(text="Score: 0", pos=(10, Window.height - 30))
        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 0.5)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {'shape': shape, 'color': color, 'x': self.cols // 2 - len(shape[0]) // 2, 'y': 0}

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            for y, row in enumerate(self.grid):
                for x, cell in enumerate(row):
                    if cell:
                        Color(*cell)
                        Rectangle(pos=(x * self.block_size, (self.rows - y - 1) * self.block_size),
                                  size=(self.block_size, self.block_size))

            if not self.game_over:
                Color(*self.current_piece['color'])
                for y, row in enumerate(self.current_piece['shape']):
                    for x, cell in enumerate(row):
                        if cell:
                            Rectangle(pos=((self.current_piece['x'] + x) * self.block_size,
                                           (self.rows - (self.current_piece['y'] + y) - 1) * self.block_size),
                                      size=(self.block_size, self.block_size))

    def check_collision(self, shape, x, y):
        for row_y, row in enumerate(shape):
            for col_x, cell in enumerate(row):
                if cell:
                    if (y + row_y >= self.rows or
                        x + col_x < 0 or
                        x + col_x >= self.cols or
                        self.grid[y + row_y][x + col_x]):
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        for y in range(self.rows - 1, -1, -1):
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.cols)])
                lines_cleared += 1
        return lines_cleared

    def update(self, dt):
        if self.game_over:
            return

        self.current_piece['y'] += 1
        if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
            self.current_piece['y'] -= 1
            self.merge_piece()
            lines_cleared = self.clear_lines()
            self.score += lines_cleared ** 2 * 100
            self.score_label.text = f"Score: {self.score}"
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
                self.game_over = True
                self.score_label.text = f"Game Over! Score: {self.score}"

        self.draw()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_piece['x'] -= 1
            if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
                self.current_piece['x'] += 1
        elif keycode[1] == 'right':
            self.current_piece['x'] += 1
            if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
                self.current_piece['x'] -= 1
        elif keycode[1] == 'down':
            self.current_piece['y'] += 1
            if self.check_collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
                self.current_piece['y'] -= 1
        elif keycode[1] == 'up':
            rotated = list(zip(*reversed(self.current_piece['shape'])))
            if not self.check_collision(rotated, self.current_piece['x'], self.current_piece['y']):
                self.current_piece['shape'] = rotated
        self.draw()
        return True

class TetrisApp(App):
    def build(self):
        game = TetrisGame()
        return game

if __name__ == '__main__':
    TetrisApp().run()
