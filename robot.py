#!/usr/bin/env python3.6

import sys
import re
from enum import Enum, auto

# Hardcoded 5x5 tile board size.
MAX_X, MAX_Y = 4, 4

# Regex for PLACE command.
PLACE_RE = re.compile(r'PLACE (\d+),(\d+),(NORTH|SOUTH|EAST|WEST)')


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def on_board(self):
        return 0 <= self.x <= MAX_X and 0 <= self.y <= MAX_Y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

# Sentinel for initial off-board position.
OFF_BOARD_POSITION = Point(-1, -1)


class Orientation(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

# Mapping of board translations given current orientation.
MOVES = {
    Orientation.NORTH: Point(0, 1),
    Orientation.SOUTH: Point(0, -1),
    Orientation.EAST: Point(1, 0),
    Orientation.WEST: Point(-1, 0),
}


class Robot:

    def __init__(self, report_file=sys.stdout):
        self.report_file = report_file
        self.position = OFF_BOARD_POSITION
        # Initial orientation is arbitrary. We use position to determine if
        # robot is on board.
        self.orientation = Orientation.NORTH

    def on_board(self):
        return self.position.on_board()

    def place(self, point, orientation):
        if point.on_board() and orientation in Orientation:
            self.position = point
            self.orientation = orientation
            return True
        return False

    def turn_left(self):
        if self.on_board():
            # Set new orientation.
            self.orientation = {
                Orientation.NORTH: Orientation.WEST,
                Orientation.SOUTH: Orientation.EAST,
                Orientation.EAST: Orientation.NORTH,
                Orientation.WEST: Orientation.SOUTH,
            }[self.orientation]
            return True
        return False

    def turn_right(self):
        if self.on_board():
            # Set new orientation.
            self.orientation = {
                Orientation.NORTH: Orientation.EAST,
                Orientation.SOUTH: Orientation.WEST,
                Orientation.EAST: Orientation.SOUTH,
                Orientation.WEST: Orientation.NORTH,
            }[self.orientation]
            return True
        return False

    def move(self):
        if self.on_board():
            # Only update position if new position is on board.
            new_position = self.position + MOVES[self.orientation]
            if new_position.on_board():
                self.position = new_position
                return True
        return False

    def report(self):
        if self.on_board():
            print(f'{self.position.x},{self.position.y},{self.orientation.name}', file=self.report_file)
            return True
        return False


class CommandParser:

    def __init__(self, robot, input_file=sys.stdin):
        self.robot = robot
        self.input_file = input_file
        # Flag that's set after first successful placement of robot on board.
        self.robot_placed = False

    def run(self):
        for line in self.input_file:
            line = line.strip() # Remove line terminator.
            place_match = PLACE_RE.match(line)
            # If robot hasn't been placed on board and current command
            # is not a PLACE command, ignore current command line.
            if not self.robot_placed and not place_match:
                continue
            if place_match:
                x, y, orientation = place_match.groups()
                point = Point(int(x), int(y))
                self.robot.place(point, Orientation[orientation])
                if self.robot.on_board():
                    # Valid PLACE command has been executed.
                    self.robot_placed = True
            elif line == 'MOVE':
                self.robot.move()
            elif line == 'LEFT':
                self.robot.turn_left()
            elif line == 'RIGHT':
                self.robot.turn_right()
            elif line == 'REPORT':
                self.robot.report()
            else:
                pass # Ignore any invalid command lines.


if __name__ == '__main__':
    robot = Robot()
    parser = CommandParser(robot)
    parser.run()
