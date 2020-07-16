import hashlib


def color_based_on_the_string_value(value):
    """
    To create a color based on the argument value (only string)

    :param value: the string value
    :type value: str

    :return: hexadecimal color based on the value
    :rtype: str
    """
    return f"#{hashlib.shake_256(bytes(value , encoding='utf-8')).hexdigest(3)}"