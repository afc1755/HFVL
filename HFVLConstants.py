# constants file for Hash Function Visualization Language
# created by Andrew Chabot
# RIT Master's Project 2021

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 850

MATRIX_RESOLUTION = 5
BOX_NEARNESS = 12
ARROW_NEARNESS = 8
ARROW_END_GAP = 20

NAV_BOX_WIDTH = WINDOW_WIDTH
NAV_BOX_HEIGHT = 40
BUTTON_HEIGHT = 30
BUTTON_WIDTH = 100
SMALL_BUTTON_WIDTH = 50

SMALL_BOX_WIDTH = 120
SMALL_BOX_HEIGHT = 100
SMALL_BOX_BORDER_NORMAL = 2
SMALL_BOX_BORDER_BOLD = 4
START_BOX_POS = [10, 10]

WHITE = (255, 255, 255)
WHITE_ALPHA = (255, 255, 255, 255)
BLACK = (0, 0, 0)
BLACK_ALPHA = (0, 0, 0, 255)
GRAY = (80, 80, 80)
RED = (180, 0, 0)
GREEN = (0, 150, 0)
BLUE = (20, 20, 180)

DEFAULT_TEXT_SIZE = 10
BUTTON_TEXT_SIZE = DEFAULT_TEXT_SIZE * 1.3
TITLE_TEXT_SIZE = DEFAULT_TEXT_SIZE * 2

ARROW_NORMAL_SIZE = 7
ARROW_BOLD_SIZE = 9
LINE_NORMAL_SIZE = 2
LINE_BOLD_SIZE = 4
SPEED_ARR = (0.1, 0.15, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 5, 10)
TEXT_SPEED_ARR = ('0.1x', '0.15x', '1/4x', '1/2x', '3/4x', '1x', '1.5x', '2x', '3x', '5x', '10x')
FONT_FAMILY = ('Lucida Sans Typewriter', 'Courier', 'Courier New', 'Arial')

TITLE_Y = WINDOW_HEIGHT - (DEFAULT_TEXT_SIZE * 2.75)

PLAY_BUTTON_X = .8 * BUTTON_WIDTH
SLOW_BUTTON_X = .2 * BUTTON_WIDTH
FAST_BUTTON_X = 1.9 * BUTTON_WIDTH

FRAME_INFO_X = (WINDOW_WIDTH / 2) - (3.1 * BUTTON_WIDTH)
SPEED_INFO_X = (WINDOW_WIDTH / 2) - (1.7 * BUTTON_WIDTH)

PREVIOUS_BUTTON_X = WINDOW_WIDTH - (6.2 * BUTTON_WIDTH)
NEXT_BUTTON_X = WINDOW_WIDTH - (5.1 * BUTTON_WIDTH)
NEXT_F_BUTTON_X = WINDOW_WIDTH - (2.6 * BUTTON_WIDTH)
PREVIOUS_F_BUTTON_X = WINDOW_WIDTH - (3.7 * BUTTON_WIDTH)
RESTART_BUTTON_X = WINDOW_WIDTH - (1.2 * BUTTON_WIDTH)
BUTTON_Y = (NAV_BOX_HEIGHT - BUTTON_HEIGHT) / 2
