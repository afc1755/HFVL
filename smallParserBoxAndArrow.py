import time

import pyglet
from pyglet.gl import *
import FrameDisplayer
import copy
import numpy as np
from hashConstants import *
from collections import deque
from Node import Node


def run_frames(file_to_read, window_args):
    frames = read_file(file_to_read)
    if frames:
        fd = FrameDisplayer.FrameDisplayer(frames, len(frames))
        pyglet.app.run()


def read_file(file_to_read):
    frames = []
    lang_file = open(file_to_read)
    if not lang_file:
        return []
    box_dict = {}
    arrow_dict = {}
    global_dict = {'title': ['', BLACK], 'frame_count_visible': True}
    link_dict = {}

    reading_frame_num = 0

    for line in lang_file:
        line = line.strip()
        if len(line) == 0:
            continue
        elif line.strip().split(' ')[0].lower() != 'frame':
            if line[0] == '$':
                function_line = line.rsplit(')', 1)[0].replace('\n', '').split('(', 1)
                if function_line[0] == '$drawBox' or function_line[0] == '$db':
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
                            elif attribute_args[0].strip().lower() == 'bold':
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
                            elif attribute_args[0].strip().lower() == 'link':
                                link_file = open(attribute_args[1].strip('\'').lower())
                                if not link_file:
                                    print('invalid link file found for box:' + box_id)
                                else:
                                    link_dict[box_id] = [x, y,
                                                         x + width, y + height,
                                                         attribute_args[1].strip('\'').lower()]
                            elif attribute_args[0].strip().lower() == 'input':
                                if box_id in link_dict:
                                    input_arr = []
                                    for input_arg in attribute_args[1].strip().lower().split(';'):
                                        input_arr.append(input_arg.strip())
                                    link_dict[box_id].append(input_arr)
                            else:
                                print('invalid attribute found when creating box ' + box_id + ': ' +
                                      attribute_args[0].strip())
                    box_dict[box_id] = [x, y, width, height, box_text, box_bold, user_box_color, {}]
                elif function_line[0] == '$drawArrow' or function_line[0] == '$da':
                    arrow_args = function_line[1].split(',')
                    start_box_id = arrow_args[0].strip().replace('\'', '')
                    end_box_id = arrow_args[1].strip().replace('\'', '')
                    arr_bold = False
                    arrowhead_thickness = ARROW_NORMAL_SIZE
                    user_arr_color = BLACK

                    if len(arrow_args) > 2:
                        for i in range(2, len(arrow_args)):
                            attribute_args = arrow_args[i].split('=')
                            if attribute_args[0].strip().lower() == 'bold':
                                if attribute_args[1].strip('\'').lower() == 'true':
                                    arr_bold = True
                                    arrowhead_thickness = ARROW_BOLD_SIZE
                                else:
                                    arr_bold = False
                                    arrowhead_thickness = ARROW_NORMAL_SIZE
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
                    start_end_arrow = get_start_end_arrow(box_dict, start_box_id, end_box_id)
                    if len(start_end_arrow) > 0:
                        arrow_coords = pathfind_arrow(*start_end_arrow, start_box_id, end_box_id, box_dict, arrow_dict)
                        curr_time = time.time()
                        if len(arrow_coords) > 0:
                            curr_arrowhead = create_arrowhead(arrow_coords, arrowhead_thickness)
                            arrow_dict[start_box_id + end_box_id] = [arrow_coords, arr_bold, user_arr_color,
                                                                     start_box_id, end_box_id, curr_arrowhead]
                        print('arrowhead time = ' + str(time.time() - curr_time))
                elif function_line[0] == '$modifyBox' or function_line[0] == '$mb':
                    box_args = function_line[1].split(',')
                    box_id = box_args[0].replace('\'', '').strip()
                    if box_id not in box_dict:
                        print('error: no such box as ' + box_id)
                    for i in range(1, len(box_args)):
                        attribute_args = box_args[i].split('=')
                        if attribute_args[0].strip().lower() == 'text':
                            box_dict[box_id][4] = attribute_args[1].replace('\'', '')
                        elif attribute_args[0].strip().lower() == 'bold':
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
                        elif attribute_args[0].strip().lower() == 'link':
                            link_file = open(attribute_args[1].strip('\'').lower())
                            if not link_file:
                                print('invalid link file found for box:' + box_id)
                            else:
                                link_box = box_dict[box_dict]
                                link_dict[box_id] = (link_box[0], link_box[1],
                                                     link_box[0] + link_box[2], link_box[1] + link_box[3],
                                                     attribute_args[1].strip('\'').lower())
                        elif attribute_args[0].strip().lower() == 'input':
                            if box_id in link_dict:
                                input_arr = []
                                for input_arg in attribute_args[1].strip().lower().split(','):
                                    input_arr.append(input_arg.strip())
                                link_dict[box_id].append(input_arr)
                        else:
                            print('invalid attribute found when modifying box ' + box_id + ': ' +
                                  attribute_args[0].strip())
                elif function_line[0] == '$modifyArrow' or function_line[0] == '$ma':
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
                                    arrow_dict[start_box_id + end_box_id][5] = \
                                        create_arrowhead(arrow_dict[start_box_id + end_box_id][0], ARROW_BOLD_SIZE)
                                else:
                                    arrow_dict[start_box_id + end_box_id][1] = False
                                    arrow_dict[start_box_id + end_box_id][5] = \
                                        create_arrowhead(arrow_dict[start_box_id + end_box_id][0], ARROW_NORMAL_SIZE)
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
                elif function_line[0] == '$modifyTitle' or function_line[0] == '$mt':
                    title_args = function_line[1].split(',')
                    if len(title_args) > 0:
                        for i in range(0, len(title_args)):
                            attribute_args = title_args[i].split('=')
                            if attribute_args[0].strip().lower() == 'text':
                                global_dict['title'][0] = attribute_args[1].replace('\'', '')
                            elif attribute_args[0].strip().lower() == 'color':
                                if attribute_args[1].strip('\'').lower() == 'blue':
                                    global_dict['title'][1] = BLUE
                                elif attribute_args[1].strip('\'').lower() == 'green':
                                    global_dict['title'][1] = GREEN
                                elif attribute_args[1].strip('\'').lower() == 'red':
                                    global_dict['title'][1] = RED
                                elif attribute_args[1].strip('\'').lower() == 'black':
                                    global_dict['title'][1] = BLACK
                                else:
                                    print(
                                        "invalid color used, defaulting to black\ncolor options are: blue, green, red")
                elif function_line[0] == '$createTextBox' or function_line[0] == '$ctb':
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
                            elif attribute_args[0].strip().lower() == 'bold':
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
                            elif attribute_args[0].strip().lower() == 'link':
                                link_file = open(attribute_args[1].strip('\'').lower())
                                if not link_file:
                                    print('invalid link file found for box:' + box_id)
                                else:
                                    link_dict[box_id] = (x, y,
                                                         x + width, y + height,
                                                         attribute_args[1].strip('\'').lower())
                            else:
                                print('invalid attribute found when creating box ' + box_id + ': ' +
                                      attribute_args[0].strip())
                    box_dict[box_id] = [x, y, width, height, box_text, box_bold, user_box_color, {}]

                    print('text box drawing')
                elif function_line[0] == '$hideFrameCount' or function_line[0] == '$hfc':
                    global_dict['frame_count_visible'] = False
                elif function_line[0] == '$showFrameCount' or function_line[0] == '$sfc':
                    global_dict['frame_count_visible'] = True
                else:
                    print('error while parsing\ninvalid function at line: \n\t' + line)
            else:
                continue
        elif line.strip().split(' ')[0].lower() == 'frame' and line.strip().split(' ')[1].lower() == 'end':
            frames.append({'box_dict': box_dict, 'arrow_dict': arrow_dict,
                           'global_dict': global_dict, 'link_dict': link_dict})
        else:
            old_box_dict = box_dict
            old_arrow_dict = arrow_dict
            box_dict = copy.deepcopy(old_box_dict)
            arrow_dict = copy.deepcopy(old_arrow_dict)
            reading_frame_num += 1
    return frames


