from __future__ import division
import re


__all__ = ["ratio"]


def convert_color_to_rgb(color):
    if type(color) is list:
        if len(color) != 3:
            raise ValueError
        return color

    if type(color) is tuple:
        if len(color) != 3:
            raise ValueError
        return list(color)

    result = re.match(r"^#?([a-f0-9|A-F0-9]{6,6})$", color)

    result_array = list(result.group(1))

    if len(result_array) == 0:
        raise ValueError

    result_array = [
        result_array[i] + result_array[i + 1] for i in range(0, len(result_array), 2)
    ]

    return [int(hex_code, 16) for hex_code in result_array]


def get_luminance(rgb_hex):
    sRGB = float(rgb_hex) / 255

    if sRGB <= 0.03928:
        return sRGB / 12.92
    else:
        return ((sRGB + 0.055) / 1.055) ** 2.4


def get_relative_luminance(rgb_array):
    r = get_luminance(rgb_array[0])
    g = get_luminance(rgb_array[1])
    b = get_luminance(rgb_array[2])

    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(color_1, color_2):
    rgb_array_1 = convert_color_to_rgb(color_1)
    rgb_array_2 = convert_color_to_rgb(color_2)

    if sum(rgb_array_1) > sum(rgb_array_2):
        lighter = rgb_array_1
        darker = rgb_array_2
    else:
        lighter = rgb_array_2
        darker = rgb_array_1

    contrast_ratio = (get_relative_luminance(lighter) + 0.05) / (
        get_relative_luminance(darker) + 0.05
    )

    return contrast_ratio
