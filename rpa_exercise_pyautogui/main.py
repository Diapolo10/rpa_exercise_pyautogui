"""Python code that draws squares on a canvas, and scribbles on them until they're unrecognisable."""

import random
import subprocess
import time
from collections.abc import Generator
from contextlib import contextmanager

import pyautogui
from pygetwindow import Window, getWindowsWithTitle  # type: ignore[import]

from rpa_exercise_pyautogui.config import (
    BOTTOM_RIGHT_PNG,
    CANVAS_EXECUTABLE,
    CONFIDENCE,
    SQUARE_SCREENSHOT,
    SQUARE_SIDE_LENGTH,
    TOP_LEFT_PNG,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_TITLE,
)


@contextmanager
def run_subprocess(*args, **kwargs) -> Generator[subprocess.Popen, None, None]:  # noqa: ANN002,ANN003
    process = subprocess.Popen(*args, **kwargs)  # noqa: S603
    try:
        yield process
    finally:
        process.kill()


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


def random_square_coordinates(count: int,
                              canvas_area: tuple[pyautogui.Point, pyautogui.Point],
                              square_side_length: int = SQUARE_SIDE_LENGTH) -> list[pyautogui.Point]:
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

    return points


def draw_random_line(canvas_area: tuple[pyautogui.Point, pyautogui.Point]) -> None:
    """Draw a random line on the canvas"""

    start_x = random.randrange(int(canvas_area[0].x), int(canvas_area[1].x))
    start_y = random.randrange(int(canvas_area[0].y), int(canvas_area[1].y))
    stop_x = random.randrange(int(canvas_area[0].x), int(canvas_area[1].x))
    stop_y = random.randrange(int(canvas_area[0].y), int(canvas_area[1].y))

    pyautogui.moveTo(
        x=start_x,
        y=start_y,
    )
    pyautogui.dragTo(
        x=stop_x,
        y=stop_y,
    )


def count_squares(canvas_area: tuple[pyautogui.Point, pyautogui.Point]) -> int:
    """Use computer vision to detect squares from the canvas, and count them"""

    squares = list(pyautogui.locateAllOnScreen(
        str(SQUARE_SCREENSHOT),
        region=(int(canvas_area[0].x),
                int(canvas_area[0].y),
                int(canvas_area[1].x),
                int(canvas_area[1].y)),
        grayscale=True,
        confidence=CONFIDENCE,
    ))

    return len(squares)


def main() -> None:
    """Main program"""

    with run_subprocess([CANVAS_EXECUTABLE]):

        time.sleep(1)

        paint_window: Window = getWindowsWithTitle(WINDOW_TITLE)[0]

        paint_window.activate()
        paint_window.restore()
        paint_window.width = WINDOW_DEFAULT_WIDTH
        paint_window.height = WINDOW_DEFAULT_HEIGHT

        pyautogui.moveTo(*paint_window.topleft)

        canvas_bottom_right = pyautogui.center(pyautogui.locateOnScreen(
            str(BOTTOM_RIGHT_PNG),
            region=(int(paint_window.topleft.x),
                    int(paint_window.topleft.y),
                    int(paint_window.bottomright.x),
                    int(paint_window.bottomright.x)),
            grayscale=True,
        ))  # type: ignore[arg-type]

        canvas_top_left = pyautogui.center(pyautogui.locateOnScreen(
            str(TOP_LEFT_PNG),
            region=(int(paint_window.topleft.x),
                    int(paint_window.topleft.y),
                    int(paint_window.bottomright.x),
                    int(paint_window.bottomright.x)),
            grayscale=True,
        ))  # type: ignore[arg-type]


        canvas_area: tuple[pyautogui.Point, pyautogui.Point] = (
            pyautogui.Point(
                canvas_top_left.x,
                canvas_top_left.y,
            ),
            pyautogui.Point(
                canvas_bottom_right.x,
                canvas_bottom_right.y,
            ),
        )

        squares = random_square_coordinates(
            random.randrange(2, 6),
            canvas_area,
            SQUARE_SIDE_LENGTH,
        )

        for point in squares:
            draw_square(point)

        pyautogui.screenshot(
            SQUARE_SCREENSHOT,
            region=(
                int(squares[0].x),
                int(squares[0].y),
                SQUARE_SIDE_LENGTH,
                SQUARE_SIDE_LENGTH,
            ),
        )

        try:
            while (count := count_squares(canvas_area)) > 0:
                print(f"Squares found: {count}")  # noqa: T201
                draw_random_line(canvas_area)

            print("No squares detected, shutting down...")  # noqa: T201

        finally:
            SQUARE_SCREENSHOT.unlink()


if __name__ == '__main__':
    main()
