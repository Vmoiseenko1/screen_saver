import pygame
from random import  random
from math import sqrt

SCREEN_SIZE = (1280, 720)

class Vector:
    def __init__(self, x):
        self.x = x

    def int_pair(self):
        return self.x

    def __add__(self, other):
        return self.x[0] + other[0], self.x[1] + other[1]

    def  __sub__(self, other):
        return self.x[0] - other[0], self.x[1] - other[1]

    def __mul__(self, other):
        if isinstance(other, list):
            return self.x[0] * other[0], self.x[1] * other[1]
        else:
            return self.x[0] * other, self.x[1] * other

    def len(self):
        return sqrt(self.x[0] ** 2 + self.x[1] ** 2)


class Line:
    def __init__(self, points = [], speeds = []):
        self.points = points
        self.speeds = speeds

    def draw_points(self, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color, (int(self.points[point_number][0]), int(self.points[point_number][1])),
                                 (int(self.points[point_number + 1][0]), int(self.points[point_number + 1][1])), width)

        elif style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(point[0]), int(point[1])), width)

    def set_points(self):
        for point in range(len(self.points)):
            self.points[point] = add(self.points[point], self.speeds[point])
            if self.points[point][0] > SCREEN_SIZE[0] or self.points[point][0] < 0:
                self.speeds[point] = (- self.speeds[point][0], self.speeds[point][1])
            if self.points[point][1] > SCREEN_SIZE[1] or self.points[point][1] < 0:
                self.speeds[point] = (self.speeds[point][0], -self.speeds[point][1])

class Joint(Line):
    def __init__(self, points, count, speeds ):
        Line.__init__(self, points, speeds)
        self.count = count

    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.points) - 1
        if deg == 0:
            return self.points[0]
        return add(multiply(self.points[deg], alpha), multiply(get_point(self.points, alpha, deg - 1), 1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append(multiply(add(self.points[i], self.points[i + 1]), 0.5))
            pnt.append(self.points[i + 1])
            pnt.append(multiply(add(self.points[i + 1], self.points[i + 2]), 0.5))

            result.extend(get_points(pnt, self.count))
        return result

def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                speeds.append((random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        object = Joint(points, speeds)
        object.draw_points()
        object.draw_points(object.get_joint(points, steps), "line", 4, color)
        if not pause:
            object.set_points()
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)


