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
                    box_dict[box_id] = [x, y, width, height, box_text, box_bold, user_box_color]
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
                    arrow_coords = pathfind_arrow(box_dict, start_box_id, end_box_id, arrow_dict)
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


def create_arrowhead(arrow_lines, arrowhead_thickness):
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
        print('Bad Last Arrow: Code Error!' + str(arrow_lines))
    return points


if __name__ == "__main__":
    run_frames('fullShaStartFrame')
