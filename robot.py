#!/usr/bin/env python3.6

import sys
import re
from enum import Enum, auto

# Regex for PLACE command.
PLACE_RE = re.compile(r'PLACE (\d+),(\d+),(NORTH|SOUTH|EAST|WEST)')


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def on_table(self, ne_corner):
        return 0 <= self.x <= ne_corner.x and 0 <= self.y <= ne_corner.y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

# North-east corner point for default 5 x 5 table top.
# Origin "south-west" corner is (0, 0).
DEFAULT_NE_CORNER = Point(4, 4)

# Sentinel for initial off-table position.
OFF_TABLE_POSITION = Point(-1, -1)


class Orientation(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

# Mapping of table translations given current orientation.
MOVES = {
    Orientation.NORTH: Point(0, 1),
    Orientation.SOUTH: Point(0, -1),
    Orientation.EAST: Point(1, 0),
    Orientation.WEST: Point(-1, 0),
}


class Robot:

    def __init__(self, table_ne_point=DEFAULT_NE_CORNER, report_file=sys.stdout):
        if table_ne_point.x < 1 or table_ne_point.y < 1:
            # Table must be at least 2 x 2 units.
            raise ValueError("Invalid table size!")
        self.table_ne_point = table_ne_point
        self.report_file = report_file
        self.position = OFF_TABLE_POSITION
        # Initial orientation is arbitrary. We use position to determine if
        # robot is on table.
        self.orientation = Orientation.NORTH

    def on_table(self):
        return self.position.on_table(self.table_ne_point)

    def place(self, point, orientation):
        if point.on_table(self.table_ne_point) and orientation in Orientation:
            self.position = point
            self.orientation = orientation

    def turn_left(self):
        if self.on_table():
            # Set new orientation.
            self.orientation = {
                Orientation.NORTH: Orientation.WEST,
                Orientation.SOUTH: Orientation.EAST,
                Orientation.EAST: Orientation.NORTH,
                Orientation.WEST: Orientation.SOUTH,
            }[self.orientation]

    def turn_right(self):
        if self.on_table():
            # Set new orientation.
            self.orientation = {
                Orientation.NORTH: Orientation.EAST,
                Orientation.SOUTH: Orientation.WEST,
                Orientation.EAST: Orientation.SOUTH,
                Orientation.WEST: Orientation.NORTH,
            }[self.orientation]

    def move(self):
        if self.on_table():
            # Only update position if new position is on table.
            new_position = self.position + MOVES[self.orientation]
            if new_position.on_table(self.table_ne_point):
                self.position = new_position

    def report(self):
        if self.on_table():
            print(f'{self.position.x},{self.position.y},{self.orientation.name}', file=self.report_file)


class CommandParser:

    def __init__(self, robot, input_file=sys.stdin):
        self.robot = robot
        self.input_file = input_file

    def run(self):
        for line in self.input_file:
            command = line.strip() # Remove line terminator.
            place_match = PLACE_RE.match(command)
            if place_match:
                x, y, orientation = place_match.groups()
                point = Point(int(x), int(y))
                self.robot.place(point, Orientation[orientation])
            elif command == 'MOVE':
                self.robot.move()
            elif command == 'LEFT':
                self.robot.turn_left()
            elif command == 'RIGHT':
                self.robot.turn_right()
            elif command == 'REPORT':
                self.robot.report()
            else:
                pass # Ignore any invalid command lines.


if __name__ == '__main__':
    robot = Robot()
    parser = CommandParser(robot)
    parser.run()
