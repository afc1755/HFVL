import pyglet
from pyglet import shapes
from pyglet.gl import *

# constant value declarations
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

NAV_BOX_WIDTH = WINDOW_WIDTH
NAV_BOX_HEIGHT = 60
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50


SMALL_BOX_WIDTH = 120
SMALL_BOX_HEIGHT = 100
SMALL_BOX_BORDER_NORMAL = 2
SMALL_BOX_BORDER_BOLD = 4
START_BOX_POS = [10, 10]

WHITE = (255, 255, 255)
WHITE_ALPHA = (255, 255, 255, 255)
BLACK = (0, 0, 0)
BLACK_ALPHA = (0, 0, 0, 255)
GRAY = (120, 120, 120)
RED = (180, 0, 0)
GREEN = (0, 150, 0)
BLUE = (0, 0, 150)

DEFAULT_TEXT_SIZE = 10

ARROW_NORMAL_SIZE = 10
ARROW_BOLD_SIZE = 12
LINE_NORMAL_SIZE = 2
LINE_BOLD_SIZE = 4
SPEED_ARR = (0.25, 0.5, 1, 1.5, 2)

NEXT_BUTTON_X = WINDOW_WIDTH - (2 * BUTTON_WIDTH)
PREVIOUS_BUTTON_X = BUTTON_WIDTH
PLAY_BUTTON_X = WINDOW_WIDTH/2 - (BUTTON_WIDTH / 2)
BUTTON_Y = (NAV_BOX_HEIGHT - BUTTON_HEIGHT)/2


def run_frames(file_to_read):
    frames, b_batches, t_batches, f_batches = read_file(file_to_read)
    fd = FrameDisplayer(frames, b_batches, t_batches, f_batches, len(frames) - 1)
    pyglet.app.run()


