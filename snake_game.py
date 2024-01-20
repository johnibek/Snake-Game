from tkinter import *
import random

# O'yin oynasining kengligi
GAME_WIDTH = 700

# O'yin oynasining kengligi
GAME_HEIGHT = 700

# Ilon tezligi
SPEED = 100

# Ilon har bir bo'lakchasining uzunligi
SPACE_SIZE = 50 

# Ilonning boshlang'ich qismlari soni
BODY_PARTS = 3

# Ilon rangi
SNAKE_COLOR = '#00FF00'  # RGB (GREEN)

# Ovqat rangi
FOOD_COLOR = '#FF0000'  # RGB (RED)

# O'yin oynasining orqa foni
BACKGROUND_COLOR = "#000000"  # BLACK


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x2, y2 in self.coordinates:
            square = canvas.create_rectangle(x2, y2, x2 + SPACE_SIZE, y2 + SPACE_SIZE, fill=SNAKE_COLOR, tags='snake')
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags='food')


def next_turn(snake, food):
    x3, y3 = snake.coordinates[0]

    if direction == 'up':
        y3 -= SPACE_SIZE

    elif direction == 'down':
        y3 += SPACE_SIZE

    elif direction == 'left':
        x3 -= SPACE_SIZE

    elif direction == 'right':
        x3 += SPACE_SIZE

    snake.coordinates.insert(0, (x3, y3))

    square = canvas.create_rectangle(x3, y3, x3 + SPACE_SIZE, y3 + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x3 == food.coordinates[0] and y3 == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete('food')

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,
                       canvas.winfo_height()/2,
                       font=('Consolas', 70),
                       text='GAME OVER',
                       fill='red',
                       tags='gameover')


window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('Consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

window.update()

# Setting the window to the center

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x1 = (screen_width - window_width)/2
y1 = (screen_height - window_height)/2

window.geometry("{}x{}+{}+{}".format(window_width, window_height, int(x1), int(y1)))

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