def get_start_end_arrow(box_dict, start_box_id, end_box_id):
    box_id_arr = [start_box_id, end_box_id]
    arrow_info = []
    for box_id in box_id_arr:
        box = box_dict[box_id]
        blocked_dict = find_blocking_boxes(box_id, box_dict)
        x_diff, y_diff = get_x_y_diff(box_dict[start_box_id], box_dict[end_box_id])
        if box_id != start_box_id:
            x_diff = -x_diff
            y_diff = -y_diff
        if abs(x_diff) > abs(y_diff):
            if x_diff < 0 and not blocked_dict['left']:
                curr_x, curr_y, curr_loc = get_placements(box, 'left')
            elif x_diff >= 0 and not blocked_dict['right']:
                curr_x, curr_y, curr_loc = get_placements(box, 'right')
            elif y_diff >= 0 and not blocked_dict['top']:
                curr_x, curr_y, curr_loc = get_placements(box, 'top')
            elif y_diff < 0 and not blocked_dict['bottom']:
                curr_x, curr_y, curr_loc = get_placements(box, 'bottom')
            elif y_diff >= 0 and not blocked_dict['bottom']:
                curr_x, curr_y, curr_loc = get_placements(box, 'bottom')
            elif y_diff < 0 and not blocked_dict['top']:
                curr_x, curr_y, curr_loc = get_placements(box, 'top')
            elif x_diff < 0 and not blocked_dict['right']:
                curr_x, curr_y, curr_loc = get_placements(box, 'right')
            elif x_diff >= 0 and not blocked_dict['left']:
                curr_x, curr_y, curr_loc = get_placements(box, 'left')
            else:
                print('can\'t find a good point for this arrow!')
                return []
        else:
            if y_diff > 0 and not blocked_dict['top']:
                curr_x, curr_y, curr_loc = get_placements(box, 'top')
            elif y_diff <= 0 and not blocked_dict['bottom']:
                curr_x, curr_y, curr_loc = get_placements(box, 'bottom')
            elif x_diff < 0 and not blocked_dict['left']:
                curr_x, curr_y, curr_loc = get_placements(box, 'left')
            elif x_diff >= 0 and not blocked_dict['right']:
                curr_x, curr_y, curr_loc = get_placements(box, 'right')
            elif x_diff < 0 and not blocked_dict['right']:
                curr_x, curr_y, curr_loc = get_placements(box, 'right')
            elif x_diff >= 0 and not blocked_dict['left']:
                curr_x, curr_y, curr_loc = get_placements(box, 'left')
            elif y_diff >= 0 and not blocked_dict['bottom']:
                curr_x, curr_y, curr_loc = get_placements(box, 'bottom')
            elif y_diff < 0 and not blocked_dict['top']:
                curr_x, curr_y, curr_loc = get_placements(box, 'top')
            else:
                print('can\'t find a good point for this arrow!')
                return []
        arrow_info.append([curr_x, curr_y, curr_loc])
    return int(arrow_info[0][0]), int(arrow_info[0][1]), arrow_info[0][2], int(arrow_info[1][0]), int(arrow_info[1][1]), arrow_info[1][2]


