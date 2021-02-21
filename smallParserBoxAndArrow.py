import pyglet
from pyglet.gl import *
from FrameDisplayer import FrameDisplayer
import copy
from hashConstants import *


def run_frames(file_to_read):
    frames = read_file(file_to_read)
    fd = FrameDisplayer(frames, len(frames) - 1)
    pyglet.app.run()


def read_file(file_to_read):
    frames = []
    lang_file = open(file_to_read)
    box_dict = {}
    arrow_dict = {}
    global_dict = {'title': ['', BLACK], 'frame_count_visible': True}

    reading_frame_num = 0

    for line in lang_file:
        line = line.strip()
        if len(line) == 0:
            continue
        elif line.strip().split(' ')[0].lower() != 'frame':
            if line[0] == '$':
                function_line = line.replace(')', '').replace('\n', '').split('(')
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
                    arrow_s_x, arrow_e_x, arrow_s_y, arrow_e_y, s_loc, e_loc = get_start_end_arrow(box_dict, start_box_id, end_box_id)
                    arrow_coords = pathfind_arrow(arrow_s_x, arrow_e_x, arrow_s_y, arrow_e_y, start_box_id, end_box_id, s_loc, e_loc, box_dict)
                    if len(arrow_coords) > 0:
                        curr_arrowhead = create_arrowhead(arrow_coords, arrowhead_thickness)
                        arrow_dict[start_box_id + end_box_id] = [arrow_coords, arr_bold, user_arr_color,
                                                                 start_box_id, end_box_id, curr_arrowhead]

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
                elif function_line[0] == '$hideFrameCount' or function_line[0] == '$hfc':
                    global_dict['frame_count_visible'] = False
                elif function_line[0] == '$showFrameCount' or function_line[0] == '$sfc':
                    global_dict['frame_count_visible'] = True
                else:
                    print('unknown function: ' + function_line[0])
            else:
                print('error while parsing\ninvalid function at line: \n\t' + line)
        elif line.strip().split(' ')[0].lower() == 'frame' and line.strip().split(' ')[1].lower() == 'end':
            frames.append({'box_dict': box_dict, 'arrow_dict': arrow_dict, 'global_dict': global_dict})
        else:
            old_box_dict = box_dict
            old_arrow_dict = arrow_dict
            box_dict = copy.deepcopy(old_box_dict)
            arrow_dict = copy.deepcopy(old_arrow_dict)
            reading_frame_num += 1
    return frames


def calculate_displacement(arrow_num):
    if arrow_num == 0:
        return 0
    elif arrow_num % 2 == 0:
        return -ARROW_BOLD_SIZE * 2 * (arrow_num - 1)
    else:
        return ARROW_BOLD_SIZE * 2 * arrow_num