class FrameDisplayer(pyglet.window.Window):

    def __init__(self, frames, b_batches, t_batches, f_batches, total_frames):
        super(FrameDisplayer, self).__init__(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.frames = frames
        self.frame_num = 0
        self.b_batches = b_batches
        self.t_batches = t_batches
        self.f_batches = f_batches
        self.total_frames = total_frames
        self.curr_speed = 0

    def next_frame(self):
        if self.frame_num == self.total_frames:
            print('Can\'t go past the last frame!')
        else:
            self.frame_num += 1
        print('next frame!')

    def previous_frame(self):
        if self.frame_num == 0:
            print('Can\'t go back past the first frame!')
        else:
            self.frame_num -= 1
        print('previous frame!')

    def play_frames(self):
        print('playing frames!')

    #@window.event
    def on_draw(self):
        dummy_arr = []

        self.clear()

        background = shapes.Rectangle(0, NAV_BOX_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - NAV_BOX_HEIGHT, color=WHITE,
                                      batch=self.b_batches[self.frame_num])
        nav_background = shapes.Rectangle(0, 0, WINDOW_WIDTH, NAV_BOX_HEIGHT, color=GRAY,
                                          batch=self.b_batches[self.frame_num])
        next_button = shapes.Rectangle(NEXT_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=self.b_batches[self.frame_num])
        previous_button = shapes.Rectangle(PREVIOUS_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                           batch=self.b_batches[self.frame_num])
        play_button = shapes.Rectangle(PLAY_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=self.b_batches[self.frame_num])
        next_button_text = pyglet.text.Label('Next',
                                             font_size=DEFAULT_TEXT_SIZE * 1.3,
                                             x=NEXT_BUTTON_X + DEFAULT_TEXT_SIZE * 3,
                                             y=BUTTON_Y + DEFAULT_TEXT_SIZE * 2,
                                             color=BLACK_ALPHA,
                                             batch=self.t_batches[self.frame_num])

        play_button_text = pyglet.text.Label('Play ' + str(SPEED_ARR[self.curr_speed]) + 'x',
                                             font_size=DEFAULT_TEXT_SIZE * 1.3,
                                             x=PLAY_BUTTON_X + DEFAULT_TEXT_SIZE * .75,
                                             y=BUTTON_Y + DEFAULT_TEXT_SIZE * 2,
                                             color=BLACK_ALPHA,
                                             batch=self.t_batches[self.frame_num])
        previous_button_text = pyglet.text.Label('Previous',
                                                 font_size=DEFAULT_TEXT_SIZE * 1.3,
                                                 x=PREVIOUS_BUTTON_X + DEFAULT_TEXT_SIZE * 1.5,
                                                 y=BUTTON_Y + DEFAULT_TEXT_SIZE * 2,
                                                 color=BLACK_ALPHA,
                                                 batch=self.t_batches[self.frame_num])

        self.b_batches[self.frame_num].draw()
        for curr_key in self.frames[self.frame_num]['box_dict']:
            curr_box = self.frames[self.frame_num]['box_dict'][curr_key]
            if curr_box[4] != '':
                dummy_arr.append(pyglet.text.Label(curr_box[4],
                                                   font_size=DEFAULT_TEXT_SIZE,
                                                   x=curr_box[0] + DEFAULT_TEXT_SIZE,
                                                   y=curr_box[1] + curr_box[3] / 2,
                                                   color=curr_box[6] + (255,),
                                                   batch=self.t_batches[self.frame_num]))
            dummy_arr.append(shapes.BorderedRectangle(curr_box[0], curr_box[1],
                                                      curr_box[2], curr_box[3],
                                                      border=SMALL_BOX_BORDER_BOLD if curr_box[5]
                                                      else SMALL_BOX_BORDER_NORMAL,
                                                      color=WHITE,
                                                      border_color=curr_box[6],
                                                      batch=self.f_batches[self.frame_num]))

        for arrow_key in self.frames[self.frame_num]['arrow_dict']:
            arrow = self.frames[self.frame_num]['arrow_dict'][arrow_key]
            dummy_arr.append(shapes.Line(arrow[0], arrow[1],
                                         arrow[2], arrow[3],
                                         width=LINE_BOLD_SIZE if arrow[4] else LINE_NORMAL_SIZE,
                                         color=arrow[5],
                                         batch=self.f_batches[self.frame_num]))
            glColor3ub(*arrow[5])
            if arrow[4]:
                arrowhead_thickness = ARROW_BOLD_SIZE
            else:
                arrowhead_thickness = ARROW_NORMAL_SIZE
            pyglet.graphics.vertex_list(3, ('v2f', [arrow[2], arrow[3],
                                                    arrow[2] - arrowhead_thickness,
                                                    arrow[3] + arrowhead_thickness,
                                                    arrow[2] + arrowhead_thickness,
                                                    arrow[3] + arrowhead_thickness])).draw(GL_TRIANGLES)

        self.f_batches[self.frame_num].draw()
        self.t_batches[self.frame_num].draw()

    #@window.event
    def on_mouse_press(self, x, y, button, modifiers):
        if NEXT_BUTTON_X <= x <= NEXT_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.next_frame()
        elif PREVIOUS_BUTTON_X <= x <= PREVIOUS_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.previous_frame()
        elif PLAY_BUTTON_X <= x <= PLAY_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.play_frames()


def read_file(file_to_read):
    frames = []

    background_batch = []
    foreground_batch = []
    text_batch = []

    lang_file = open(file_to_read)
    box_dict = {}
    arrow_dict = {}
    reading_frame_num = 0

    for line in lang_file:
        line = line.strip()
        if len(line) == 0:
            print('space here')
        elif line.strip().split(' ')[0].lower() != 'frame':
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
                    arrow_dict[start_box_id+end_box_id] = [x1, y1, x2, y2, arr_bold, user_arr_color]

                elif function_line[0] == '$modifyBox':
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
                    if (start_box_id + end_box_id) not in arrow_dict:
                        print('boxes not found for arrow to go between\nbox ids: ' + start_box_id + ' and ' + end_box_id)
                    if len(arrow_args) > 2:
                        for i in range(2, len(arrow_args)):
                            attribute_args = arrow_args[i].split('=')
                            if attribute_args[0].strip().lower() == 'bold':
                                if attribute_args[1].strip('\'').lower() == 'true':
                                    arrow_dict[start_box_id + end_box_id][4] = True
                                else:
                                    arrow_dict[start_box_id + end_box_id][4] = False
                            elif attribute_args[0].strip().lower() == 'color':
                                if attribute_args[1].strip('\'').lower() == 'blue':
                                    arrow_dict[start_box_id + end_box_id][5] = BLUE
                                elif attribute_args[1].strip('\'').lower() == 'green':
                                    arrow_dict[start_box_id + end_box_id][5] = GREEN
                                elif attribute_args[1].strip('\'').lower() == 'red':
                                    arrow_dict[start_box_id + end_box_id][5] = RED
                                else:
                                    print("invalid color used, defaulting to black\ncolor options are: blue, green, red")
            else:
                print('error while parsing\ninvalid function at line: \n\t' + line)
        elif line.strip().split(' ')[0].lower() == 'frame' and line.strip().split(' ')[1].lower() == 'end':
            frames.append({'box_dict': box_dict, 'arrow_dict': arrow_dict})
        else:
            box_dict = {}
            arrow_dict = {}
            reading_frame_num += 1
            foreground_batch.append(pyglet.graphics.Batch())
            background_batch.append(pyglet.graphics.Batch())
            text_batch.append(pyglet.graphics.Batch())
    return frames, background_batch, text_batch, foreground_batch


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
    run_frames('frameSHA')