def find_blocking_boxes(box_id, box_dict):
    # below finds other boxes close on every side of the start and end boxes
    # this tells the arrow not to start on any of those close sides
    blocked = dict.fromkeys(['left', 'right', 'top', 'bottom'], False)
    curr_box = box_dict[box_id]

    for box in box_dict:
        box_left = box_dict[box][0]
        box_right = box_dict[box][0] + box_dict[box][2]
        box_top = box_dict[box][1] + box_dict[box][3]
        box_bottom = box_dict[box][1]
        if box != box_id:
            if abs(box_left - (curr_box[0] + curr_box[2])) < 10 and (
                    box_bottom <= curr_box[1] + 2 * curr_box[3] / 3 <= box_top):
                blocked['right'] = True
            if abs(curr_box[0] - box_right) <= 10 and (box_bottom <= curr_box[1] + 2 * curr_box[3] / 3 <= box_top):
                blocked['left'] = True
            if abs(box_bottom - (curr_box[1] + curr_box[3])) <= 10 and (
                    box_left <= curr_box[0] + 2 * curr_box[2] / 3 <= box_right):
                blocked['top'] = True
            if abs(curr_box[1] - box_top) <= 10 and (box_left <= curr_box[0] + 2 * curr_box[2] / 3 <= box_right):
                blocked['bottom'] = True
    return blocked


