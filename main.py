def rgb_distance(color1, color2):
    """
    Calculate the distance between two colors in the RGB color space.
    :param color1: RGB color value 1
    :param color2: RGB color value 2
    :return: distance between color1 and color2

    >>> color1 = 0x8a3324
    >>> color2 = 0x0000FF
    >>> distance = rgb_distance(color1, color2)
    >>> print(f"Distance between color1 and color2: {distance:.2f}")
    Distance between color1 and color2: 263.83
    """
    red1 = color1 >> 16 & 0xff
    green1 = color1 >> 8 & 0xff
    blue1 = color1 & 0xff

    red2 = color2 >> 16 & 0xff
    green2 = color2 >> 8 & 0xff
    blue2 = color2 & 0xff

    distance = ((red1 - red2) ** 2 + (green1 - green2) ** 2 + (blue1 - blue2) ** 2) ** 0.5
    return distance

def rgb_center(colors):
    """
    Calculate the average color of a sequence of colors in the RGB color space.
    :param colors: sequence of RGB color values
    :return: average color

    >>> colors = [0xFF0000, 0x00FF00, 0x0000FF]
    >>> average_color = rgb_center(colors)
    >>> print(f"Average color: {average_color:#06x}")
    Average color: 0x555555
    """
    total_red = 0
    total_green = 0
    total_blue = 0

    for color in colors:
        total_red += color >> 16 & 0xff
        total_green += color >> 8 & 0xff
        total_blue += color & 0xff

    average_red = total_red // len(colors)
    average_green = total_green // len(colors)
    average_blue = total_blue // len(colors)

    average_color = average_red << 16 | average_green << 8 | average_blue
    return average_color


