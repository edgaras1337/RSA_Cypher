def to_int(val, default=0):
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def to_string(array):
    msg = ""

    for num in array:
        msg += chr(num)

    return msg


def to_num_array(msg):
    array = []

    for c in msg:
        array.append(ord(c))

    return array
