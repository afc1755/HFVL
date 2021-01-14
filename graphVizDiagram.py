import pyglet
from pyglet import shapes
from pyglet.gl import *

# constant value declarations
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SMALL_BOX_WIDTH = 120
SMALL_BOX_HEIGHT = 100
START_BOX_POS = [10, 10]

WHITE = (255, 255, 255)
WHITE_ALPHA = (255, 255, 255, 255)
BLACK = (0, 0, 0)
BLACK_ALPHA = (0, 0, 0, 255)

DEFAULT_TEXT_SIZE = 10

ARROW_NORMAL_SIZE = 10
ARROW_BOLD_SIZE = 5
LINE_NORMAL_SIZE = 1
LINE_BOLD_SIZE = 2


def draw_basic_picture(round_num):
    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    background_batch = pyglet.graphics.Batch()
    foreground_batch = pyglet.graphics.Batch()
    background = shapes.Rectangle(0, 0, 800, 600, color=(255, 255, 255), batch=background_batch)

    top_label = []
    top_box = []
    bottom_label = []
    bottom_box = []
    arrow = []
    arrowheads = []

    for i in range(0, 5):
        top_label.append(pyglet.text.Label('Word ' + str(i + 1) + ' Round ' + str(round_num),
                                           font_name='Times New Roman',
                                           font_size=DEFAULT_TEXT_SIZE,
                                           x=START_BOX_POS[0] + (SMALL_BOX_WIDTH * i) + DEFAULT_TEXT_SIZE,
                                           y=WINDOW_HEIGHT-(START_BOX_POS[1]+(SMALL_BOX_HEIGHT/2)+(DEFAULT_TEXT_SIZE/2)),
                                           batch=foreground_batch))
        top_label[i].color = BLACK_ALPHA
        top_box.append(shapes.BorderedRectangle(START_BOX_POS[0] + (SMALL_BOX_WIDTH * i),
                                                WINDOW_HEIGHT-START_BOX_POS[1]-SMALL_BOX_HEIGHT,
                                                SMALL_BOX_WIDTH, SMALL_BOX_HEIGHT,
                                                border=1,
                                                color=WHITE,
                                                border_color=BLACK,
                                                batch=background_batch))

        bottom_label.append(pyglet.text.Label('Word ' + str(i+1) + ' Round ' + str(round_num + 1),
                                              font_name='Times New Roman',
                                              font_size=DEFAULT_TEXT_SIZE,
                                              x=START_BOX_POS[0]+(SMALL_BOX_WIDTH*i)+DEFAULT_TEXT_SIZE,
                                              y=START_BOX_POS[1]+(SMALL_BOX_HEIGHT/2)-(DEFAULT_TEXT_SIZE/2),
                                              batch=foreground_batch))
        bottom_label[i].color = BLACK_ALPHA
        bottom_box.append(shapes.BorderedRectangle(START_BOX_POS[0]+(SMALL_BOX_WIDTH*i), START_BOX_POS[1],
                                                   SMALL_BOX_WIDTH, SMALL_BOX_HEIGHT,
                                                   border=1,
                                                   color=WHITE,
                                                   border_color=BLACK,
                                                   batch=background_batch))

        arrow_start_x = START_BOX_POS[0]+(SMALL_BOX_WIDTH * i)+SMALL_BOX_WIDTH/2
        arrow_start_y = WINDOW_HEIGHT - START_BOX_POS[1] - SMALL_BOX_HEIGHT
        arrow_end_x = START_BOX_POS[0]+(SMALL_BOX_WIDTH*i)+SMALL_BOX_WIDTH/2
        arrow_end_y = START_BOX_POS[1]+SMALL_BOX_HEIGHT
        arrow.append(shapes.Line(arrow_start_x,
                                 arrow_start_y,
                                 arrow_end_x,
                                 arrow_end_y,
                                 width=LINE_NORMAL_SIZE,
                                 color=BLACK,
                                 batch=background_batch
                                 ))

        arrowheads.append(pyglet.graphics.vertex_list(3, ('v2f', [arrow_end_x, arrow_end_y,
                                                                  arrow_end_x-ARROW_NORMAL_SIZE,
                                                                  arrow_end_y+ARROW_NORMAL_SIZE,
                                                                  arrow_end_x+ARROW_NORMAL_SIZE,
                                                                  arrow_end_y+ARROW_NORMAL_SIZE])))

    @window.event
    def on_draw():
        window.clear()
        background_batch.draw()

        for curr_arrow in arrowheads:
            glColor3ub(*BLACK)
            curr_arrow.draw(GL_TRIANGLES)

        foreground_batch.draw()

    pyglet.app.run()


if __name__ == "__main__":
    draw_basic_picture(0)


