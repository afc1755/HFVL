import pyglet
from pyglet import shapes
from pyglet.gl import *

# constant value declarations
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SMALL_BOX_WIDTH = 120
SMALL_BOX_HEIGHT = 100
SMALL_BOX_BORDER_NORMAL = 2
SMALL_BOX_BORDER_BOLD = 4
START_BOX_POS = [10, 10]

WHITE = (255, 255, 255)
WHITE_ALPHA = (255, 255, 255, 255)
BLACK = (0, 0, 0)
BLACK_ALPHA = (0, 0, 0, 255)
RED = (180, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 150)

DEFAULT_TEXT_SIZE = 10

ARROW_NORMAL_SIZE = 10
ARROW_BOLD_SIZE = 12
LINE_NORMAL_SIZE = 2
LINE_BOLD_SIZE = 4


def read_file(file_to_read):
    box_dict = {}
    arrowline_dict = {}
    arrowheads = []
    arrow_color = []
    dummy_arr = []

    window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
    background_batch = pyglet.graphics.Batch()
    foreground_batch = pyglet.graphics.Batch()
    text_batch = pyglet.graphics.Batch()
    background = shapes.Rectangle(0, 0, 1200, 800, color=(255, 255, 255), batch=background_batch)
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
                user_box_color = BLACK
                box_bold = False

                if len(box_args) > 5:
                    for i in range(5, len(box_args)):
                        attribute_args = box_args[i].split('=')
                        if attribute_args[0].strip().lower() == 'text':
                            box_text = attribute_args[1].replace('\'', '')
                        if attribute_args[0].strip().lower() == 'bold':
                            if attribute_args[1].strip('\'').lower() == 'true':
                                box_bold = True
                            else:
                                box_bold = False
                        elif attribute_args[0].strip().lower() == 'color':
                            if attribute_args[1].strip('\'').lower() == 'blue':
                                user_box_color = BLUE
                            elif attribute_args[1].strip('\'').lower() == 'green':
                                user_box_color = GREEN
                            elif attribute_args[1].strip('\'').lower() == 'red':
                                user_box_color = RED
                            else:
                                print("invalid color used, defaulting to black\ncolor options are: blue, green, red")
                box_dict[box_id] = [x, y, width, height, box_text, box_bold, user_box_color]
            elif function_line[0] == '$drawArrow':
                arrow_args = function_line[1].split(',')
                start_box_id = arrow_args[0].replace('\'', '')
                end_box_id = arrow_args[1].replace('\'', '')
                arr_bold = False
                user_arr_color = BLACK

                if len(arrow_args) > 2:
                    for i in range(2, len(arrow_args)):
                        attribute_args = arrow_args[i].split('=')
                        if attribute_args[0].strip().lower() == 'bold':
                            if attribute_args[1].strip('\'').lower() == 'true':
                                arr_bold = True
                            else:
                                arr_bold = False
                        elif attribute_args[0].strip().lower() == 'color':
                            if attribute_args[1].strip('\'').lower() == 'blue':
                                user_arr_color = BLUE
                            elif attribute_args[1].strip('\'').lower() == 'green':
                                user_arr_color = GREEN
                            elif attribute_args[1].strip('\'').lower() == 'red':
                                user_arr_color = RED
                            else:
                                print("invalid color used, defaulting to black\ncolor options are: blue, green, red")
                x1, y1, x2, y2 = pathfind_arrow(box_dict[start_box_id], box_dict[end_box_id])

                arrow_color.append(user_arr_color)
                arrowline_dict[start_box_id+end_box_id] = [x1, y1, x2, y2, arr_bold, user_arr_color]

            elif function_line[0] == '$modifyBox':
                box_text = ''
                box_args = function_line[1].split(',')
                box_id = box_args[0].replace('\'', '').strip()
                if box_id not in box_dict:
                    print('error: no such box as ' + box_id)
                for i in range(1, len(box_args)):
                    attribute_args = box_args[i].split('=')
                    if attribute_args[0].strip().lower() == 'text':
                        box_dict[box_id][4] = attribute_args[1].replace('\'', '')
                    if attribute_args[0].strip().lower() == 'bold':
                        if attribute_args[1].strip('\'').lower() == 'true':
                            box_dict[box_id][5] = True
                        else:
                            box_dict[box_id][5] = False
                    elif attribute_args[0].strip().lower() == 'color':
                        if attribute_args[1].strip('\'').lower() == 'blue':
                            box_dict[box_id][6] = BLUE
                        elif attribute_args[1].strip('\'').lower() == 'green':
                            box_dict[box_id][6] = GREEN
                        elif attribute_args[1].strip('\'').lower() == 'red':
                            box_dict[box_id][6] = RED
                        else:
                            print("invalid color used, defaulting to black\ncolor options are: blue, green, red")

            elif function_line[0] == '$modifyArrow':
                arrow_args = function_line[1].split(',')
                start_box_id = arrow_args[0].replace('\'', '')
                end_box_id = arrow_args[1].replace('\'', '')
                if (start_box_id + end_box_id) not in arrowline_dict:
                    print('boxes not found for arrow to go between\nbox ids: ' + start_box_id + ' and ' + end_box_id)
                if len(arrow_args) > 2:
                    for i in range(2, len(arrow_args)):
                        attribute_args = arrow_args[i].split('=')
                        if attribute_args[0].strip().lower() == 'bold':
                            if attribute_args[1].strip('\'').lower() == 'true':
                                arrowline_dict[start_box_id + end_box_id][4] = True
                            else:
                                arrowline_dict[start_box_id + end_box_id][4] = False
                        elif attribute_args[0].strip().lower() == 'color':
                            if attribute_args[1].strip('\'').lower() == 'blue':
                                arrowline_dict[start_box_id + end_box_id][5] = BLUE
                            elif attribute_args[1].strip('\'').lower() == 'green':
                                arrowline_dict[start_box_id + end_box_id][5] = GREEN
                            elif attribute_args[1].strip('\'').lower() == 'red':
                                arrowline_dict[start_box_id + end_box_id][5] = RED
                            else:
                                print("invalid color used, defaulting to black\ncolor options are: blue, green, red")
            else:
                print('error while parsing\ninvalid function at line: \n\t' + line)

    @window.event
    def on_draw():
        window.clear()
        background_batch.draw()
        for curr_box in box_dict:
            if box_dict[curr_box][4] != '':
                dummy_arr.append(pyglet.text.Label(box_dict[curr_box][4],
                                                   font_size=DEFAULT_TEXT_SIZE,
                                                   x=box_dict[curr_box][0] + DEFAULT_TEXT_SIZE,
                                                   y=box_dict[curr_box][1] + box_dict[curr_box][3] / 2,
                                                   color=box_dict[curr_box][6] + (255,),
                                                   batch=text_batch))
            dummy_arr.append(shapes.BorderedRectangle(box_dict[curr_box][0], box_dict[curr_box][1],
                                                      box_dict[curr_box][2], box_dict[curr_box][3],
                                                      border=SMALL_BOX_BORDER_BOLD if box_dict[curr_box][5]
                                                      else SMALL_BOX_BORDER_NORMAL,
                                                      color=WHITE,
                                                      border_color=box_dict[curr_box][6],
                                                      batch=foreground_batch))

        for arrowline in arrowline_dict:
            dummy_arr.append(shapes.Line(arrowline_dict[arrowline][0], arrowline_dict[arrowline][1],
                                         arrowline_dict[arrowline][2], arrowline_dict[arrowline][3],
                                         width=LINE_BOLD_SIZE if arrowline_dict[arrowline][4] else LINE_NORMAL_SIZE,
                                         color=arrowline_dict[arrowline][5],
                                         batch=foreground_batch))
            glColor3ub(*arrowline_dict[arrowline][5])
            if arrowline_dict[arrowline][4]:
                arrowhead_thickness = ARROW_BOLD_SIZE
            else:
                arrowhead_thickness = ARROW_NORMAL_SIZE
            pyglet.graphics.vertex_list(3, ('v2f', [arrowline_dict[arrowline][2], arrowline_dict[arrowline][3],
                                                    arrowline_dict[arrowline][2] - arrowhead_thickness,
                                                    arrowline_dict[arrowline][3] + arrowhead_thickness,
                                                    arrowline_dict[arrowline][2] + arrowhead_thickness,
                                                    arrowline_dict[arrowline][3] + arrowhead_thickness])).draw(GL_TRIANGLES)

        foreground_batch.draw()
        text_batch.draw()

        """for curr_arrow in range(0, len(arrowheads)):
            glColor3ub(*arrow_color[curr_arrow])
            arrowheads[curr_arrow].draw(GL_TRIANGLES)"""

    pyglet.app.run()


def pathfind_arrow(start_box, end_box):
    x1 = start_box[0] + start_box[2] / 2
    y1 = start_box[1] + start_box[3]
    x2 = end_box[0] + end_box[2] / 2
    y2 = end_box[1] + end_box[3]

    xdiff = x1 - x2
    ydiff = y1 - y2

    if abs(xdiff) > abs(ydiff):
        if xdiff < 0:
            x1 = x1 + (start_box[2] / 2)
            x2 = x2 - (end_box[2] / 2)
            y1 = y1 - (start_box[3] / 2)
            y2 = y2 - (end_box[3] / 2)
        else:
            x1 = x1 - start_box[2] / 2
            x2 = x2 + end_box[2] / 2
            y1 = y1 - start_box[3] / 2
            y2 = y2 - end_box[3] / 2
    else:
        if ydiff < 0:
            y2 = y2 - end_box[3]
        else:
            y1 = y1 - start_box[3]

    return x1, y1, x2, y2


if __name__ == "__main__":
    read_file('sampleSHA')


