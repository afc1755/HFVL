from pyglet import shapes
from pyglet import clock
from pyglet.gl import *
from hashConstants import *
import time
import smallParserBoxAndArrow


class FrameDisplayer(pyglet.window.Window):
    def __init__(self, frames, total_frames, round_splits):
        super(FrameDisplayer, self).__init__(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.frames = frames
        self.frame_num = 0
        self.total_frames = total_frames
        self.curr_speed = 5
        self.is_playing = False
        self.old_time = time.time()
        self.round_splits = round_splits

    def load_new_window(self, file_name, window_args):
        prev_window_dict = {}
        for window_arg in window_args:
            try:
                prev_window_dict[window_arg] = self.frames[self.frame_num]['box_dict'][window_arg][4]
            except KeyError:
                print('issues with argument from current window to function window for window arg: ' + window_arg)
        smallParserBoxAndArrow.run_frames(file_name, prev_window_dict)

    def next_frame(self):
        if self.frame_num == self.total_frames - 1:
            print('Can\'t go past the last frame!')
            if self.is_playing:
                self.start_stop_frames()
        else:
            self.frame_num += 1
        print('next frame!')

    def previous_frame(self):
        if self.frame_num == 0:
            print('Can\'t go back past the first frame!')
        else:
            self.frame_num -= 1
        print('previous frame!')

    def next_round(self):
        for i in range(0, len(self.round_splits)):
            if self.round_splits[i] > self.frame_num:
                self.frame_num = self.round_splits[i]
                break
            if i == (len(self.round_splits) - 1):
                print('already on the last round!')

    def previous_round(self):
        if self.round_splits[0] >= self.frame_num:
            print('already on the first round!')
        else:
            for i in range(0, len(self.round_splits)):
                if self.round_splits[i] >= self.frame_num:
                    if i != 0:
                        self.frame_num = self.round_splits[i - 1]
                        break
                if (i + 1) == len(self.round_splits):
                    self.frame_num = self.round_splits[i]

    def call_draw(self, dt):
        self.on_draw()

    def increase_speed(self):
        if self.curr_speed >= (len(SPEED_ARR) - 1):
            print('Can\'t go past top speed!')
        else:
            print('increasing speed...')
            self.curr_speed += 1

    def decrease_speed(self):
        if self.curr_speed <= 0:
            print('Can\'t go below bottom speed!')
        else:
            print('decreasing speed...')
            self.curr_speed -= 1

    def start_stop_frames(self):
        if self.is_playing:
            clock.unschedule(self.call_draw)
            self.is_playing = False
            print('stopping frames!')
        else:
            clock.unschedule(self.call_draw)
            clock.schedule(self.call_draw)
            self.is_playing = True
            print('playing frames at ' + str(SPEED_ARR[self.curr_speed]) + 'x speed')

    def restart(self):
        self.frame_num = 0
        print('restarting frames!')

    def on_draw(self):
        dummy_arr = []
        if self.is_playing and (time.time() - self.old_time) >= (2.0 / SPEED_ARR[self.curr_speed]):
            self.next_frame()
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
        next_f_button = shapes.Rectangle(NEXT_F_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                         batch=b_batch)
        previous_f_button = shapes.Rectangle(PREVIOUS_F_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                             batch=b_batch)
        play_pause_button = shapes.Rectangle(PLAY_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                             batch=b_batch)
        faster_up_button = shapes.Rectangle(FAST_BUTTON_X, BUTTON_Y, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                            batch=b_batch)
        slower_button = shapes.Rectangle(SLOW_BUTTON_X, BUTTON_Y, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                         batch=b_batch)
        restart_button = shapes.Rectangle(RESTART_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                          batch=b_batch)

        title_text_len = 16 * len(self.frames[self.frame_num]['global_dict']['title'][0])
        if WINDOW_WIDTH > title_text_len:
            x_displacement = WINDOW_WIDTH/2 - (8 * len(self.frames[self.frame_num]['global_dict']['title'][0]))
        else:
            x_displacement = DEFAULT_TEXT_SIZE * 2
        title_text = pyglet.text.Label(self.frames[self.frame_num]['global_dict']['title'][0],
                                       font_name=FONT_FAMILY,
                                       font_size=TITLE_TEXT_SIZE,
                                       x=x_displacement,
                                       y=TITLE_Y,
                                       color=self.frames[self.frame_num]['global_dict']['title'][1] + (255,),
                                       batch=t_batch)
        if self.is_playing:
            play_button_text = pyglet.text.Label('Stop',
                                                 font_name=FONT_FAMILY,
                                                 font_size=BUTTON_TEXT_SIZE,
                                                 bold=True,
                                                 x=PLAY_BUTTON_X + DEFAULT_TEXT_SIZE * 3,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        else:
            play_button_text = pyglet.text.Label('Play',
                                                 font_name=FONT_FAMILY,
                                                 font_size=BUTTON_TEXT_SIZE,
                                                 bold=True,
                                                 x=PLAY_BUTTON_X + DEFAULT_TEXT_SIZE * 2.8,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        slow_button_text = pyglet.text.Label('<<',
                                             font_name=FONT_FAMILY,
                                             font_size=BUTTON_TEXT_SIZE,
                                             bold=True,
                                             x=SLOW_BUTTON_X + DEFAULT_TEXT_SIZE * 1.5,
                                             y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                             color=BLACK_ALPHA,
                                             batch=t_batch)
        fast_button_text = pyglet.text.Label('>>',
                                             font_name=FONT_FAMILY,
                                             font_size=BUTTON_TEXT_SIZE,
                                             bold=True,
                                             x=FAST_BUTTON_X + DEFAULT_TEXT_SIZE * 1.5,
                                             y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                             color=BLACK_ALPHA,
                                             batch=t_batch)
        previous_button_text = pyglet.text.Label('Previous',
                                                 font_name=FONT_FAMILY,
                                                 font_size=BUTTON_TEXT_SIZE,
                                                 bold=True,
                                                 x=PREVIOUS_BUTTON_X + DEFAULT_TEXT_SIZE * 0.6,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        next_button_text = pyglet.text.Label('Next',
                                             font_name=FONT_FAMILY,
                                             font_size=BUTTON_TEXT_SIZE,
                                             bold=True,
                                             x=NEXT_BUTTON_X + DEFAULT_TEXT_SIZE * 2.8,
                                             y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                             color=BLACK_ALPHA,
                                             batch=t_batch)
        previous_f_button_text = pyglet.text.Label('Round <',
                                                 font_name=FONT_FAMILY,
                                                 font_size=BUTTON_TEXT_SIZE,
                                                 bold=True,
                                                 x=PREVIOUS_F_BUTTON_X + DEFAULT_TEXT_SIZE * 1.2,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        next_f_button_text = pyglet.text.Label('Round >',
                                             font_name=FONT_FAMILY,
                                             font_size=BUTTON_TEXT_SIZE,
                                             bold=True,
                                             x=NEXT_F_BUTTON_X + DEFAULT_TEXT_SIZE * 1.2,
                                             y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                             color=BLACK_ALPHA,
                                             batch=t_batch)
        restart_button_text = pyglet.text.Label('Restart',
                                                font_name=FONT_FAMILY,
                                                font_size=BUTTON_TEXT_SIZE,
                                                bold=True,
                                                x=RESTART_BUTTON_X + DEFAULT_TEXT_SIZE * 1.2,
                                                y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                color=BLACK_ALPHA,
                                                batch=t_batch)
        if self.frames[self.frame_num]['global_dict']['frame_count_visible']:
            if self.total_frames > 1000:
                f_font_size = 11
            else:
                f_font_size = BUTTON_TEXT_SIZE
            if self.frame_num > 99:
                f_buffer = 5
            else:
                f_buffer = 0
            frame_text = pyglet.text.Label('Frame ' + str(self.frame_num + 1) + '/' + str(self.total_frames),
                                           font_name=FONT_FAMILY,
                                           font_size=f_font_size,
                                           bold=True,
                                           x=FRAME_INFO_X - f_buffer,
                                           y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                           color=WHITE_ALPHA,
                                           batch=t_batch)
            speed_text = pyglet.text.Label('Speed: ' + str(TEXT_SPEED_ARR[self.curr_speed]),
                                           font_name=FONT_FAMILY,
                                           font_size=f_font_size,
                                           x=SPEED_INFO_X + f_buffer,
                                           bold=True,
                                           y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                           color=WHITE_ALPHA,
                                           batch=t_batch)

        b_batch.draw()
        for curr_key in self.frames[self.frame_num]['box_dict']:
            curr_box = self.frames[self.frame_num]['box_dict'][curr_key]
            if curr_box[4] != '':
                word_size = DEFAULT_TEXT_SIZE * 0.8 * len(curr_box[4])
                if word_size > curr_box[2]:
                    split = curr_box[2]//(DEFAULT_TEXT_SIZE * 0.9)
                    last_word_index = 0
                    full_text = curr_box[4]
                    curr_y_displacement = 0
                    start_line_index = 0
                    for curr_text_index in range(0, len(full_text)):
                        curr_char = full_text[curr_text_index]
                        if curr_char == ' ' or curr_char == '\\':
                            last_word_index = curr_text_index
                        if curr_char == '\\' or (curr_text_index - start_line_index) == split:
                            dummy_arr.append(pyglet.text.Label(full_text[start_line_index:last_word_index],
                                                               font_name=FONT_FAMILY,
                                                               font_size=DEFAULT_TEXT_SIZE,
                                                               x=curr_box[0] + DEFAULT_TEXT_SIZE,
                                                               y=curr_box[1] + curr_box[3] - (DEFAULT_TEXT_SIZE * 1.8) - curr_y_displacement,
                                                               bold=curr_box[5],
                                                               color=curr_box[6] + (255,),
                                                               batch=t_batch))
                            start_line_index = last_word_index + 1
                            curr_y_displacement += DEFAULT_TEXT_SIZE * 1.3
                        elif curr_text_index + 1 == len(full_text):
                            dummy_arr.append(pyglet.text.Label(full_text[start_line_index:],
                                                               font_name=FONT_FAMILY,
                                                               font_size=DEFAULT_TEXT_SIZE,
                                                               x=curr_box[0] + DEFAULT_TEXT_SIZE,
                                                               y=curr_box[1] + curr_box[3] - (
                                                                           DEFAULT_TEXT_SIZE * 2) - curr_y_displacement,
                                                               bold=curr_box[5],
                                                               color=curr_box[6] + (255,),
                                                               batch=t_batch))
                else:
                    dummy_arr.append(pyglet.text.Label(curr_box[4],
                                                       font_name=FONT_FAMILY,
                                                       font_size=DEFAULT_TEXT_SIZE,
                                                       x=curr_box[0] + ((curr_box[2] - word_size) / 2),
                                                       y=curr_box[1] + curr_box[3] / 2,
                                                       bold=curr_box[5],
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
            pyglet.graphics.vertex_list(3, ('v2f', arrow[5])).draw(GL_TRIANGLES)

        f_batch.draw()
        t_batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if NEXT_BUTTON_X <= x <= NEXT_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.next_frame()
        elif PREVIOUS_BUTTON_X <= x <= PREVIOUS_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.previous_frame()
        elif NEXT_F_BUTTON_X <= x <= NEXT_F_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.next_round()
        elif PREVIOUS_F_BUTTON_X <= x <= PREVIOUS_F_BUTTON_X+BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.previous_round()
        elif PLAY_BUTTON_X <= x <= PLAY_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.start_stop_frames()
        elif SLOW_BUTTON_X <= x <= SLOW_BUTTON_X + SMALL_BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.decrease_speed()
        elif FAST_BUTTON_X <= x <= FAST_BUTTON_X + SMALL_BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.increase_speed()
        elif RESTART_BUTTON_X <= x <= RESTART_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.restart()
        else:
            for curr_lb in self.frames[self.frame_num]['link_dict']:
                lb_tuple = self.frames[self.frame_num]['link_dict'][curr_lb]
                if lb_tuple[0] <= x <= lb_tuple[2] and lb_tuple[1] <= y <= lb_tuple[3]:
                    self.load_new_window(lb_tuple[4], lb_tuple[5])
