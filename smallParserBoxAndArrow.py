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
            print('space here')
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
                    arrow_coords = pathfind_arrow(box_dict, start_box_id, end_box_id)
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
        return -ARROW_BOLD_SIZE * (arrow_num - 1)
    else:
        return ARROW_BOLD_SIZE * arrow_num


def pathfind_arrow(box_dict, start_box_id, end_box_id):
    start_box = box_dict[start_box_id]
    end_box = box_dict[end_box_id]

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

    big_x = abs(x_diff) > abs(y_diff)

    start_left_block = False
    start_right_block = False
    start_top_block = False
    start_bottom_block = False
    end_left_block = False
    end_right_block = False
    end_top_block = False
    end_bottom_block = False

    for box in box_dict:
        box_left = box_dict[box][0]
        box_right = box_dict[box][0] + box_dict[box][2]
        box_top = box_dict[box][1] + box_dict[box][3]
        box_bottom = box_dict[box][1]
        if box != start_box_id:
            if abs(box_left - (start_box[0] + start_box[2])) < 10 and (box_bottom <= start_box[1] + 2 * start_box[3] / 3 <= box_top):
                start_right_block = True
            if abs(start_box[0] - box_right) <= 10 and (box_bottom <= start_box[1] + 2 * start_box[3] / 3 <= box_top):
                start_left_block = True
            if abs(box_bottom - (start_box[1] + start_box[3])) <= 10 and (box_left <= start_box[0] + 2 * start_box[2] / 3 <= box_right):
                start_top_block = True
            if abs(start_box[1] - box_top) <= 10 and (box_left <= start_box[0] + 2 * start_box[2] / 3 <= box_right):
                start_bottom_block = True
        if box != end_box_id:
            if abs(box_left - (end_box[0] + end_box[2])) < 10 and (box_bottom <= end_box[1] + 2 * end_box[3] / 3 <= box_top):
                end_right_block = True
            if abs(end_box[0] - box_right) <= 10 and (box_bottom <= end_box[1] + 2 * end_box[3] / 3 <= box_top):
                end_left_block = True
            if abs(box_bottom - (end_box[1] + end_box[3])) <= 10 and (box_left <= end_box[0] + 2 * end_box[2] / 3 <= box_right):
                end_top_block = True
            if abs(end_box[1] - box_top) <= 10 and (box_left <= end_box[0] + 2 * end_box[2] / 3 <= box_right):
                end_bottom_block = True

    x1 = -1
    y1 = -1
    desired_x = -1
    desired_y = -1

    if abs(x_diff) > abs(y_diff):
        if x_diff > 0 and not start_left_block and not end_right_block:
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
        elif x_diff <= 0 and not start_right_block and not end_left_block:
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
    elif x1 == -1:
        if y_diff > 0 and not start_bottom_block and not end_top_block:
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
        elif y_diff <= 0 and not start_top_block and not end_bottom_block:
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
    else:
        print('no path able to be created between two boxes: ' + str(end_box_id) + ' and ' + str(start_box_id))
        return []

    old_x = x1
    old_y = y1

    curr_x = x1
    curr_y = y1

    vert_list = []
    displacement = True
    last_y = False

    while curr_x != desired_x or curr_y != desired_y:
        if displacement:
            displacement = False
            if big_x:
                curr_x = (desired_x + curr_x) / 2
                curr_y = old_y
                last_y = False
            else:
                curr_y = (desired_y + curr_y) / 2
                curr_x = old_x
                last_y = True

        elif last_y and curr_x - desired_x != 0:
            curr_x = desired_x
            curr_y = old_y
            last_y = False
        else:
            curr_y = desired_y
            curr_x = old_x
            last_y = True

        vert_list.append([old_x, old_y, curr_x, curr_y])
        old_x = curr_x
        old_y = curr_y

    return vert_list


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
    run_frames('frameSHA')
