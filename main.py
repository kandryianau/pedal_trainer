import pygame as pg
import sys

PLOT_WEIGH = 1600
PLOT_HIGH = 600

pg.init()
pg.joystick.init()
joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
joystick_count = pg.joystick.get_count()

screen = pg.display.set_mode((PLOT_WEIGH + 20, PLOT_HIGH + 40))
plot_surface = pg.Surface((PLOT_WEIGH, PLOT_HIGH))
clock = pg.time.Clock()

ideal_curve = (
    (0, 0),
    (0.1, 60),

)

points = [(0, PLOT_HIGH)]
plot_x = 0
plot_y = 0
plot_x_step = 5

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    for i in range(joystick_count):
        joystick = pg.joystick.Joystick(i)
        joystick.init()

        try:
            jid = joystick.get_instance_id()
        except AttributeError:
            # get_instance_id() is an SDL2 method
            jid = joystick.get_id()

        joy_name = joystick.get_name()

        try:
            guid = joystick.get_guid()
        except AttributeError:
            # get_guid() is an SDL2 method
            pass

        axes = joystick.get_numaxes()

        for a in range(axes):
            if joy_name == 'Alien Zadrotti Pedals' and a == 1:
                axis = joystick.get_axis(a)
                plot_y = int((PLOT_HIGH * (1 - axis)) / 2)

    screen.fill("gray")
    plot_surface.fill((220, 230, 220))
    points.append((plot_x, plot_y))

    for i in range(10, 100, 10):
        pg.draw.line(plot_surface, (150, 150, 150), (0, PLOT_HIGH - int(PLOT_HIGH / 100 * i)), (
            PLOT_WEIGH, PLOT_HIGH - int(PLOT_HIGH / 100 * i)))

    pg.draw.aalines(plot_surface, (255, 0, 0), False, points, 10)
    pg.draw.line(plot_surface, (0, 0, 255), (plot_x, PLOT_HIGH), (plot_x, 0))
    screen.blit(plot_surface, (10, 10))
    pg.display.update()
    plot_x += plot_x_step

    if plot_x >= PLOT_WEIGH:
        plot_x = 0
        points = [(0, PLOT_HIGH)]

    # pg.time.delay(5)
    pg.display.flip()
    clock.tick(60)
