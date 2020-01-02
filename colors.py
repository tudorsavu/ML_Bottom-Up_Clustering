# color cycler
col = [
    (0.9, 0.9, 0),
    (0.9, 0, 0.9),
    (0, 0.9, 0.9),
    (0, 0.75, 0.75),
    (0.75, 0, 0.75),
    (0.75, 0.75, 0),
    (0.75, 0.75, 0.75),
    (0.25, 1, 0.25),
    (0.25, 0.25, 1),
    (0.25, 0.25, 0.25),
    (0.5, 0.5, 1),
    (0.5, 1, 0.5),
    (1, 0.5, 0.5),
    (0.5, 0.5, 0.5),
    (0, 0, 0.5),
    (0, 0.5, 0),
    (0.5, 0, 0),
    (0, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 0)]

col_iterator = 0


def get_color(size):
    global col_iterator
    if col_iterator > len(col) - 1:
        col_iterator = 0
    color = col[col_iterator]
    colors = []
    for it in range(0, size):
        colors.append(color)
    col_iterator += 1
    return colors
