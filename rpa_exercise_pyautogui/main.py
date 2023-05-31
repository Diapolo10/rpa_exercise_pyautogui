import random
import subprocess
import time
from pathlib import Path

import pyautogui
from pygetwindow import getWindowsWithTitle, Window  # type: ignore[import]

from rpa_exercise_pyautogui.config import (
    CANVAS_OFFSET_TOP_LEFT,
    DEFAULT_CANVAS_HEIGHT,
    DEFAULT_CANVAS_WIDTH,
    SQUARE_SIDE_LENGTH,
    WINDOW_TITLE,
)


SQUARE_SCREENSHOT = Path(__file__).parent / 'images' / 'square.png'  # TODO: Swap to importlib.resources

subprocess.Popen(['mspaint'])

time.sleep(1)


PAINT_WINDOW: Window = getWindowsWithTitle(WINDOW_TITLE)[0]
CANVAS_AREA: tuple[pyautogui.Point, pyautogui.Point] = (
    pyautogui.Point(
        PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_LEFT.x,
        PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_LEFT.y,
    ),
    pyautogui.Point(
        PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_LEFT.x + DEFAULT_CANVAS_WIDTH,
        PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_LEFT.y + DEFAULT_CANVAS_HEIGHT,
    ),
)

PAINT_WINDOW.activate()
PAINT_WINDOW.restore()
pyautogui.moveTo(*PAINT_WINDOW.topleft)
# pyautogui.screenshot("./test.png", region=(PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_LEFT.x, PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_LEFT.y, DEFAULT_CANVAS_WIDTH, DEFAULT_CANVAS_HEIGHT))


def draw_square(top_left: pyautogui.Point | tuple[int, int], side_length: int = SQUARE_SIDE_LENGTH) -> None:
    """
    Draws a square at a desired point on the canvas
    
    NOTE: Does not perform any boundary checking.
    """

    pyautogui.moveTo(top_left)
    pyautogui.drag(xOffset=+side_length)
    pyautogui.drag(yOffset=+side_length)
    pyautogui.drag(xOffset=-side_length)
    pyautogui.drag(yOffset=-side_length)


def random_square_coordinates(count: int, canvas_area: tuple[pyautogui.Point, pyautogui.Point], square_side_length: int) -> list[pyautogui.Point]:
    """
    Returns the desired number of starting points for non-overlapping squares in random positions
    
    NOTE: The function may halt if the canvas does not have enough room for the desired number of squares.
    """

    points: list[pyautogui.Point] = []
    invalid_points: set[tuple[int, int]] = set()

    while len(points) < count:
        x_coord = random.choice(range(int(canvas_area[0].x), int(canvas_area[1].x) - square_side_length))
        y_coord = random.choice(range(int(canvas_area[0].y), int(canvas_area[1].y) - square_side_length))

        if (x_coord, y_coord) not in invalid_points:
            points.append(pyautogui.Point(x_coord, y_coord))
            for bad_x in range(x_coord-square_side_length, x_coord+square_side_length+1):
                for bad_y in range(y_coord-square_side_length, y_coord+square_side_length+1):
                    invalid_points.add((bad_x, bad_y))

    print(points)
    # print(invalid_points)

    return points


print(PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_LEFT.x)
print(PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_LEFT.y)
print(PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_LEFT.x + DEFAULT_CANVAS_WIDTH)
print(PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_LEFT.y + DEFAULT_CANVAS_HEIGHT)

for point in random_square_coordinates(random.randrange(2, 6), CANVAS_AREA, SQUARE_SIDE_LENGTH):
    draw_square(point)


# pyautogui.moveTo(*PAINT_WINDOW.topleft)
# pyautogui.moveTo(PAINT_WINDOW.topleft.x + OFFSET_TOP_RIGHT.x + (DEFAULT_CANVAS_WIDTH // 2), PAINT_WINDOW.topleft.y + OFFSET_TOP_RIGHT.y + (DEFAULT_CANVAS_HEIGHT // 2), duration=1)
# draw_square(pyautogui.Point(PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_RIGHT.x + (DEFAULT_CANVAS_WIDTH // 2), PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_RIGHT.y + (DEFAULT_CANVAS_HEIGHT // 2)))
# draw_square(pyautogui.Point(PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_RIGHT.x + (DEFAULT_CANVAS_WIDTH // 4), PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_RIGHT.y + (DEFAULT_CANVAS_HEIGHT // 2)))
# draw_square(pyautogui.Point(PAINT_WINDOW.topleft.x + CANVAS_OFFSET_TOP_RIGHT.x + DEFAULT_CANVAS_WIDTH - (DEFAULT_CANVAS_WIDTH // 4), PAINT_WINDOW.topleft.y + CANVAS_OFFSET_TOP_RIGHT.y + (DEFAULT_CANVAS_HEIGHT // 2)))