def get_placements(curr_box, curr_dir):
    # this code helps to determine what the displacement of an arrow start and end point should be
    # it finds out how many arrows are already starting or finishing from that arrow
    if curr_dir in curr_box[7]:
        multi_arrow_displacement_start = calculate_displacement(curr_box[7][curr_dir])
        curr_box[7][curr_dir] += 1
    else:
        multi_arrow_displacement_start = 0
        curr_box[7][curr_dir] = 1
    if curr_dir == 'left':
        curr_x = curr_box[0]
        curr_y = curr_box[1] + curr_box[3] / 2 + multi_arrow_displacement_start
        curr_loc = 'left'
    elif curr_dir == 'right':
        curr_x = curr_box[0] + curr_box[2]
        curr_y = curr_box[1] + curr_box[3] / 2 + multi_arrow_displacement_start
        curr_loc = 'right'
    elif curr_dir == 'top':
        curr_x = curr_box[0] + curr_box[2] / 2 + multi_arrow_displacement_start
        curr_y = curr_box[1] + curr_box[3]
        curr_loc = 'top'
    else:
        curr_x = curr_box[0] + curr_box[2] / 2 + multi_arrow_displacement_start
        curr_y = curr_box[1]
        curr_loc = 'bottom'
    return curr_x, curr_y, curr_loc


def calculate_displacement(arrow_num):
    if arrow_num == 0:
        return 0
    elif arrow_num % 2 == 0:
        return -ARROW_BOLD_SIZE * 1.8 * (arrow_num - 1)
    else:
        return ARROW_BOLD_SIZE * 1.8 * arrow_num


def get_x_y_diff(start_box, end_box):
    if start_box[0] < end_box[0]:
        x_diff = min((end_box[0] + end_box[2]) - start_box[0], abs(end_box[0] - start_box[0]))
    elif start_box[0] > end_box[0]:
        x_diff = -min(abs(end_box[0] - (start_box[0] + start_box[2])), abs(end_box[0] - start_box[0]))
    else:
        x_diff = 0
    if start_box[1] < end_box[1]:
        y_diff = min((end_box[1] - (start_box[1] + start_box[3])), end_box[1] - start_box[1])
    elif start_box[1] > end_box[1]:
        y_diff = -min(abs((end_box[1] + end_box[3]) - start_box[1]), abs(end_box[1] - start_box[1]))
    else:
        y_diff = 0
    return x_diff, y_diff


def point_in_box(p_x, p_y, box):
    if box[0] <= p_x <= box[0] + box[2] and box[1] <= p_y <= box[1] + box[3]:
        return True
    else:
        return False


def point_near_box(p_x, p_y, box):
    if box[0] - BOX_NEARNESS <= p_x <= box[0] + box[2] + BOX_NEARNESS and box[1] - BOX_NEARNESS <= p_y <= box[1] + box[3] + BOX_NEARNESS:
        return True
    else:
        return False


