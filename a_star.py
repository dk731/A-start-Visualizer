import time
#from A_A import *
from collections import defaultdict
from random import randint
import pygame as pg
from math import inf
global start, end, box_size, dem, walls, win, s, gdosochka, fdosochka, dim, cameFrom, true_path, visited
s = None
win = None
true_path = set()
walls = set() #nomer korobochki
dem = (100, 100)
box_size = 12  #px
start = None
end = None
visited = set()


def reset():
    global start, end, walls, gdosochka, fdosochka, cameFrom, visited
    walls = set()
    start = None
    end = None
    gdosochka = None
    fdosochka = None
    cameFrom = None
    visited = set()

def set_start_end(pos):

    global start, end, walls

    if mouse_pos_to_dosochka(pg.mouse.get_pos()) == start:
        start = None

    elif mouse_pos_to_dosochka(pg.mouse.get_pos()) == end:
        end = None

    else:
        if not start and pos not in walls:
            start = pos

        elif not end and pos not in walls:
            end = pos




def pre_draw():
    global start, end, walls, dim, s, win, box_size

    win.fill((255, 255, 255))
    s = pg.Surface(to_norm_size(win.get_size()), pg.SRCALPHA, 32)
    draw_field()

    x, y = box_size * start[0] + box_size // 2, box_size * start[1] + box_size // 2
    pg.draw.circle(s, (255, 0, 0), (x, y), box_size // 2)

    x, y = box_size * end[0] + box_size // 2, box_size * end[1] + box_size // 2
    pg.draw.circle(s, (0, 255, 0), (x, y), box_size // 2)

    for wall in walls:
        x, y = box_size * wall[0] , box_size * wall[1]
        pg.draw.rect(s, (0, 0, 0), (x, y, box_size, box_size))


    win.blit(s, (-box_size, -box_size))
    pg.display.flip()


def draw_visit(pos):
    global start, end, walls, s, win, box_size, visited

    x, y = box_size * pos[0] + box_size // 2, box_size * pos[1] + box_size // 2
    visited.add(pos)
    pg.draw.circle(s, (128,128,128), (x, y), box_size // 5)
    win.blit(s, (-box_size, -box_size))
    pg.display.flip()



def draw_path():
    global win, s, box_size, cameFrom, start, end, true_path
    true_path = []
    tmp_vert = end
    while tmp_vert in cameFrom.keys():
        true_path.append(tmp_vert)
        tmp_vert = cameFrom[tmp_vert]

    for i in range(len(true_path) - 1):
        x, y = box_size * true_path[i][0] + box_size // 2, box_size * true_path[i][1] + box_size // 2
        x1, y1 = box_size * true_path[i + 1][0] + box_size // 2, box_size * true_path[i + 1][1] + box_size // 2
        pg.draw.circle(s, (255, 0, 255), (x, y), box_size // 3)
        pg.draw.line(s, (255, 0, 255), (x, y), (x1, y1), 3)
        win.blit(s, (-box_size, -box_size))
        pg.display.flip()
        pg.time.delay(10)






def draw_all():
    global start, end, walls, win, s, box_size, true_path, visited
    win.fill((255, 255, 255))
    s = pg.Surface(to_norm_size(win.get_size()), pg.SRCALPHA, 32)
    draw_field()

    x, y = box_size * start[0] + box_size // 2, box_size * start[1] + box_size // 2
    pg.draw.circle(s, (255, 0, 0), (x, y), box_size // 2)

    x, y = box_size * end[0] + box_size // 2, box_size * end[1] + box_size // 2
    pg.draw.circle(s, (0, 255, 0), (x, y), box_size // 2)

    for wall in walls:
        x, y = box_size * wall[0] , box_size * wall[1]
        pg.draw.rect(s, (0, 0, 0), (x, y, box_size, box_size))

    for i in range(len(true_path) - 1):
        x, y = box_size * true_path[i][0] + box_size // 2, box_size * true_path[i][1] + box_size // 2
        x1, y1 = box_size * true_path[i + 1][0] + box_size // 2, box_size * true_path[i + 1][1] + box_size // 2
        pg.draw.circle(s, (255, 0, 255), (x, y), box_size // 3)
        pg.draw.line(s, (255, 0, 255), (x, y), (x1, y1), 3)

    x, y = box_size * true_path[len(true_path) - 1][0] + box_size // 2, box_size * true_path[len(true_path) - 1][1] + box_size // 2
    pg.draw.circle(s, (255, 0, 255), (x, y), box_size // 3)
    pg.draw.line(s, (255, 0, 255), (x, y), (start[0] * box_size + box_size // 2, start[1] * box_size + box_size // 2), 3)

    for i in visited:
        x, y = box_size * i[0] + box_size // 2, box_size * i[1] + box_size // 2
        pg.draw.circle(s, (128, 128, 128), (x, y), box_size // 5)


    win.blit(s, (-box_size, -box_size))
    pg.display.flip()



def evalz_herj(otkuda):
    global end
    return abs(otkuda[0] - end[0]) + abs(otkuda[1] - end[1])


def _get_friends_(gde_ja):
    ans = []
    gde_ja = (gde_ja[0], gde_ja[1])
    ans.append((gde_ja[0] - 1, gde_ja[1] + 1))
    ans.append((gde_ja[0], gde_ja[1] + 1))
    ans.append((gde_ja[0] + 1, gde_ja[1] + 1))
    ans.append((gde_ja[0] + 1, gde_ja[1]))
    ans.append((gde_ja[0] + 1, gde_ja[1] - 1))
    ans.append((gde_ja[0], gde_ja[1] - 1))
    ans.append((gde_ja[0] - 1, gde_ja[1] - 1))
    ans.append((gde_ja[0] - 1, gde_ja[1]))
    return ans

def find_path():
    global start, end, walls, gdosochka, cameFrom, fdosochka, dim

    width = dem[0] + 2
    height = dem[1] + 2

    dim = (width, height)
    gdosochka = defaultdict(lambda : inf)
    fdosochka = defaultdict(lambda : inf)
    cameFrom = dict()

    gdosochka[start] = 0
    fdosochka[start] = evalz_herj(start)
    openSet = {start}

    visited = set()

    for i in range(width):
        visited.add((0, i))
        visited.add((height, i))
    for i in range(height):
        visited.add((i, 0))
        visited.add((i, width))
    for i in walls:
        visited.add(i)

    pre_draw()


    while openSet:

        v = min([point for point in openSet], key=lambda x: fdosochka[x])

        if v == end:
            draw_path()
            while True:
                for e in pg.event.get():
                    if e.type == pg.KEYDOWN:
                        if e.key == pg.K_RETURN:
                            reset()
                            return
                    if e.type == pg.QUIT:
                        pg.quit()
                        raise SystemExit

                draw_all()


        openSet.remove(v)
        for u in _get_friends_(v):


            if (gdosochka[u] > 1 + gdosochka[v]) and (u not in visited ):
                draw_visit(u)
                cameFrom[u] = v
                gdosochka[u] = 1 + gdosochka[v]
                fdosochka[u] = gdosochka[u] + evalz_herj(u)
                if u not in openSet:
                    openSet.add(u)




    reset()


def to_norm_size(size):
    global box_size
    return (size[0] + box_size, size[1] + box_size)


def draw_all_nopath():
    global start, end, walls, win, s, box_size
    win.fill((255, 255, 255))
    s = pg.Surface(to_norm_size(win.get_size()), pg.SRCALPHA, 32)
    draw_field()

    try:
        x, y = box_size * start[0] + box_size // 2, box_size * start[1] + box_size // 2
        pg.draw.circle(s, (255, 0, 0), (x, y), box_size//2)
    except Exception:
        pass

    try:
        x, y = box_size * end[0] + box_size // 2, box_size * end[1] + box_size // 2
        pg.draw.circle(s, (0, 255, 0), (x, y), box_size//2)
    except Exception:
        pass

    for i in walls:
        x, y = box_size * i[0] , box_size * i[1]
        pg.draw.rect(s, (0, 0, 0), (x, y, box_size, box_size))

    win.blit(s, (-box_size, -box_size))
    pg.display.flip()
    pg.time.wait(10)


def set_wall(pos):
    global walls, start, end
    if (pos not in walls) and (pos not in [start, end]):
        walls.add(pos)
        if (pos[0] - 1, pos[1] + 1) in walls:
            if randint(0, 1):
                walls.add((pos[0] - 1, pos[1]))
            else:
                walls.add((pos[0], pos[1] + 1))

        if (pos[0] + 1, pos[1] + 1) in walls:
            if randint(0, 1):
                walls.add((pos[0], pos[1] + 1))
            else:
                walls.add((pos[0] + 1, pos[1]))

        if (pos[0] + 1, pos[1] - 1) in walls:
            if randint(0, 1):
                walls.add((pos[0] + 1, pos[1]))
            else:
                walls.add((pos[0], pos[1] - 1))

        if (pos[0] - 1, pos[1] - 1) in walls:
            if randint(0, 1):
                walls.add((pos[0] - 1, pos[1]))
            else:
                walls.add((pos[0], pos[1] - 1))


        # walls.append((pos[0], pos[1] + 1))
        # walls.append((pos[0] + 1, pos[1]))
        # walls.append((pos[0], pos[1] - 1))
        # walls.append((pos[0] - 1, pos[1]))
def draw_field():
    global win, s
    # for i in range(dem):
    #     pg.draw.line(s, (0, 0, 0), (i * box_size, 0), (i * box_size, win.get_size()[1]))
    # for i in range(dem):
    #     pg.draw.line(s, (0, 0, 0), (0, i * box_size), (win.get_size()[0], i * box_size))
    pass



def mouse_pos_to_dosochka(pos):
    global box_size
    return (pos[0] // box_size + 1 , pos[1] // box_size + 1 )



def main():
    global win, s, box_size, dem
    pg.init()
    pg.RESIZABLE = False

    win = pg.display.set_mode((dem[0] * box_size + 1, dem[1] * box_size + 1), pg.RESIZABLE)
    s = pg.Surface(to_norm_size(win.get_size()), pg.SRCALPHA, 32)
    pg.display.set_caption("Path Finder")

    going = True
    while going:
        for e in pg.event.get():
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    reset()
                if e.key == pg.K_RETURN:
                    if start and end:
                        find_path()

            if (e.type == pg.MOUSEBUTTONDOWN) and e.button == 1:
                set_start_end(mouse_pos_to_dosochka(pg.mouse.get_pos()))


            if (e.type == pg.MOUSEBUTTONDOWN) and e.button == 3:
                set_wall(mouse_pos_to_dosochka(pg.mouse.get_pos()))

            if e.type == pg.MOUSEMOTION and e.buttons[2]:
                set_wall(mouse_pos_to_dosochka(pg.mouse.get_pos()))

            if e.type == pg.QUIT:
                going = False

        draw_all_nopath()

    pg.quit()
    raise SystemExit
main()
