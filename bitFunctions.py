# helper functions that can be used in the language
BIT_BYTE = {'0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5', '0110': '6', '0111': '7',
            '1000': '8', '1001': '9', '1010': 'a', '1011': 'b', '1100': 'c', '1101': 'd', '1110': 'e', '1111': 'f'}

BYTE_BIT = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
            '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}


def apply_function(func_name, in_args):
    func_args = []
    for func_arg in in_args:
        func_args.append(func_arg.replace('(', '').replace('*', '').replace(')', ''))
    if func_name == 'bytebit':
        if len(func_args) == 1:
            return byte_to_bit(func_args[0])
        else:
            print('wrong number of args for byte to bit, expected 1 got ' + str(len(func_args)))
    elif func_name == 'bitbyte':
        if len(func_args) == 1:
            return bit_to_byte(func_args[0])
        else:
            print('wrong number of args for bit to byte, expected 1 got ' + str(len(func_args)))
    elif func_name == 'bitshift5':
        if len(func_args) == 1:
            return bit_shift(func_args[0], 5)
        else:
            print('wrong number of args for bit shift 5, expected 1 got ' + str(len(func_args)))
    elif func_name == 'bitshift30':
        if len(func_args) == 1:
            return bit_shift(func_args[0], 30)
        else:
            print('wrong number of args for bit shift 30, expected 1 got ' + str(len(func_args)))
    elif func_name == 'not':
        if len(func_args) == 1:
            return not_bit(func_args[0])
        else:
            print('wrong number of args for not, expected 1 got ' + str(len(func_args)))
    elif func_name == 'mod':
        if len(func_args) == 1:
            return mod_32(func_args[0])
        else:
            print('wrong number of args for modulus, expected 1 got ' + str(len(func_args)))
    elif func_name == 'add':
        if len(func_args) == 2:
            return add_bit(func_args[0], func_args[1])
        else:
            print('wrong number of args for addition, expected 2 got ' + str(len(func_args)))
    elif func_name == 'and':
        if len(func_args) == 2:
            return and_bit(func_args[0], func_args[1])
        else:
            print('wrong number of args for and, expected 2 got ' + str(len(func_args)))
    elif func_name == 'or':
        if len(func_args) == 2:
            return or_bit(func_args[0], func_args[1])
        else:
            print('wrong number of args for or, expected 2 got ' + str(len(func_args)))
    elif func_name == 'xor':
        if len(func_args) == 2:
            return xor_bit(func_args[0], func_args[1])
        else:
            print('wrong number of args for xor, expected 2 got ' + str(len(func_args)))
    elif func_name == '+':
        if len(func_args) == 2:
            return number_add(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical add, expected 2 got ' + str(len(func_args)))
    elif func_name == 'lt' or func_name == 'lessthan':
        if len(func_args) == 2:
            return less_than(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical less than, expected 2 got ' + str(len(func_args)))
    return func_name


def bit_shift(in_bit, shift_len):
    in_bit = in_bit.replace(' ', '')
    first_slice = in_bit[0:shift_len]
    second_slice = in_bit[shift_len:]
    prelim_shift = second_slice + first_slice
    bit_shift_out = ''
    for i in range(0, len(prelim_shift)):
        bit_shift_out += prelim_shift[i]
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit):
            bit_shift_out += ' '
    return bit_shift_out


def byte_to_bit(in_byte):
    in_byte = in_byte.replace(' ', '')
    in_bit = ''
    for i in range(0, len(in_byte)):
        in_bit += BYTE_BIT[in_byte[i]]
        if (i + 1) % 2 == 0 and (i + 1) != len(in_byte):
            in_bit += ' '
    return in_bit


def bit_to_byte(in_bit):
    in_bit = in_bit.replace(' ', '')
    curr_bit = ''
    in_byte = ''
    for i in range(0, len(in_bit)):
        curr_bit += in_bit[i]
        if (i + 1) % 4 == 0:
            in_byte += BIT_BYTE[curr_bit]
            curr_bit = ''
            if (i + 1) % 8 == 0 and (i + 1) != len(in_bit):
                in_byte += ' '
    return in_byte


def add_bit(in_bit_1, in_bit_2):
    in_bit_1 = in_bit_1.replace(' ', '')[::-1]
    in_bit_2 = in_bit_2.replace(' ', '')[::-1]
    if len(in_bit_1) != len(in_bit_2):
        print('error')
    carry_bit = 0
    add_bit_out = ''
    for i in range(0, len(in_bit_1)):
        add_res = int(in_bit_1[i]) + int(in_bit_2[i]) + carry_bit
        if add_res == 0:
            carry_bit = 0
            add_bit_out += '0'
        elif add_res == 1:
            carry_bit = 0
            add_bit_out += '1'
        elif add_res == 2:
            carry_bit = 1
            add_bit_out += '0'
        elif add_res == 3:
            carry_bit = 1
            add_bit_out += '1'
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit_1):
            add_bit_out += ' '
    if carry_bit == 1:
        add_bit_out += '1'
    return add_bit_out[::-1]


def mod_32(in_bit):
    in_bit = in_bit.replace(' ', '')
    if len(in_bit) == 33:
        in_bit = in_bit[1:]
    mod_bit_out = ''
    for i in range(0, len(in_bit)):
        mod_bit_out += in_bit[i]
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit):
            mod_bit_out += ' '
    return mod_bit_out


def and_bit(in_bit_1, in_bit_2):
    in_bit_1 = in_bit_1.replace(' ', '')
    in_bit_2 = in_bit_2.replace(' ', '')
    and_bit_out = ''
    for i in range(0, len(in_bit_1)):
        if in_bit_1[i] == '1' and in_bit_2[i] == '1':
            and_bit_out += '1'
        else:
            and_bit_out += '0'
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit_1):
            and_bit_out += ' '
    return and_bit_out


def or_bit(in_bit_1, in_bit_2):
    in_bit_1 = in_bit_1.replace(' ', '')
    in_bit_2 = in_bit_2.replace(' ', '')
    or_bit_out = ''
    for i in range(0, len(in_bit_1)):
        if in_bit_1[i] == '0' and in_bit_2[i] == '0':
            or_bit_out += '0'
        else:
            or_bit_out += '1'
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit_1):
            or_bit_out += ' '
    return or_bit_out


def xor_bit(in_bit_1, in_bit_2):
    in_bit_1 = in_bit_1.replace(' ', '')
    in_bit_2 = in_bit_2.replace(' ', '')
    or_bit_out = ''
    for i in range(0, len(in_bit_1)):
        if in_bit_1[i] == in_bit_2[i]:
            or_bit_out += '0'
        else:
            or_bit_out += '1'
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit_1):
            or_bit_out += ' '
    return or_bit_out


def not_bit(in_bit):
    in_bit = in_bit.replace(' ', '')
    not_bit_out = ''
    for i in range(0, len(in_bit)):
        if in_bit[i] == '1':
            not_bit_out += '0'
        else:
            not_bit_out += '1'
        if (i + 1) % 8 == 0 and (i + 1) != len(in_bit):
            not_bit_out += ' '
    return not_bit_out


def number_add(num1, num2):
    try:
        return str(int(num1) + int(num2))
    except ValueError:
        print('not an acceptable integer expression: ' + num1 + ' + ' + num2)
        return '0'


def less_than(num1, num2):
    try:
        return int(num1) < int(num2)
    except ValueError:
        print('not an acceptable integer expression: ' + num1 + ' < ' + num2)
        return False