def create_matrix(special_box_coords, special_box_loc, boxes_to_ignore, box_dict, arrow_dict):
    out_mat = np.zeros((WINDOW_WIDTH//MATRIX_RESOLUTION, WINDOW_HEIGHT//MATRIX_RESOLUTION))
    for x in range(0, WINDOW_WIDTH//MATRIX_RESOLUTION):
        for y in range(0, WINDOW_HEIGHT//MATRIX_RESOLUTION):
            if check_colliding(x * MATRIX_RESOLUTION, y * MATRIX_RESOLUTION, box_dict, boxes_to_ignore):
                out_mat[x][y] = -1
            elif check_colliding_arrow(x * MATRIX_RESOLUTION, y * MATRIX_RESOLUTION, arrow_dict):
                out_mat[x][y] = 500
            else:
                out_mat[x][y] = 1
    for i in range(0, 2):
        if special_box_loc[i] == 'top':
            extra_x = int(special_box_coords[i][0] // MATRIX_RESOLUTION)
            extra_y = int((special_box_coords[i][1] // MATRIX_RESOLUTION))
            for extra_space in range(1, int(ARROW_END_GAP// MATRIX_RESOLUTION)):
                out_mat[extra_x - 1][extra_y + extra_space] = -1
                out_mat[extra_x + 1][extra_y + extra_space] = -1
        elif special_box_loc[i] == 'bottom':
            extra_x = int(special_box_coords[i][0] // MATRIX_RESOLUTION)
            extra_y = int((special_box_coords[i][1] // MATRIX_RESOLUTION))
            for extra_space in range(1, int(ARROW_END_GAP//MATRIX_RESOLUTION)):
                out_mat[extra_x - 1][extra_y - extra_space] = -1
                out_mat[extra_x + 1][extra_y - extra_space] = -1
        elif special_box_loc[i] == 'left':
            extra_x = int((special_box_coords[i][0] // MATRIX_RESOLUTION))
            extra_y = int(special_box_coords[i][1] // MATRIX_RESOLUTION)
            for extra_space in range(1, int(ARROW_END_GAP//MATRIX_RESOLUTION)):
                out_mat[extra_x - extra_space][extra_y - 1] = -1
                out_mat[extra_x - extra_space][extra_y + 1] = -1
        elif special_box_loc[i] == 'right':
            extra_x = int((special_box_coords[i][0] // MATRIX_RESOLUTION))
            extra_y = int(special_box_coords[i][1] // MATRIX_RESOLUTION)
            for extra_space in range(1, int(ARROW_END_GAP// MATRIX_RESOLUTION)):
                out_mat[extra_x + extra_space][extra_y - 1] = -1
                out_mat[extra_x + extra_space][extra_y + 1] = -1
    return out_mat


def is_inside_matrix(x, y):
    if 0 <= x < int(WINDOW_WIDTH//MATRIX_RESOLUTION) and 0 <= y < int(WINDOW_HEIGHT//MATRIX_RESOLUTION):
        return True
    return False


def pathfind_arrow(start_x, start_y, s_loc, end_x, end_y, e_loc, s_box_id, e_box_id, box_dict, arrow_dict):
    curr_time = time.time()
    matrix = create_matrix([[start_x, start_y], [end_x, end_y]], [s_loc, e_loc], [s_box_id, e_box_id], box_dict, arrow_dict)
    print('matrix creation:' + str(time.time() - curr_time))
    curr_time = time.time()
    old_node = pathfind_arrow_dijkstras(matrix, int(start_x//MATRIX_RESOLUTION), int(start_y//MATRIX_RESOLUTION),
                                        int(end_x//MATRIX_RESOLUTION), int(end_y//MATRIX_RESOLUTION))

    if not old_node:
        return []

    point_list = []
    moving_y = False
    first_run = True
    last_node = old_node
    curr_node = last_node.parent
    while curr_node.parent:
        if last_node.x == curr_node.x:
            if moving_y or first_run:
                last_node = curr_node
                curr_node = curr_node.parent
                first_run = False
            else:
                point_list.append([last_node.x * MATRIX_RESOLUTION, last_node.y * MATRIX_RESOLUTION, old_node.x * MATRIX_RESOLUTION, old_node.y * MATRIX_RESOLUTION])
                old_node = last_node
            moving_y = True
        else:
            if not moving_y or first_run:
                last_node = curr_node
                curr_node = curr_node.parent
                first_run = False
            else:
                point_list.append([last_node.x * MATRIX_RESOLUTION, last_node.y * MATRIX_RESOLUTION, old_node.x * MATRIX_RESOLUTION, old_node.y * MATRIX_RESOLUTION])
                old_node = last_node
            moving_y = False
    point_list.append([curr_node.x * MATRIX_RESOLUTION, curr_node.y * MATRIX_RESOLUTION, old_node.x * MATRIX_RESOLUTION, old_node.y * MATRIX_RESOLUTION])
    point_list.reverse()
    print('rest of arrow finding:' + str(time.time() - curr_time))
    return point_list


def pathfind_arrow_dijkstras(matrix, start_x, start_y, end_x, end_y):
    # create a queue and enqueue the first node
    q = deque()
    src = Node(start_x, start_y, None)
    q.append(src)
    score_dict = {(src.x, src.y): 0}

    row = [-1, 0, 0, 1]
    col = [0, -1, 1, 0]
    candidates = []

    # loop till queue is empty
    while q:
        # dequeue front node and process it
        curr = q.popleft()
        i = curr.x
        j = curr.y

        # return if the destination is found
        if i == end_x and j == end_y:
            if score_dict[(i, j)] < 3:
                return curr
            else:
                candidates.append(curr)

        curr_score = score_dict[(curr.x, curr.y)]
        # check all four possible movements from the current cell
        # and recur for each valid movement
        for k in range(4):
            # get next position coordinates using the value of the current cell
            x = i + row[k]
            y = j + col[k]

            # check if it is possible to go to the next position
            # from the current position
            if is_inside_matrix(x, y) and (int(matrix[x][y]) != -1 or (x == end_x and y == end_y)):
                # construct the next cell node
                next = Node(x, y, curr)
                key = (next.x, next.y)
                next_score = curr_score + matrix[x][y]

                # if it is not visited yet
                if key not in score_dict:
                    # enqueue it and mark it as visited
                    q.append(next)
                    score_dict[key] = next_score
                elif score_dict[key] > next_score:
                    if next in q:
                        q.remove(next)
                    score_dict[key] = next_score
                    q.append(next)

    if len(candidates) == 0:
        # return None if the path is not possible
        return None
    else:
        curr_min = np.inf
        curr_can = None
        for candidate in candidates:
            if score_dict[(candidate.x, candidate.y)] < curr_min:
                curr_min = score_dict[(candidate.x, candidate.y)]
                curr_can = candidate
        return curr_can


def check_colliding(loc_x, loc_y, box_dict, boxes_to_ignore):
    for box_id in box_dict:
        if box_id in boxes_to_ignore:
            if point_in_box(loc_x, loc_y, box_dict[box_id]):
                return True
        else:
            if point_near_box(loc_x, loc_y, box_dict[box_id]):
                return True

    return False


def check_colliding_arrow(loc_x, loc_y, arrow_dict):
    for arrow_id in arrow_dict:
        for coord in arrow_dict[arrow_id][0]:
            if point_near_arrow(loc_x, loc_y, coord):
                return True
    return False


def point_near_arrow(loc_x, loc_y, coord):
    if (coord[0] - (MATRIX_RESOLUTION * ARROW_NEARNESS)) <= loc_x <= (coord[2] + (MATRIX_RESOLUTION * ARROW_NEARNESS)) and \
            (coord[1] - (MATRIX_RESOLUTION * ARROW_NEARNESS)) <= loc_y <= (coord[3] + (MATRIX_RESOLUTION * ARROW_NEARNESS)):
        return True
    return False


def create_arrowhead(arrow_lines, arrowhead_thickness):
    start_x = arrow_lines[-1][0]
    start_y = arrow_lines[-1][1]
    end_x = arrow_lines[-1][2]
    end_y = arrow_lines[-1][3]

    points = [end_x, end_y]
    diff_x = end_x - start_x
    diff_y = end_y - start_y

    if diff_x < 0 and diff_y == 0:
        points.extend([end_x + arrowhead_thickness,
                       end_y - arrowhead_thickness,
                       end_x + arrowhead_thickness,
                       end_y + arrowhead_thickness])
    elif diff_x > 0 and diff_y == 0:
        points.extend([end_x - arrowhead_thickness,
                       end_y + arrowhead_thickness,
                       end_x - arrowhead_thickness,
                       end_y - arrowhead_thickness])
    elif diff_x == 0 and diff_y < 0:
        points.extend([end_x - arrowhead_thickness,
                       end_y + arrowhead_thickness,
                       end_x + arrowhead_thickness,
                       end_y + arrowhead_thickness])
    elif diff_x == 0 and diff_y > 0:
        points.extend([end_x + arrowhead_thickness,
                       end_y - arrowhead_thickness,
                       end_x - arrowhead_thickness,
                       end_y - arrowhead_thickness])
    else:
        print('Bad Last Arrow: Code Error!' + str(arrow_lines))
        points.extend([end_x + arrowhead_thickness,
                       end_y - arrowhead_thickness,
                       end_x + arrowhead_thickness,
                       end_y + arrowhead_thickness])
    return points


if __name__ == "__main__":
    run_frames('fullShaStartFrame', [])
