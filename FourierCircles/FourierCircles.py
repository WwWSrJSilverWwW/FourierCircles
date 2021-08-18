import pygame
from math import sin, cos, pi, atan

pygame.init()

di = pygame.display.Info()

WIDTH = di.current_w // 4 * 3
HEIGHT = di.current_h // 4 * 3
SIZE = (WIDTH, HEIGHT)
FPS = 120
FONT = "comicsansms"
NAME = "FourierCircles"
VERSION = "v.0.1.0"
RAM_WIDTH = 16
LEFT_WIDTH = 5
RIGHT_WIDTH = 5
FKO = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

M = 0
N = 0
RADIUS_SCALE_ST = 1.0
SPEED_SCALE_ST = 1.0
RADIUS_SCALE_CHANGE = 0.25
SPEED_SCALE_CHANGE = 0.25
RADIUS_SCALE = RADIUS_SCALE_ST
SPEED_SCALE = SPEED_SCALE_ST
RADIUS = []
SPEED = []
ANGLE = []
CENTER = []
LINE_COLOR = RED
CTR = []


def start():
    global M, N
    M = FKO
    N = 2 * M + 1
    if len(CTR) > 0:
        ks = [0]
        for i in range(1, M + 1):
            ks.extend([-i, i])
        for k in ks:
            xk, yk = 0, 0
            for t in range(len(CTR)):
                xk += CTR[t][0] * cos(-2 * pi * k * t / len(CTR)) - CTR[t][1] * sin(-2 * pi * k * t / len(CTR))
                yk += CTR[t][0] * sin(-2 * pi * k * t / len(CTR)) + CTR[t][1] * cos(-2 * pi * k * t / len(CTR))
            ckx, cky = xk / len(CTR), yk / len(CTR)
            RADIUS.append((ckx ** 2 + cky ** 2) ** 0.5)
            if len(CENTER) != 0:
                CENTER.append([CENTER[-1][0] + ckx, CENTER[-1][1] + cky])
            else:
                CENTER.append([0, 0])
                CENTER.append([ckx, cky])
            SPEED.append(k)
            if ckx >= 0:
                u = 0
            else:
                u = 180
            if ckx == 0:
                tt = 0
            else:
                tt = -atan(cky / ckx) / pi * 180
            ANGLE.append((u + tt) % 360)
        CENTER.pop(-1)


start()
M = 0
N = 0

circles_radius = RADIUS[:]
circles_speed = SPEED[:]
circles_angle = ANGLE[:]
circles_center = [x[:] for x in CENTER]

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(NAME)
clock = pygame.time.Clock()