def get_start_end_arrow(box_dict, start_box_id, end_box_id):
    start_box = box_dict[start_box_id]
    end_box = box_dict[end_box_id]

    blocked_dict = find_blocking_boxes(start_box_id, end_box_id, box_dict)
    x_diff, y_diff = get_x_y_diff(start_box, end_box)

    x1 = -1
    y1 = -1
    desired_x = -1
    desired_y = -1
    start_loc = ''
    end_loc = ''

    # this code determines what the displacement of an arrow start and end point should be
    # it finds out how many arrows are already starting or finishing from that arrow
    if abs(x_diff) > abs(y_diff):
        if x_diff > 0 and not blocked_dict['s_left'] and not blocked_dict['e_right']:
            if 'left' in start_box[7]:
                multi_arrow_displacement_start = calculate_displacement(start_box[7]['left'])
                start_box[7]['left'] += 1
            else:
                multi_arrow_displacement_start = 0
                start_box[7]['left'] = 1
            if 'right' in end_box[7]:
                multi_arrow_displacement_end = calculate_displacement(end_box[7]['right'])
                end_box[7]['right'] += 1
            else:
                multi_arrow_displacement_end = 0
                end_box[7]['right'] = 1
            x1 = start_box[0]
            desired_x = end_box[0] + end_box[2]
            y1 = start_box[1] + start_box[3] / 2 + multi_arrow_displacement_start
            desired_y = end_box[1] + (end_box[3] / 2) + multi_arrow_displacement_end
            start_loc = 'left'
            end_loc = 'right'
        elif x_diff <= 0 and not blocked_dict['s_right'] and not blocked_dict['e_left']:
            if 'right' in start_box[7]:
                multi_arrow_displacement_start = calculate_displacement(start_box[7]['right'])
                start_box[7]['right'] += 1
            else:
                multi_arrow_displacement_start = 0
                start_box[7]['right'] = 1
            if 'left' in end_box[7]:
                multi_arrow_displacement_end = calculate_displacement(end_box[7]['left'])
                end_box[7]['left'] += 1
            else:
                multi_arrow_displacement_end = 0
                end_box[7]['left'] = 1
            x1 = start_box[0] + start_box[2]
            desired_x = end_box[0]
            y1 = start_box[1] + start_box[3] / 2 + multi_arrow_displacement_start
            desired_y = end_box[1] + (end_box[3] / 2) + multi_arrow_displacement_end
            start_loc = 'right'
            end_loc = 'left'
    elif x1 == -1:
        if y_diff > 0 and not blocked_dict['s_bottom'] and not blocked_dict['e_top']:
            if 'top' in start_box[7]:
                multi_arrow_displacement_start = calculate_displacement(start_box[7]['top'])
                start_box[7]['top'] += 1
            else:
                multi_arrow_displacement_start = 0
                start_box[7]['top'] = 1
            if 'bottom' in end_box[7]:
                multi_arrow_displacement_end = calculate_displacement(end_box[7]['bottom'])
                end_box[7]['bottom'] += 1
            else:
                multi_arrow_displacement_end = 0
                end_box[7]['bottom'] = 1
            y1 = start_box[1]
            x1 = start_box[0] + start_box[2] / 2 + multi_arrow_displacement_start
            desired_y = end_box[1] + end_box[3]
            desired_x = end_box[0] + end_box[2] / 2 + multi_arrow_displacement_end
            start_loc = 'bottom'
            end_loc = 'top'
        elif y_diff <= 0 and not blocked_dict['s_top'] and not blocked_dict['e_bottom']:
            if 'bottom' in start_box[7]:
                multi_arrow_displacement_start = calculate_displacement(start_box[7]['bottom'])
                start_box[7]['bottom'] += 1
            else:
                multi_arrow_displacement_start = 0
                start_box[7]['bottom'] = 1
            if 'top' in end_box[7]:
                multi_arrow_displacement_end = calculate_displacement(end_box[7]['top'])
                end_box[7]['top'] += 1
            else:
                multi_arrow_displacement_end = 0
                end_box[7]['top'] = 1

            x1 = start_box[0] + start_box[2] / 2 + multi_arrow_displacement_start
            y1 = start_box[1] + start_box[3]
            desired_x = end_box[0] + end_box[2] / 2 + multi_arrow_displacement_end
            desired_y = end_box[1]
            start_loc = 'top'
            end_loc = 'bottom'
        else:
            print('uh oh no path')
    else:
        print('no path able to be created between two boxes: ' + str(end_box_id) + ' and ' + str(start_box_id))
        return []
    return x1, y1, desired_x, desired_y, start_loc, end_loc


def find_blocking_boxes(start_box_id, end_box_id, box_dict):
    blocked = dict.fromkeys(["s_left", "s_right", "s_top", "s_bottom", "e_left", "e_right", "e_top", "e_bottom"], False)
    start_box = box_dict[start_box_id]
    end_box = box_dict[end_box_id]

    # below finds other boxes close on every side of the start and end boxes
    # this tells the arrow not to start on any of those close sides
    for box in box_dict:
        box_left = box_dict[box][0]
        box_right = box_dict[box][0] + box_dict[box][2]
        box_top = box_dict[box][1] + box_dict[box][3]
        box_bottom = box_dict[box][1]
        if box != start_box_id:
            if abs(box_left - (start_box[0] + start_box[2])) < 10 and (
                    box_bottom <= start_box[1] + 2 * start_box[3] / 3 <= box_top):
                blocked['s_right'] = True
            if abs(start_box[0] - box_right) <= 10 and (box_bottom <= start_box[1] + 2 * start_box[3] / 3 <= box_top):
                blocked['s_left'] = True
            if abs(box_bottom - (start_box[1] + start_box[3])) <= 10 and (
                    box_left <= start_box[0] + 2 * start_box[2] / 3 <= box_right):
                blocked['s_top'] = True
            if abs(start_box[1] - box_top) <= 10 and (box_left <= start_box[0] + 2 * start_box[2] / 3 <= box_right):
                blocked['s_bottom'] = True
        if box != end_box_id:
            if abs(box_left - (end_box[0] + end_box[2])) < 10 and (
                    box_bottom <= end_box[1] + 2 * end_box[3] / 3 <= box_top):
                blocked['e_right'] = True
            if abs(end_box[0] - box_right) <= 10 and (box_bottom <= end_box[1] + 2 * end_box[3] / 3 <= box_top):
                blocked['e_left'] = True
            if abs(box_bottom - (end_box[1] + end_box[3])) <= 10 and (
                    box_left <= end_box[0] + 2 * end_box[2] / 3 <= box_right):
                blocked['e_top'] = True
            if abs(end_box[1] - box_top) <= 10 and (box_left <= end_box[0] + 2 * end_box[2] / 3 <= box_right):
                blocked['e_bottom'] = True
    return blocked


