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
ARROW_BOLD_SIZE = 12
LINE_NORMAL_SIZE = 1
LINE_BOLD_SIZE = 2


def read_file(file_to_read):
    box_dict = {}
    arrowheads = []
    dummy_arr = []

    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    background_batch = pyglet.graphics.Batch()
    foreground_batch = pyglet.graphics.Batch()
    text_batch = pyglet.graphics.Batch()
    background = shapes.Rectangle(0, 0, 800, 600, color=(255, 255, 255), batch=background_batch)
    lang_file = open(file_to_read)

    for line in lang_file:
        if line[0] == '$':
            function_line = line.replace(')', '').replace('\n', '').split('(')
            if function_line[0] == '$drawBox':
                box_text = ''
                box_args = function_line[1].split(',')
                box_id = box_args[0].replace('\'', '')
                x = int(box_args[1])
                y = int(box_args[2])
                width = int(box_args[3])
                height = int(box_args[4])

                if len(box_args) > 5:
                    for i in range(5, len(box_args)):
                        attribute_args = box_args[i].split('=')
                        if attribute_args[0] == 'text':
                            box_text = attribute_args[1].replace('\'', '')

                dummy_arr = draw_box(x, y, width, height, foreground_batch, text_batch, box_text, dummy_arr)
                box_dict[box_id] = [x, y, width, height]

            elif function_line[0] == '$drawArrow':
                arrow_args = function_line[1].split(',')
                start_box_id = arrow_args[0].replace('\'', '')
                end_box_id = arrow_args[1].replace('\'', '')
                bold = False

                if len(arrow_args) > 2:
                    for i in range(2, len(arrow_args)):
                        attribute_args = arrow_args[i].split('=')
                        if attribute_args[0] == 'bold':
                            if attribute_args[1].strip('\'') == 'True':
                                bold = True
                            else:
                                bold = False

                x1 = box_dict[start_box_id][0] + box_dict[start_box_id][2]/2
                y1 = box_dict[start_box_id][1] + box_dict[start_box_id][3]
                x2 = box_dict[end_box_id][0] + box_dict[end_box_id][2] / 2
                y2 = box_dict[end_box_id][1] + box_dict[end_box_id][3]
                arrowheads.append(draw_arrow(x1, y1, x2, y2, bold, foreground_batch, dummy_arr))

            else:
                print('error while parsing\ninvalid function at line: \n\t' + line)

    @window.event
    def on_draw():
        window.clear()
        background_batch.draw()
        foreground_batch.draw()
        text_batch.draw()

        glColor3ub(*BLACK)
        for curr_arrow in arrowheads:
            curr_arrow.draw(GL_TRIANGLES)

    pyglet.app.run()


def draw_box(x, y, width, height, use_batch, text_batch, text, dummy_arr):
    if text != '':
        dummy_arr.append(pyglet.text.Label(text,
                                           font_size=DEFAULT_TEXT_SIZE,
                                           x=x + DEFAULT_TEXT_SIZE,
                                           y=y + height/2,
                                           color=BLACK_ALPHA,
                                           batch=text_batch))

    dummy_arr.append(shapes.BorderedRectangle(x, y,
                                              width, height,
                                              border=1,
                                              color=WHITE,
                                              border_color=BLACK,
                                              batch=use_batch))
    return dummy_arr


def draw_arrow(x1, y1, x2, y2, bold, use_batch, dummy_arr):
    if bold:
        dummy_arr.append(shapes.Line(x1, y1,
                                     x2, y2,
                                     width=LINE_BOLD_SIZE,
                                     color=BLACK,
                                     batch=use_batch))
        return pyglet.graphics.vertex_list(3, ('v2f', [x2, y2,
                                                       x2 - ARROW_BOLD_SIZE, y2 + ARROW_BOLD_SIZE,
                                                       x2 + ARROW_BOLD_SIZE, ARROW_BOLD_SIZE]))
    else:
        dummy_arr.append(shapes.Line(x1, y1,
                                     x2, y2,
                                     width=LINE_NORMAL_SIZE,
                                     color=BLACK,
                                     batch=use_batch))
        return pyglet.graphics.vertex_list(3, ('v2f', [x2, y2,
                                                       x2 - ARROW_NORMAL_SIZE, y2 + ARROW_NORMAL_SIZE,
                                                       x2 + ARROW_NORMAL_SIZE, y2 + ARROW_NORMAL_SIZE]))


if __name__ == "__main__":
    read_file('small_env')


