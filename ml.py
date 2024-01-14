# importing the necessary modules
import seaborn as sns
import pygame   # importing the pygame module
import time     # importing the time module
import random   # importing the random module
import seaborn as sns  # importing the seaborn module
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def run_game(speed_of_snake=50, runtime=200, Heuristic="Euclidean"):
    step = 0
    # defining the size of the window
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 460
    wall_list = []
    num_wall = 20
    # defining  the colors
    midnight_blue = pygame.Color(25, 25, 112)
    mint_cream = pygame.Color(245, 255, 250)
    crimson_red = pygame.Color(220, 20, 60)
    lawn_green = pygame.Color(124, 252, 0)
    orange_red = pygame.Color(255, 69, 0)

    # initializing the pygame window using the pygame.init() function
    pygame.init()

    # using the set_mode() function of the pygame.display module to set the size of the screen
    display_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # setting the title of the application using the set_caption() function
    pygame.display.set_caption('SNAKE')

    # creating an object of the Clock() class of the pygame.time module
    game_clock = pygame.time.Clock()

    # defining the default position of the snake
    position_of_snake = [100, 50]

    # defining the first four blocks of snake body
    body_of_snake = [
        [100, 50],
        [90, 50],
        [80, 50],
        [70, 50]
    ]

    # position of the fruit
    position_of_fruit = [
        random.randrange(1, (SCREEN_WIDTH//10)) * 10,
        random.randrange(1, (SCREEN_HEIGHT//10)) * 10
    ]
    spawning_of_fruit = True
    # setting the default direction of the snake towards RIGHT
    initial_direction = 'RIGHT'
    snake_direction = initial_direction

    # initial score
    player_score = 0
    # defining the functions
    # function to display the score

    def display_score(selection, font_color, font_style, font_size):

        # creating the font object
        score_font_style = pygame.font.SysFont(font_style, font_size)

        # creating the display surface object
        score_surface = score_font_style.render(
            f'Your Score : {str(player_score)}', True, font_color
        )

        # creating a rectangular object for the text placement
        score_rectangle = score_surface.get_rect()

        # displaying the text
        display_screen.blit(score_surface, score_rectangle)

    # function to over the game

    def game_over():

        # creating the font object
        game_over_font_style = pygame.font.SysFont('times new roman', 50)

        # creating the display surface object
        game_over_surface = game_over_font_style.render(
            f'Your Score is : {str(player_score)}', True, crimson_red
        )

        # creating a rectangular object for the text placement
        game_over_rectangle = game_over_surface.get_rect()

        # setting the position of the text
        game_over_rectangle.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)

        # displaying the text on the screen
        display_screen.blit(game_over_surface, game_over_rectangle)

        # using the flip() function to update the small portion of the screen
        pygame.display.flip()

        # suspending the execution of the current thread for 2 seconds
        time.sleep(2)

        # calling the quit() function
        pygame.quit()

    def get_neighbor(current, direct):
        neighs = []
        up = [current[0], current[1] - 10]
        down = [current[0], current[1] + 10]
        left = [current[0] - 10, current[1]]
        right = [current[0] + 10, current[1]]
        neighs += [up] if direct != "DOWN" else []
        neighs += [down] if direct != "UP" else []
        neighs += [left] if direct != "RIGHT" else []
        neighs += [right] if direct != "LEFT" else []
        return tuple(tuple(inner) for inner in neighs)

    def random_wall():
        wall_list.clear()
        for i in range(num_wall):
            x = random.randrange(1, (SCREEN_WIDTH//10)) * 10
            y = random.randrange(1, (SCREEN_HEIGHT//10)) * 10
            while [x, y] in body_of_snake or [x, y] in wall_list or (x, y) == tuple(position_of_fruit) or euclideanDistance(x, position_of_fruit[0], y, position_of_fruit[1]) <= 1800:
                x = random.randrange(1, (SCREEN_WIDTH//10)) * 10
                y = random.randrange(1, (SCREEN_HEIGHT//10)) * 10
            wall_list.append([x, y])

    def getpath_Astar(food1, snake1, h_func):
        direct = initial_direction
        snake1 = tuple(tuple(inner) for inner in snake1)
        openset = [snake1[0]]
        f = {snake1[0]: 0}
        g = {snake1[0]: 0}
        closedset = []
        dir_array1 = []
        parent = {snake1[0]: False}
        while openset:
            current1 = min(openset, key=lambda x: f[x])
            openset = [openset[i]
                       for i in range(len(openset)) if openset[i] != current1]
            closedset.append(current1)
            # update direct
            if parent[current1]:
                if current1[0] == parent[current1][0] and current1[1] < parent[current1][1]:
                    direct = "UP"
                elif current1[0] == parent[current1][0] and current1[1] > parent[current1][1]:
                    direct = "DOWN"
                elif current1[0] < parent[current1][0] and current1[1] == parent[current1][1]:
                    direct = "LEFT"
                elif current1[0] > parent[current1][0] and current1[1] == parent[current1][1]:
                    direct = "RIGHT"
            for neighbor in get_neighbor(current1, direct):
                if neighbor[0] < 0 or neighbor[0] > SCREEN_WIDTH - 10 or neighbor[1] < 0 or neighbor[1] > SCREEN_HEIGHT - 10:
                    continue
                if neighbor not in closedset and list(neighbor) not in tuple(body_of_snake):
                    tempg = g[current1] + 10
                    if neighbor in openset:
                        if tempg < g[neighbor]:
                            g[neighbor] = tempg
                    else:
                        g[neighbor] = tempg
                        openset.append(neighbor)
                    h_neighbor = h_func(
                        neighbor[0], food1[0], neighbor[1], food1[1])
                    f[neighbor] = g[neighbor] + h_neighbor
                    parent[neighbor] = current1
            if current1[0] == food1[0] and current1[1] == food1[1]:
                break

        if not parent[current1]:
            # No valid path found
            return []
        while parent[current1]:
            if current1[0] == parent[current1][0] and current1[1] < parent[current1][1]:
                dir_array1.append("UP")
            elif current1[0] == parent[current1][0] and current1[1] > parent[current1][1]:
                dir_array1.append("DOWN")
            elif current1[0] < parent[current1][0] and current1[1] == parent[current1][1]:
                dir_array1.append("LEFT")
            elif current1[0] > parent[current1][0] and current1[1] == parent[current1][1]:
                dir_array1.append("RIGHT")
            current1 = parent[current1]
        # print(dir_array1)
        dir_array1.reverse()
        return dir_array1

    start_time = time.time()
    # setting the run flag value to True
    game_run = True
    step = 0
    # the game loop
    # using the while loop
    while game_run:
        elapsed_time = time.time() - start_time
        if elapsed_time >= runtime:
            print(step, player_score)
            break
        # iterating through the events in the pygame.event module
        for event in pygame.event.get():
            # setting the variable value to False if the event's type is equivalent to pygame's QUIT constant
            if event.type == pygame.QUIT:
                # setting the flag value to False
                game_run = False

        Heuristic_func = {"Euclidean": euclideanDistance,
                          "Manhattan": manhattanDistance, "Chebyshev": chebyshevDistance}
        path = getpath_Astar(
            position_of_fruit, body_of_snake, Heuristic_func[Heuristic])
        if (len(path) > 0):
            snake_direction = path[0]
        # neglecting the action taken if the key of opposite direction is pressed
        if snake_direction == 'UP' and initial_direction != 'DOWN':
            initial_direction = 'UP'
        if snake_direction == 'DOWN' and initial_direction != 'UP':
            initial_direction = 'DOWN'
        if snake_direction == 'LEFT' and initial_direction != 'RIGHT':
            initial_direction = 'LEFT'
        if snake_direction == 'RIGHT' and initial_direction != 'LEFT':
            initial_direction = 'RIGHT'

        # updating the position of the snake for every direction
        if initial_direction == 'UP':
            position_of_snake[1] -= 10
        if initial_direction == 'DOWN':
            position_of_snake[1] += 10
        if initial_direction == 'LEFT':
            position_of_snake[0] -= 10
        if initial_direction == 'RIGHT':
            position_of_snake[0] += 10
        step += 1
        # updating the body of the snake
        body_of_snake.insert(0, list(position_of_snake))
        if position_of_snake[0] == position_of_fruit[0] and position_of_snake[1] == position_of_fruit[1]:
            # incrementing the player's score by 1
            player_score += 1
            spawning_of_fruit = False
            # print(path)
        else:
            body_of_snake.pop()

        # randomly spawning the fruit
        while (not spawning_of_fruit):
            position_of_fruit = [
                random.randrange(1, (SCREEN_WIDTH//10)) * 10,
                random.randrange(1, (SCREEN_HEIGHT//10)) * 10
            ]
            if position_of_fruit in body_of_snake:
                continue
            break
        spawning_of_fruit = True

        # filling the color on the screen
        display_screen.fill(mint_cream)

        # drawing the game objects on the screen
        pygame.draw.rect(display_screen, midnight_blue,
                         pygame.Rect(body_of_snake[0][0], body_of_snake[0][1], 10, 10))
        for position in body_of_snake[1:]:
            pygame.draw.rect(display_screen, lawn_green,
                             pygame.Rect(position[0], position[1], 10, 10))
            pygame.draw.rect(display_screen, orange_red, pygame.Rect(
                position_of_fruit[0], position_of_fruit[1], 10, 10))

        # conditions for the game to over
        if position_of_snake[0] < 0 or position_of_snake[0] > SCREEN_WIDTH - 10:
            game_over()
            return step, player_score
        if position_of_snake[1] < 0 or position_of_snake[1] > SCREEN_HEIGHT - 10:
            game_over()
            return step, player_score

        # touching the snake body
        for block in body_of_snake[1:]:
            if position_of_snake[0] == block[0] and position_of_snake[1] == block[1]:
                game_over()
                return step, player_score

        # displaying the score continuously
        display_score(1, midnight_blue, 'times new roman', 20)

        # refreshing the game screen
        pygame.display.update()

        # refresh rate
        game_clock.tick(speed_of_snake)

    # calling the quit() function to quit the application
    pygame.quit()
    return step, player_score


def euclideanDistance(x1, x2, y1, y2):
    return (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)


def manhattanDistance(x1, x2, y1, y2):
    return abs(x1-x2) + abs(y1 - y2)


def chebyshevDistance(x1, x2, y1, y2):
    return max(abs(x1-x2), abs(y1 - y2))


def run_test(epochs=5, speed=20, time=20):
    res_euclidean = []
    res_manhattan = []
    res_chebyshev = []
    for i in range(epochs):
        res_euclidean.append(run_game(speed, time, "Euclidean"))
        res_manhattan.append(run_game(speed, time, "Manhattan"))
        res_chebyshev.append(run_game(speed, time, "Chebyshev"))
    return res_euclidean, res_manhattan, res_chebyshev


res_euclidean, res_manhattan, res_chebyshev = run_test(
    epochs=20, speed=3000, time=30)


x_values, y_values = zip(*res_euclidean)

data_euclidean = pd.DataFrame({'X': x_values, 'Y': y_values})

x_values, y_values = zip(*res_manhattan)

data_manhattan = pd.DataFrame({'X': x_values, 'Y': y_values})

x_values, y_values = zip(*res_chebyshev)

data_chebyshev = pd.DataFrame({'X': x_values, 'Y': y_values})


data = pd.concat([data_euclidean.assign(heuristic='Euclidean'), data_manhattan.assign(
    heuristic='Manhattan'), data_chebyshev.assign(heuristic='Chebyshev')])


# Tạo biểu đồ hồi quy tuyến tính sử dụng lmplot
sns.set(style="whitegrid")  # Thiết lập phong cách cho biểu đồ
plt.figure(figsize=(8, 6))  # Kích thước của biểu đồ
sns.lmplot(x='X', y='Y', data=data, fit_reg=False, hue='heuristic', scatter_kws={
           's': 100})  # fit_reg=False để tắt đường hồi quy

# Đặt tên cho trục và tiêu đề
plt.xlabel('Steps')
plt.ylabel('Scores')
plt.title('Biểu đồ so sánh các hàm heuristic')

# Hiển thị biểu đồ
plt.show()