def get_x_y_diff(start_box, end_box):
    if start_box[0] < end_box[0]:
        x_diff = start_box[0] + (start_box[2] - end_box[0])
    elif start_box[0] > end_box[0]:
        x_diff = start_box[0] - (end_box[0] + end_box[2])
    else:
        x_diff = 0
    if start_box[1] > end_box[1]:
        y_diff = start_box[1] - (end_box[1] + end_box[3])
    elif start_box[1] < end_box[1]:
        y_diff = start_box[1] + (start_box[3] - end_box[1])
    else:
        y_diff = 0
    return x_diff, y_diff


def point_in_box(p_x, p_y, box):
    if box[0] <= p_x <= box[0] + box[2] and box[1] <= p_y <= box[1] + box[3]:
        return True
    else:
        return False


def point_near_box(p_x, p_y, box):
    if box[0] - 10 <= p_x <= box[0] + box[2] + 10 and box[1] - 10 <= p_y <= box[1] + box[3] + 10:
        return True
    else:
        return False


def pathfind_arrow(start_x, start_y, end_x, end_y, s_box_id, e_box_id, s_loc, e_loc, box_dict):
    old_x = start_x
    old_y = start_y

    curr_x = start_x
    curr_y = start_y

    x_diff = end_x - start_x
    y_diff = end_y - start_y

    x_inc = 10
    y_inc = 10

    if x_diff != 0:
        x_inc = (x_diff/abs(x_diff)) * 10

    if y_diff != 0:
        y_inc = (y_diff/abs(y_diff)) * 10

    vert_list = []

    # priority 1: move in a direction different than last move, move away from boxes and towards destination box
    # if x is already right, try to move towards in y.
    # if we can't move towards in y, try to change x and see if we can move y now
    # if x is not right, try to move in an x direction
    # if we can't move in x direction, move in y direction either way
    #
    # priority 2: move towards the end box in either direction if not hitting other boxes
    # priority 3: move away from other boxes to get more space

    if s_loc == 'top' or s_loc == 'bottom':
        last_move_y = False
    else:
        last_move_y = True

    if e_loc == 'top' or e_loc == 'bottom':
        final_move_y = True
    else:
        final_move_y = False

    while curr_x != end_x or curr_y != end_y:
        colliding = False
        moving = False
        currently_moving_neg = False
        currently_moving_pos = False
        if last_move_y:
            while not colliding:
                if curr_x != end_x and end_x - 10 <= curr_x <= end_x + 10:
                    curr_x = end_x
                    break
                if not currently_moving_neg:
                    for box_id in box_dict:
                        if box_id != s_box_id and box_id != e_box_id:
                            if point_near_box(curr_x + x_inc, curr_x, box_dict[box_id]):
                                colliding = True
                                break
                    if not colliding:
                        currently_moving_pos = True
                        curr_x = curr_x + x_inc
                if not currently_moving_pos:
                    for box_id in box_dict:
                        if box_id != s_box_id and box_id != e_box_id:
                            if point_near_box(curr_x - x_inc, curr_x, box_dict[box_id]):
                                colliding = True
                                break
                    if not colliding:
                        currently_moving_neg = True
                        curr_x = curr_x - x_inc
                if room_to_go(curr_x, curr_y, False, x_diff, box_dict):
                    break
            last_move_y = False
        else:
            while not colliding:
                if curr_y != end_y and end_y - 10 <= curr_y <= end_y + 10:
                    curr_y = end_y
                    break
                if not currently_moving_neg:
                    for box_id in box_dict:
                        if box_id != s_box_id and box_id != e_box_id:
                            if point_near_box(curr_x, curr_y + y_inc, box_dict[box_id]):
                                colliding = True
                                break
                    if not colliding:
                        currently_moving_pos = True
                        curr_y = curr_y + y_inc
                if not currently_moving_pos:
                    for box_id in box_dict:
                        if box_id != s_box_id and box_id != e_box_id:
                            if point_near_box(curr_x, curr_y - y_inc, box_dict[box_id]):
                                colliding = True
                                break
                    if not colliding:
                        currently_moving_neg = True
                        curr_y = curr_y - y_inc
                if room_to_go(curr_x, curr_y, True, y_diff, box_dict):
                    break
            last_move_y = True
        vert_list.append([old_x, old_y, curr_x, curr_y])
        old_x = curr_x
        old_y = curr_y
    print('good arrow')
    return vert_list


def room_to_go(curr_x, curr_y, y_dir, plus_minus, box_dict):
    if y_dir and plus_minus < 0:
        return True
    elif y_dir and plus_minus >= 0:
        return True
    elif not y_dir and plus_minus < 0:
        return True
    elif y_dir and plus_minus >= 0:
        return True


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
    return points


if __name__ == "__main__":
    run_frames('qsha')