sc1 = pygame.surface.Surface([WIDTH // 2, HEIGHT])
sc1.fill(WHITE)

running = True
paused = 0
hided = 0
without_ctr = 0
drawing = 1
now_drawing = 0
line = []
while running:
    sc.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            RADIUS_SCALE = RADIUS_SCALE_ST
            SPEED_SCALE = SPEED_SCALE_ST

            M = 0
            N = 0
            RADIUS = []
            SPEED = []
            ANGLE = []
            CENTER = []
            CTR = []

            circles_radius = RADIUS[:]
            circles_speed = SPEED[:]
            circles_angle = ANGLE[:]
            circles_center = [x[:] for x in CENTER]

            line = []
            hided = 0
            without_ctr = 0
            drawing = 1
            now_drawing = 1
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = 0
            now_drawing = 0
            without_ctr = 1
            start()

            circles_radius = RADIUS[:]
            circles_speed = SPEED[:]
            circles_angle = ANGLE[:]
            circles_center = [x[:] for x in CENTER]
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT] and 0:
                nr = RADIUS_SCALE
                ns = SPEED_SCALE
                if event.key == pygame.K_UP:
                    nr += RADIUS_SCALE_CHANGE
                if event.key == pygame.K_DOWN and nr - RADIUS_SCALE_CHANGE > 0:
                    nr -= RADIUS_SCALE_CHANGE
                if event.key == pygame.K_RIGHT:
                    ns += SPEED_SCALE_CHANGE
                if event.key == pygame.K_LEFT and ns - SPEED_SCALE_CHANGE > 0:
                    ns -= SPEED_SCALE_CHANGE
                if all(x[0] / RADIUS_SCALE * nr <= WIDTH // 2 for x in line):
                    for i in range(N):
                        circles_radius[i] = circles_radius[i] / RADIUS_SCALE * nr
                        circles_speed[i] = circles_speed[i] / SPEED_SCALE * ns
                    for x in CTR:
                        x[0] = x[0] / RADIUS_SCALE * nr
                        x[1] = x[1] / RADIUS_SCALE * nr
                    for x in line:
                        x[0] = x[0] / RADIUS_SCALE * nr
                        x[1] = x[1] / RADIUS_SCALE * nr
                    RADIUS_SCALE = nr
                    SPEED_SCALE = ns
            if event.key == pygame.K_SPACE:
                paused += 1
                paused %= 2
            if event.key == pygame.K_TAB:
                hided += 1
                hided %= 3
            if event.key == pygame.K_q:
                without_ctr += 1
                without_ctr %= 2

    if not drawing:
        if len(line) >= 2:
            ln = [[x[0] + WIDTH // 4 * 3, x[1] + HEIGHT // 2] for x in line]
            pygame.draw.lines(sc, LINE_COLOR, False, ln, RIGHT_WIDTH)
        if len(line) >= 1000:
            line.pop(0)

        if hided <= 1:
            for i in range(N):
                wh = [circles_center[i][0] + WIDTH // 4 * 3, circles_center[i][1] + HEIGHT // 2]
                if hided <= 1:
                    pygame.draw.circle(sc, BLACK, wh, 2 * RADIUS_SCALE)
                if hided == 0:
                    pygame.draw.circle(sc, BLACK, wh, circles_radius[i], 1)
        if hided <= 1 and len(circles_center) >= 2:
            wh = [[x[0] + WIDTH // 4 * 3, x[1] + HEIGHT // 2] for x in circles_center]
            pygame.draw.lines(sc, BLACK, False, wh, 1)

        if not paused:
            for i in range(1, N):
                circles_angle[i] += circles_speed[i] * SPEED_SCALE
                circles_angle[i] %= 360
                circles_center[i][1] = circles_center[i - 1][1] - circles_radius[i - 1] * sin(circles_angle[i - 1] / 180 * pi)
                circles_center[i][0] = circles_center[i - 1][0] + circles_radius[i - 1] * cos(circles_angle[i - 1] / 180 * pi)
            if len(circles_center) >= 1:
                line.append(circles_center[-1][:])

    sc.blit(sc1, (0, 0))

    if len(CTR) >= 2:
        pp = [x[:] for x in CTR]
        for x in pp:
            x[0] += WIDTH // 4
            x[1] += HEIGHT // 2
        pygame.draw.lines(sc, GREEN, True, pp, LEFT_WIDTH)

    j = (RAM_WIDTH - 1) // 2
    pygame.draw.line(sc, GRAY, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], RAM_WIDTH)
    pygame.draw.line(sc, GRAY, [j, 0], [j, HEIGHT], RAM_WIDTH)
    pygame.draw.line(sc, GRAY, [WIDTH - j - (2 - RAM_WIDTH % 2), 0], [WIDTH - j - (2 - RAM_WIDTH % 2), HEIGHT], RAM_WIDTH)
    pygame.draw.line(sc, GRAY, [0, HEIGHT - j - (2 - RAM_WIDTH % 2)], [WIDTH, HEIGHT - j - (2 - RAM_WIDTH % 2)], RAM_WIDTH)
    pygame.draw.line(sc, GRAY, [0, j], [WIDTH, j], RAM_WIDTH)

    f2 = pygame.font.SysFont(FONT, 15)
    text5 = f2.render(VERSION, True, BLACK)
    sc.blit(text5, (22, HEIGHT - 40))

    if drawing and now_drawing:
        mx, my = pygame.mouse.get_pos()
        mx = max(min(mx, WIDTH // 2 - RAM_WIDTH // 2), RAM_WIDTH)
        my = max(min(my, HEIGHT - RAM_WIDTH), RAM_WIDTH)
        mx -= WIDTH // 4
        my -= HEIGHT // 2
        if len(CTR) == 0 or CTR[-1] != [mx, my]:
            CTR.append([mx, my])

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
