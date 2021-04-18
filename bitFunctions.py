# helper functions that can be used in the language
BIT_BYTE = {'0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5', '0110': '6', '0111': '7',
            '1000': '8', '1001': '9', '1010': 'a', '1011': 'b', '1100': 'c', '1101': 'd', '1110': 'e', '1111': 'f'}

BYTE_BIT = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
            '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}

ROT_TABLE = [[ 0, 36,  3, 41, 18],
             [ 1, 10, 44, 45,  2],
             [62,  6, 43, 15, 61],
             [28, 55, 25, 21, 56],
             [27, 20, 39,  8, 14]]

K_RCs = ['00 00 00 00 00 00 00 01', '00 00 00 00 00 00 80 82', '80 00 00 00 00 00 80 8a', '80 00 00 00 80 00 80 00',
         '00 00 00 00 00 00 80 8b', '00 00 00 00 80 00 00 01', '80 00 00 00 80 00 80 81', '80 00 00 00 00 00 80 09',
         '00 00 00 00 00 00 00 8a', '00 00 00 00 00 00 00 88', '00 00 00 00 80 00 80 09', '00 00 00 00 80 00 00 0a',
         '00 00 00 00 80 00 80 8b', '80 00 00 00 00 00 00 8b', '80 00 00 00 00 00 80 89', '80 00 00 00 00 00 80 03',
         '80 00 00 00 00 00 80 02', '80 00 00 00 00 00 00 80', '00 00 00 00 00 00 80 0a', '80 00 00 00 80 00 00 0a',
         '80 00 00 00 80 00 80 81', '80 00 00 00 00 00 80 80', '00 00 00 00 80 00 00 01', '80 00 00 00 80 00 80 08']


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
    elif func_name == 'lbitshift5':
        if len(func_args) == 1:
            return lbit_shift(func_args[0], 5)
        else:
            print('wrong number of args for bit shift 5, expected 1 got ' + str(len(func_args)))
    elif func_name == 'lbitshift30':
        if len(func_args) == 1:
            return lbit_shift(func_args[0], 30)
        else:
            print('wrong number of args for bit shift 30, expected 1 got ' + str(len(func_args)))
    elif func_name == 'rbitshift2':
        if len(func_args) == 1:
            return rbit_shift(func_args[0], 2)
        else:
            print('wrong number of args for bit shift, expected 1 got ' + str(len(func_args)))
    elif func_name == 'rbitshift13':
        if len(func_args) == 1:
            return rbit_shift(func_args[0], 13)
        else:
            print('wrong number of args for bit shift, expected 1 got ' + str(len(func_args)))
    elif func_name == 'rbitshift22':
        if len(func_args) == 1:
            return rbit_shift(func_args[0], 22)
        else:
            print('wrong number of args for bit shift, expected 1 got ' + str(len(func_args)))
    elif func_name == 'rbitshift6':
        if len(func_args) == 1:
            return rbit_shift(func_args[0], 6)
        else:
            print('wrong number of args for bit shift, expected 1 got ' + str(len(func_args)))
    elif func_name == 'rbitshift':
        if len(func_args) == 2:
            return rbit_shift(func_args[0], int(func_args[1]))
        else:
            print('wrong number of args for bit shift, expected 2 got ' + str(len(func_args)))
    elif func_name == 'rbitshift11':
        if len(func_args) == 1:
            return rbit_shift(func_args[0], 11)
        else:
            print('wrong number of args for bit shift, expected 1 got ' + str(len(func_args)))
    elif func_name == 'rbitshift25':
        if len(func_args) == 1:
            return rbit_shift(func_args[0], 25)
        else:
            print('wrong number of args for bit shift, expected 1 got ' + str(len(func_args)))
    elif func_name == 'not':
        if len(func_args) == 1:
            return not_bit(func_args[0])
        else:
            print('wrong number of args for not, expected 1 got ' + str(len(func_args)))
    elif func_name == 'mod32':
        if len(func_args) == 1:
            return mod_32(func_args[0])
        else:
            print('wrong number of args for modulus, expected 1 got ' + str(len(func_args)))
    elif func_name == 'trunc32':
        if len(func_args) == 1:
            return trunc_32(func_args[0])
        else:
            print('wrong number of args for truncate to 32 bytes, expected 1 got ' + str(len(func_args)))
    elif func_name == 'first272':
        if len(func_args) == 1:
            return first_272(func_args[0])
        else:
            print('wrong number of args for first 272 bytes, expected 1 got ' + str(len(func_args)))
    elif func_name == 'last128':
        if len(func_args) == 1:
            return last_128(func_args[0])
        else:
            print('wrong number of args for last 128 bytes, expected 1 got ' + str(len(func_args)))
    elif func_name == 'last384':
        if len(func_args) == 1:
            return last_384(func_args[0])
        else:
            print('wrong number of args for last 384 bytes, expected 1 got ' + str(len(func_args)))
    elif func_name == 'theta':
        if len(func_args) == 1:
            return theta(func_args[0])
        else:
            print('wrong number of args for Theta, expected 1 got ' + str(len(func_args)))
    elif func_name == 'roh':
        if len(func_args) == 1:
            return roh(func_args[0])
        else:
            print('wrong number of args for Roh, expected 1 got ' + str(len(func_args)))
    elif func_name == 'pi':
        if len(func_args) == 1:
            return pi(func_args[0])
        else:
            print('wrong number of args for Pi, expected 1 got ' + str(len(func_args)))
    elif func_name == 'chi':
        if len(func_args) == 1:
            return chi(func_args[0])
        else:
            print('wrong number of args for Chi, expected 1 got ' + str(len(func_args)))
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
    elif func_name == 'indexarr':
        if len(func_args) == 2:
            return index_arr(func_args[0], func_args[1])
        else:
            print('wrong number of args for indexing array, expected 3 got ' + str(len(func_args)))
    elif func_name == 'indexmat':
        if len(func_args) == 3:
            return index_mat(func_args[0], func_args[1], func_args[2])
        else:
            print('wrong number of args for indexing matrix, expected 3 got ' + str(len(func_args)))
    elif func_name == '+':
        if len(func_args) == 2:
            return number_add(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical add, expected 2 got ' + str(len(func_args)))
    elif func_name == '-':
        if len(func_args) == 2:
            return number_sub(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical subtract, expected 2 got ' + str(len(func_args)))
    elif func_name == '*':
        if len(func_args) == 2:
            return number_mult(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical multiply, expected 2 got ' + str(len(func_args)))
    elif func_name == 'mod':
        if len(func_args) == 2:
            return number_mod(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical mod, expected 2 got ' + str(len(func_args)))
    elif func_name == 'lt' or func_name == 'lessthan':
        if len(func_args) == 2:
            return less_than(func_args[0], func_args[1])
        else:
            print('wrong number of args for numerical less than, expected 2 got ' + str(len(func_args)))
    elif func_name == 'concat':
        if len(func_args) == 2:
            return concat(func_args[0], func_args[1])
        else:
            print('wrong number of args for concatenation, expected 2 got ' + str(len(func_args)))
    elif func_name == 'kf1600':
        if len(func_args) == 2:
            return keccak_f_1600(func_args[0], func_args[1])
        else:
            print('wrong number of args for keccak-f[1600], expected 2 got ' + str(len(func_args)))
    elif func_name == 'iota':
        if len(func_args) == 2:
            return iota(func_args[0], func_args[1])
        else:
            print('wrong number of args for Iota, expected 2 got ' + str(len(func_args)))
    elif func_name == 'xorloop':
        if len(func_args) == 2:
            return xor_loop(func_args[0], func_args[1])
        else:
            print('wrong number of args for XOR loop, expected 2 got ' + str(len(func_args)))
    elif func_name == 'cfunc':
        if len(func_args) == 1:
            return c_func(func_args[0])
        else:
            print('wrong number of args for C function, expected 1 got ' + str(len(func_args)))
    elif func_name == 'dfunc':
        if len(func_args) == 1:
            return d_func(func_args[0])
        else:
            print('wrong number of args for D function, expected 1 got ' + str(len(func_args)))
    return func_name


def lbit_shift(in_bit, shift_len):
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


def rbit_shift(in_bit, shift_len):
    in_bit = in_bit.replace(' ', '')
    first_slice = in_bit[0:len(in_bit)-shift_len]
    second_slice = in_bit[len(in_bit)-shift_len:]
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


def number_sub(num1, num2):
    try:
        return str(int(num1) - int(num2))
    except ValueError:
        print('not an acceptable integer expression: ' + num1 + ' - ' + num2)
        return '0'


def number_mod(num1, num2):
    try:
        return str(int(num1) % int(num2))
    except ValueError:
        print('not an acceptable integer expression: ' + num1 + ' mod ' + num2)
        return '0'


def number_mult(num1, num2):
    try:
        return str(int(num1) * int(num2))
    except ValueError:
        print('not an acceptable integer expression: ' + num1 + ' * ' + num2)
        return '0'


def less_than(num1, num2):
    try:
        return int(num1) < int(num2)
    except ValueError:
        print('not an acceptable integer expression: ' + num1 + ' < ' + num2)
        return False


def concat(num1, num2):
    return num1 + num2


def trunc_32(in_byte):
    in_byte = in_byte.replace(' ', '')
    out_byte = ''
    for i in range(0, len(in_byte)):
        if i == 64:
            return out_byte
        out_byte += in_byte[i]
        if (i + 1) % 2 == 0 and (i + 1) != len(in_byte):
            out_byte += ' '
    return out_byte


def first_272(in_byte):
    in_byte = in_byte.replace(' ', '')
    out_byte = ''
    for i in range(0, len(in_byte)):
        if i == 272:
            return out_byte
        out_byte += in_byte[i]
        if (i + 1) % 2 == 0 and (i + 1) != len(in_byte):
            out_byte += ' '
    return out_byte


def last_128(in_byte):
    in_byte = in_byte.replace(' ', '')
    out_byte = ''
    for i in range(272, len(in_byte)):
        out_byte += in_byte[i]
        if (i + 1) % 2 == 0 and (i + 1) != len(in_byte):
            out_byte += ' '
    return out_byte


def last_384(in_byte):
    in_byte = in_byte.replace(' ', '')
    out_byte = ''
    for i in range(16, len(in_byte)):
        out_byte += in_byte[i]
        if (i + 1) % 2 == 0 and (i + 1) != len(in_byte):
            out_byte += ' '
    return out_byte


def rot(i1, i2):
    return ROT_TABLE[i1][i2]


def create_mat(a):
    a_mat = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    a = a.replace(' ', '')
    curr_i = 0
    curr_sub_i = 0
    for i in range(0, len(a)):
        if i != 0 and i % 64 == 0:
            a_mat[curr_i][curr_sub_i] = a[i-64:i]
            curr_sub_i += 1
        if i != 0 and i % 320 == 0:
            curr_i += 1
            curr_sub_i = 0
    a_mat[4][4] = a[(len(a)-64):]
    return a_mat


def un_matrix(in_mat):
    out_str = ''
    for x in range(0, len(in_mat)):
        for y in range(0, len(in_mat[x])):
            out_str += in_mat[x][y]
            out_str += ' '
    return out_str[:len(out_str) - 1]


def un_arr(in_arr):
    out_str = ''
    for x in range(0, len(in_arr)):
        out_str += in_arr[x]
        out_str += ' '
    return out_str[:len(out_str) - 1]


def create_arr(in_str):
    a_arr = ['', '', '', '', '']
    in_str = in_str.replace(' ', '')
    curr_i = 0
    for i in range(0, len(in_str)):
        if i != 0 and i % 64 == 0:
            a_arr[curr_i] = in_str[i - 64:i]
            curr_i += 1
    a_arr[4] = in_str[(len(in_str) - 64):]
    return a_arr


def c_func(a):
    a = byte_to_bit(a)
    a = create_mat(a)
    c = ['', '', '', '', '']
    for x in range(0, 5):
        c[x] = xor_bit(xor_bit(xor_bit(xor_bit(a[x][0], a[x][1]), a[x][2]), a[x][3]), a[x][4])

    return bit_to_byte(un_arr(c))


def d_func(c_in):
    c_in = byte_to_bit(c_in)
    c_in = create_arr(c_in)
    d = ['', '', '', '', '']
    for x in range(0, 5):
        xplus = x + 1
        if xplus > 4:
            xplus = 0
        d[x] = xor_bit(c_in[x-1], rbit_shift(c_in[xplus], 1))
    return bit_to_byte(un_arr(d))


def xor_loop(a, d):
    a = byte_to_bit(a)
    a = create_mat(a)
    d = byte_to_bit(d)
    d = create_arr(d)

    for x in range(0, 5):
        for y in range(0, 5):
            a[x][y] = xor_bit(a[x][y], d[x])
    return bit_to_byte(un_matrix(a))


def theta(a):
    a = byte_to_bit(a)
    a = create_mat(a)

    c = ['', '', '', '', '']
    d = ['', '', '', '', '']
    for x in range(0, 5):
        c[x] = xor_bit(xor_bit(xor_bit(xor_bit(a[x][0], a[x][1]), a[x][2]), a[x][3]), a[x][4])

    for x in range(0, 5):
        xplus = x + 1
        if xplus > 4:
            xplus = 0
        d[x] = xor_bit(c[x-1], rbit_shift(c[xplus], 1))

    for x in range(0, 5):
        for y in range(0, 5):
            a[x][y] = xor_bit(a[x][y], d[x])

    return bit_to_byte(un_matrix(a))


def roh(theta_o):
    theta_o = byte_to_bit(theta_o)
    theta_o = create_mat(theta_o)
    for x in range(0, 5):
        for y in range(0, 5):
            theta_o[x][y] = rbit_shift(theta_o[x][y], rot(x, y))
    return bit_to_byte(un_matrix(theta_o))


def pi(roh_o):
    roh_o = byte_to_bit(roh_o)
    roh_o = create_mat(roh_o)
    for x in range(0, 5):
        for y in range(0, 5):
            second_index = 2 * x + 3 * y
            second_index = second_index % 5
            roh_o[y][second_index] = roh_o[x][y]
    return bit_to_byte(un_matrix(roh_o))


def chi(pi_o):
    pi_o = byte_to_bit(pi_o)
    pi_old = create_mat(pi_o)
    chi_out = pi_old.copy()
    for x in range(0, 5):
        for y in range(0, 5):
            chi_out[x][y] = xor_bit(pi_old[x][y], and_bit(not_bit(pi_old[(x+1) % 5][y]), pi_old[(x+2) % 5][y]))
    return bit_to_byte(un_matrix(chi_out))


def iota(chi_o, rc):
    chi_o = byte_to_bit(chi_o)
    chi_o = create_mat(chi_o)
    chi_o[0][0] = xor_bit(chi_o[0][0], byte_to_bit(rc))
    return bit_to_byte(un_matrix(chi_o))


def keccak_f_1600(rate, capacity):
    a = rate + ' ' + capacity
    for i in range(0, 24):
        a = iota(chi(pi(roh(theta(a)))), K_RCs[i])
    return a


def index_mat(a, index1, index2):
    a = byte_to_bit(a)
    a = create_mat(a)
    if int(index1) >= len(a):
        print("invalid index " + index1 + ' for matrix of length ' + str(len(a)))
        return '0'
    if int(index2) >= len(a[int(index1)]):
        print("invalid index " + index2 + ' for array of length ' + str(len(a[index1])))
        return '0'
    return bit_to_byte(a[int(index1)][int(index2)])


def index_arr(a, index1):
    a = byte_to_bit(a)
    a = create_arr(a)
    if int(index1) >= len(a):
        print("invalid index " + index1 + ' for array of length ' + str(len(a)))
        return '0'
    return bit_to_byte(a[int(index1)])
