import pyglet
from pyglet import shapes
from pyglet import clock
from pyglet.gl import *
import time
import copy

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
TEXT_SPEED_ARR = ('1/4', '1/2', '1', '1.5', '2')

NEXT_BUTTON_X = WINDOW_WIDTH - (2 * BUTTON_WIDTH)
PREVIOUS_BUTTON_X = BUTTON_WIDTH
PLAY_BUTTON_X = 1.15 * WINDOW_WIDTH / 3 - (BUTTON_WIDTH / 2)
STOP_BUTTON_X = WINDOW_WIDTH / 2 - (BUTTON_WIDTH / 2)
RESTART_BUTTON_X = 1.85 * WINDOW_WIDTH / 3 - (BUTTON_WIDTH / 2)
BUTTON_Y = (NAV_BOX_HEIGHT - BUTTON_HEIGHT) / 2


def run_frames(file_to_read):
    frames = read_file(file_to_read)
    fd = FrameDisplayer(frames, len(frames) - 1)
    pyglet.app.run()


class FrameDisplayer(pyglet.window.Window):
    def __init__(self, frames, total_frames):
        super(FrameDisplayer, self).__init__(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.frames = frames
        self.frame_num = 0
        self.total_frames = total_frames
        self.curr_speed = 0
        self.is_playing = False
        self.time_diff = 0
        self.old_time = time.time()

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
        clock.unschedule(self.call_draw)
        clock.schedule_interval(self.call_draw, (1.5 / SPEED_ARR[self.curr_speed]))
        if self.is_playing:
            if self.curr_speed > 3:
                self.curr_speed = 0
            else:
                self.curr_speed += 1
        self.is_playing = True
        print('playing frames at ' + str(SPEED_ARR[self.curr_speed]) + 'x speed')

    def call_draw(self, dt):
        self.on_draw()

    def stop_frames(self):
        clock.unschedule(self.call_draw)
        self.is_playing = False
        print('stopping frames!')

    def restart(self):
        self.frame_num = 0
        print('restarting frames!')

    def on_draw(self):
        dummy_arr = []
        if self.is_playing and (time.time() - self.old_time) + self.time_diff >= (0.8 / SPEED_ARR[self.curr_speed]):
            self.next_frame()
            self.time_diff = 0
            self.old_time = time.time()

        self.clear()
        b_batch = pyglet.graphics.Batch()
        t_batch = pyglet.graphics.Batch()
        f_batch = pyglet.graphics.Batch()
        background = shapes.Rectangle(0, NAV_BOX_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT - NAV_BOX_HEIGHT, color=WHITE,
                                      batch=b_batch)
        nav_background = shapes.Rectangle(0, 0, WINDOW_WIDTH, NAV_BOX_HEIGHT, color=GRAY,
                                          batch=b_batch)
        next_button = shapes.Rectangle(NEXT_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=b_batch)
        previous_button = shapes.Rectangle(PREVIOUS_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                           batch=b_batch)
        play_button = shapes.Rectangle(PLAY_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=b_batch)
        stop_button = shapes.Rectangle(STOP_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=b_batch)
        restart_button = shapes.Rectangle(RESTART_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                          batch=b_batch)
        next_button_text = pyglet.text.Label('Next',
                                             font_size=DEFAULT_TEXT_SIZE * 1.3,
                                             x=NEXT_BUTTON_X + DEFAULT_TEXT_SIZE * 3,
                                             y=BUTTON_Y + DEFAULT_TEXT_SIZE * 2,
                                             color=BLACK_ALPHA,
                                             batch=t_batch)

        if self.is_playing:
            play_button_text = pyglet.text.Label('Playing @ ' + TEXT_SPEED_ARR[self.curr_speed] + 'x',
                                                 font_size=DEFAULT_TEXT_SIZE,
                                                 x=PLAY_BUTTON_X + DEFAULT_TEXT_SIZE * .25,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .5),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        else:
            play_button_text = pyglet.text.Label('Play @ ' + TEXT_SPEED_ARR[self.curr_speed] + 'x',
                                                 font_size=DEFAULT_TEXT_SIZE,
                                                 x=PLAY_BUTTON_X + DEFAULT_TEXT_SIZE * 1.2,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .5),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)

        previous_button_text = pyglet.text.Label('Previous',
                                                 font_size=DEFAULT_TEXT_SIZE * 1.3,
                                                 x=PREVIOUS_BUTTON_X + DEFAULT_TEXT_SIZE * 1.5,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        stop_button_text = pyglet.text.Label('Stop',
                                             font_size=DEFAULT_TEXT_SIZE * 1.3,
                                             x=STOP_BUTTON_X + DEFAULT_TEXT_SIZE * 3,
                                             y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                             color=BLACK_ALPHA,
                                             batch=t_batch)

        restart_button_text = pyglet.text.Label('Restart',
                                                font_size=DEFAULT_TEXT_SIZE * 1.3,
                                                x=RESTART_BUTTON_X + DEFAULT_TEXT_SIZE * 2.1,
                                                y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                color=BLACK_ALPHA,
                                                batch=t_batch)

        frame_text = pyglet.text.Label('Frame ' + str(self.frame_num) + '/' + str(self.total_frames),
                                       font_name='Courier',
                                       font_size=DEFAULT_TEXT_SIZE,
                                       x=DEFAULT_TEXT_SIZE/4,
                                       y=WINDOW_HEIGHT - DEFAULT_TEXT_SIZE,
                                       color=BLACK_ALPHA,
                                       batch=t_batch)

        b_batch.draw()
        for curr_key in self.frames[self.frame_num]['box_dict']:
            curr_box = self.frames[self.frame_num]['box_dict'][curr_key]
            if curr_box[4] != '':
                dummy_arr.append(pyglet.text.Label(curr_box[4],
                                                   font_size=DEFAULT_TEXT_SIZE,
                                                   x=curr_box[0] + DEFAULT_TEXT_SIZE,
                                                   y=curr_box[1] + curr_box[3] / 2,
                                                   color=curr_box[6] + (255,),
                                                   batch=t_batch))
            dummy_arr.append(shapes.BorderedRectangle(curr_box[0], curr_box[1],
                                                      curr_box[2], curr_box[3],
                                                      border=SMALL_BOX_BORDER_BOLD if curr_box[5]
                                                      else SMALL_BOX_BORDER_NORMAL,
                                                      color=WHITE,
                                                      border_color=curr_box[6],
                                                      batch=f_batch))

        for arrow_key in self.frames[self.frame_num]['arrow_dict']:
            arrow = self.frames[self.frame_num]['arrow_dict'][arrow_key]
            for arrow_line in arrow[0]:
                dummy_arr.append(shapes.Line(arrow_line[0], arrow_line[1],
                                             arrow_line[2], arrow_line[3],
                                             width=LINE_BOLD_SIZE if arrow[1] else LINE_NORMAL_SIZE,
                                             color=arrow[2],
                                             batch=f_batch))
            glColor3ub(*arrow[2])
            if arrow[1]:
                arrowhead_thickness = ARROW_BOLD_SIZE
            else:
                arrowhead_thickness = ARROW_NORMAL_SIZE
            pyglet.graphics.vertex_list(3, ('v2f', create_arrowhead(arrow, arrowhead_thickness))).draw(GL_TRIANGLES)

        f_batch.draw()
        t_batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if NEXT_BUTTON_X <= x <= NEXT_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.next_frame()
        elif PREVIOUS_BUTTON_X <= x <= PREVIOUS_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.previous_frame()
        elif PLAY_BUTTON_X <= x <= PLAY_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.play_frames()
        elif STOP_BUTTON_X <= x <= STOP_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.stop_frames()
        elif RESTART_BUTTON_X <= x <= RESTART_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.restart()


def read_file(file_to_read):
    frames = []

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
                                elif attribute_args[1].strip('\'').lower() == 'black':
                                    user_box_color = BLACK
                                else:
                                    print(
                                        "invalid color used, defaulting to black\ncolor options are: blue, green, red")
                    box_dict[box_id] = [x, y, width, height, box_text, box_bold, user_box_color]
                elif function_line[0] == '$drawArrow':
                    arrow_args = function_line[1].split(',')
                    start_box_id = arrow_args[0].strip().replace('\'', '')
                    end_box_id = arrow_args[1].strip().replace('\'', '')
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
                                elif attribute_args[1].strip('\'').lower() == 'black':
                                    user_arr_color = BLACK
                                else:
                                    print(
                                        "invalid color used, defaulting to black\ncolor options are: blue, green, red")
                    arrow_coords = pathfind_arrow(box_dict, start_box_id, end_box_id, arrow_dict)
                    arrow_dict[start_box_id + end_box_id] = [arrow_coords, arr_bold, user_arr_color,
                                                             start_box_id, end_box_id]

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
                            elif attribute_args[1].strip('\'').lower() == 'black':
                                box_dict[box_id][6] = BLACK
                            else:
                                print("invalid color used, defaulting to black\ncolor options are: blue, green, red")

                elif function_line[0] == '$modifyArrow':
                    arrow_args = function_line[1].split(',')
                    start_box_id = arrow_args[0].replace('\'', '')
                    end_box_id = arrow_args[1].replace('\'', '')
                    if (start_box_id + end_box_id) not in arrow_dict:
                        print(
                            'boxes not found for arrow to go between\nbox ids: ' + start_box_id + ' and ' + end_box_id)
                    if len(arrow_args) > 2:
                        for i in range(2, len(arrow_args)):
                            attribute_args = arrow_args[i].split('=')
                            if attribute_args[0].strip().lower() == 'bold':
                                if attribute_args[1].strip('\'').lower() == 'true':
                                    arrow_dict[start_box_id + end_box_id][1] = True
                                else:
                                    arrow_dict[start_box_id + end_box_id][1] = False
                            elif attribute_args[0].strip().lower() == 'color':
                                if attribute_args[1].strip('\'').lower() == 'blue':
                                    arrow_dict[start_box_id + end_box_id][2] = BLUE
                                elif attribute_args[1].strip('\'').lower() == 'green':
                                    arrow_dict[start_box_id + end_box_id][2] = GREEN
                                elif attribute_args[1].strip('\'').lower() == 'red':
                                    arrow_dict[start_box_id + end_box_id][2] = RED
                                elif attribute_args[1].strip('\'').lower() == 'black':
                                    arrow_dict[start_box_id + end_box_id][2] = BLACK
                                else:
                                    print(
                                        "invalid color used, defaulting to black\ncolor options are: blue, green, red")
            else:
                print('error while parsing\ninvalid function at line: \n\t' + line)
        elif line.strip().split(' ')[0].lower() == 'frame' and line.strip().split(' ')[1].lower() == 'end':
            frames.append({'box_dict': box_dict, 'arrow_dict': arrow_dict})
        else:
            old_box_dict = box_dict
            old_arrow_dict = arrow_dict
            box_dict = copy.deepcopy(old_box_dict)
            arrow_dict = copy.deepcopy(old_arrow_dict)
            reading_frame_num += 1
    return frames


def pathfind_arrow(box_dict, start_box_id, end_box_id, arrow_dict):
    start_box = box_dict[start_box_id]
    end_box = box_dict[end_box_id]
    x1 = start_box[0]
    y1 = start_box[1]

    if start_box[0] < end_box[0]:
        xdiff = start_box[0] + (start_box[2] - end_box[0])
    elif start_box[0] > end_box[0]:
        xdiff = start_box[0] - (end_box[0] + end_box[2])
    else:
        xdiff = 0
    if start_box[1] > end_box[1]:
        ydiff = start_box[1] - (end_box[1] + end_box[3])
    elif start_box[1] < end_box[1]:
        ydiff = start_box[1] + (start_box[3] - end_box[1])
    else:
        ydiff = 0

    bigx = abs(xdiff) > abs(ydiff)

    if abs(xdiff) > abs(ydiff):
        if xdiff > 0:
            desiredx = end_box[0] + end_box[2]
            y1 = y1 + start_box[3] / 2
            desiredy = end_box[1] + (end_box[3] / 2)
        else:
            x1 = x1 + start_box[2]
            desiredx = end_box[0]
            y1 = y1 + start_box[3] / 2
            desiredy = end_box[1] + (end_box[3] / 2)
    else:
        if ydiff > 0:
            x1 = x1 + start_box[2] / 2
            desiredy = end_box[1] + end_box[3]
            desiredx = end_box[0] + end_box[2] / 2
        else:
            x1 = x1 + start_box[2] / 2
            y1 = y1 + start_box[3]
            desiredx = end_box[0] + end_box[2] / 2
            desiredy = end_box[1]

    oldx = x1
    oldy = y1

    currx = x1
    curry = y1

    vert_list = []
    displacement = True
    lasty = False

    while currx != desiredx or curry != desiredy:
        if displacement:
            displacement = False
            if bigx:
                currx = (desiredx + currx) / 2
                curry = oldy
                lasty = False
            else:
                curry = (desiredy + curry) / 2
                currx = oldx
                lasty = True

        elif lasty and currx - desiredx != 0:
            currx = desiredx
            curry = oldy
            lasty = False
        else:
            curry = desiredy
            currx = oldx
            lasty = True

        vert_list.append([oldx, oldy, currx, curry])
        oldx = currx
        oldy = curry

    return vert_list


def create_arrowhead(arrow, arrowhead_thickness):
    arrow_lines = arrow[0]
    startx = arrow_lines[-1][0]
    starty = arrow_lines[-1][1]
    endx = arrow_lines[-1][2]
    endy = arrow_lines[-1][3]

    points = [endx, endy]
    diffx = endx - startx
    diffy = endy - starty

    if diffx < 0 and diffy == 0:
        points.extend([endx + arrowhead_thickness,
                       endy - arrowhead_thickness,
                       endx + arrowhead_thickness,
                       endy + arrowhead_thickness])
    elif diffx > 0 and diffy == 0:
        points.extend([endx - arrowhead_thickness,
                       endy + arrowhead_thickness,
                       endx - arrowhead_thickness,
                       endy - arrowhead_thickness])
    elif diffx == 0 and diffy < 0:
        points.extend([endx - arrowhead_thickness,
                       endy + arrowhead_thickness,
                       endx + arrowhead_thickness,
                       endy + arrowhead_thickness])
    elif diffx == 0 and diffy > 0:
        points.extend([endx + arrowhead_thickness,
                       endy - arrowhead_thickness,
                       endx - arrowhead_thickness,
                       endy - arrowhead_thickness])
    else:
        print('Bad Last Arrow: Code Error!' + str(arrow))
    return points


if __name__ == "__main__":
    run_frames('fullShaStartFrame')
