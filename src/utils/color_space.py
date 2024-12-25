import pandas as pd
from typing import List, Tuple
from numpy import random


def get_color_space(img=None) -> List[Tuple[int, int, int]]:
    # default lego colors
    default_palette = [
        (38, 38, 38),
        (32, 70, 135),
        (1, 167, 255),
        (190, 236, 250),
        (226, 234, 246),
        (230, 183, 241),
        (222, 40, 29),
        (243, 138, 33),
        (245, 191, 41),
        (244, 219, 65),
        (245, 239, 151),
        (229, 220, 189),
        (210, 150, 100),
        (120, 62, 42),
        (70, 220, 126),
        (197, 234, 66)
    ]
    # TODO: here integrate the image picker
    color_palette = default_palette
    return color_palette


def print_color_text(text, rgb):
    r, g, b = rgbimg_tk
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")


def print_a_colored_square(rgb):
    r, g, b = rgb
    s = f"\033[48;2;{r};{g};{b}m  \033[0m"
    print(
        s + s + s + s + s + s + '\n' + s + s + s + s + s + s + '\n' + s + s + s + s + s + s + '\n' + s + s + s + s + s + s + '\n' + s + s + s + s + s + s + '\n' + s + s + s + s + s + s + '\n')


def get_color_resources(color_palette: List[Tuple[int, int, int]], force_default=True) -> pd.DataFrame:
    """
    For each color in the color palette, collect how many times they shall be used.
    """
    # check if there is cached data, load it if it exists, print it and ask the user if they want to use it
    try:
        df = pd.read_csv('color_resources.csv')
        df = df.set_index('color')
        print("The following color resources are cached:")
        print(df)
        if force_default:
            return df
        use_cached = input("Do you want to use the cached data? (y/n) ")
        if use_cached == 'y':
            return df
    except FileNotFoundError:
        pass
    # convert the list of tuples to a dictionary where tuple entries are keys
    color_resources = {color: 0 for color in color_palette}
    # go through the color palette and ask the user how many times they want to use each color
    color_resources = {}
    for color in color_palette:
        print_a_colored_square(color)
        n = int(input(f"How many times do you want to use the color {color}? "))
        color_resources[color] = n
    # convert it to a dataframe and save it as a CSV file
    df = pd.DataFrame(color_resources.items(), columns=['color', 'n'])
    df.to_csv('color_resources.csv', index=False)
    return df


def get_closest_color(color, color_space, p_second_closest=0) -> Tuple[int, int, int]:
    """
    For a given color, find the closest color in the color space.
    Add the second closest color with a probability of p_second_closest.
    """

    def get(color, color_space):
        closest_color = None
        min_distance = float('inf')
        for c in color_space:
            r2, g2, b2 = c
            d = (r - r2) ** 2 + (g - g2) ** 2 + (b - b2) ** 2
            if d < min_distance:
                min_distance = d
                closest_color = c
        return closest_color

    if color_space == []:
        return (0, 0, 0, 0)  # 100% transparent color

    r, g, b = color[:3]

    closest_color = get(color, color_space)
    color_space.remove(closest_color)
    second_closest_color = get(color, color_space)

    if p_second_closest > 0:
        if random.random() < p_second_closest:
            return second_closest_color

    return closest_color


def get_color_rank(color: Tuple, color_space: List[Tuple[int, int, int]]) -> int:
    """
    For a given color, find the rank of the color in the color space.
    """
    if color_space == []:
        return None
    r, g, b = color[:3]
    rank = 1
    for c in color_space:
        r2, g2, b2 = c
        if (r, g, b) == (r2, g2, b2):
            return rank
        rank += 1
    return rank


if __name__ == "__main__":
    get_color_resources(get_color_space(), force_default=False)
