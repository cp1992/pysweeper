def flatten(list):
    return [item for sublist in list for item in sublist]


def get_screen_horizontal_center(root, offset=0):
    screen_width = root.winfo_screenwidth() - offset
    return int(screen_width / 2)
