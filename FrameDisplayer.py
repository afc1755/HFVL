from pyglet import shapes
from pyglet import clock
from pyglet.gl import *
from hashConstants import *
import time


class FrameDisplayer(pyglet.window.Window):
    def __init__(self, frames, total_frames):
        super(FrameDisplayer, self).__init__(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.frames = frames
        self.frame_num = 0
        self.total_frames = total_frames
        self.curr_speed = 5
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
            clock.schedule_interval(self.call_draw, (1.5 / SPEED_ARR[self.curr_speed]))
            self.is_playing = True
            print('playing frames at ' + str(SPEED_ARR[self.curr_speed]) + 'x speed')

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
        play_pause_button = shapes.Rectangle(PLAY_BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=b_batch)
        faster_up_button = shapes.Rectangle(FAST_BUTTON_X, BUTTON_Y, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
                                       batch=b_batch)
        slower_button = shapes.Rectangle(SLOW_BUTTON_X, BUTTON_Y, SMALL_BUTTON_WIDTH, BUTTON_HEIGHT, color=WHITE,
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
            play_button_text = pyglet.text.Label('Stop',
                                                 font_size=DEFAULT_TEXT_SIZE,
                                                 x=PLAY_BUTTON_X + DEFAULT_TEXT_SIZE * .25,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .5),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        else:
            play_button_text = pyglet.text.Label('Play',
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
        slow_button_text = pyglet.text.Label('<<',
                                                 font_size=DEFAULT_TEXT_SIZE * 1.3,
                                                 x=SLOW_BUTTON_X + DEFAULT_TEXT_SIZE * 1.5,
                                                 y=BUTTON_Y + (BUTTON_HEIGHT * .5 - DEFAULT_TEXT_SIZE * .65),
                                                 color=BLACK_ALPHA,
                                                 batch=t_batch)
        fast_button_text = pyglet.text.Label('>>',
                                             font_size=DEFAULT_TEXT_SIZE * 1.3,
                                             x=FAST_BUTTON_X + DEFAULT_TEXT_SIZE * 1.5,
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
        speed_text = pyglet.text.Label('Speed: ' + str(TEXT_SPEED_ARR[self.curr_speed]),
                                       font_name='Courier',
                                       font_size=DEFAULT_TEXT_SIZE,
                                       x=DEFAULT_TEXT_SIZE / 4,
                                       y=WINDOW_HEIGHT - DEFAULT_TEXT_SIZE * 2.5,
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
            pyglet.graphics.vertex_list(3, ('v2f', arrow[5])).draw(GL_TRIANGLES)

        f_batch.draw()
        t_batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if NEXT_BUTTON_X <= x <= NEXT_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.next_frame()
        elif PREVIOUS_BUTTON_X <= x <= PREVIOUS_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.previous_frame()
        elif PLAY_BUTTON_X <= x <= PLAY_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.start_stop_frames()
        elif SLOW_BUTTON_X <= x <= SLOW_BUTTON_X + SMALL_BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.decrease_speed()
        elif FAST_BUTTON_X <= x <= FAST_BUTTON_X + SMALL_BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.increase_speed()
        elif RESTART_BUTTON_X <= x <= RESTART_BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
            self.restart()
