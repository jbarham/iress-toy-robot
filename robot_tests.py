#!/usr/bin/env python3.6

import io
import unittest

from robot import Robot, Point, Orientation, CommandParser


class TestTurns(unittest.TestCase):

    def testLeftTurns(self):
        # Check that robot does a 360 counter-clockwise turn.
        robot = Robot()
        robot.place(Point(0, 0), Orientation.NORTH)
        self.assertEqual(robot.orientation, Orientation.NORTH)
        for orientation in [
            Orientation.WEST,
            Orientation.SOUTH,
            Orientation.EAST,
            Orientation.NORTH
        ]:
            robot.turn_left()
            self.assertEqual(robot.orientation, orientation)

    def testRightTurns(self):
        robot = Robot()
        robot.place(Point(0, 0), Orientation.NORTH)
        # Check that robot does a 360 clockwise turn.
        self.assertEqual(robot.orientation, Orientation.NORTH)
        for orientation in [
            Orientation.EAST,
            Orientation.SOUTH,
            Orientation.WEST,
            Orientation.NORTH
        ]:
            robot.turn_right()
            self.assertEqual(robot.orientation, orientation)


class TestPlacement(unittest.TestCase):

    def testInvalidPlacements(self):
        robot = Robot()
        invalid_places = [(-1, -1), (-1, 0), (0, -1), (0, 5), (5, 0), (5, 5)]
        # Check that robot ignores invalid placements.
        self.assertFalse(robot.on_table())
        for invalid in invalid_places:
            robot.place(Point(*invalid), Orientation.NORTH)
            self.assertFalse(robot.on_table())
        robot.place(Point(0, 0), Orientation.NORTH)
        # Thunderbirds Are Go!
        self.assertTrue(robot.on_table())
        # Check that robot ignores invalid placements after it's on the table.
        for invalid in invalid_places:
            robot.place(Point(*invalid), Orientation.NORTH)
            self.assertTrue(robot.on_table())

    def testInvalidTableSizes(self):
        for invalid in [(-1, -1), (0, 0), (0, 1), (1, 0)]:
            with self.assertRaises(ValueError):
                Robot(Point(*invalid))

    def testValidTableSizes(self):
        for valid in [(1, 1), (1, 2), (2, 1), (5, 5), (50, 50), (1, 50)]:
            Robot(Point(*valid))


class TestCommandParserAndReports(unittest.TestCase):

    def test(self):
        output = io.StringIO()
        robot = Robot(report_file=output)
        # Traverse whole grid and check that parser correctly dispatches commands,
        # including ignoring invalid commands, and robot correctly reports its position,
        # and ignores commands that would move it off the table.
        command_file = io.StringIO(
'''
# Invalid: no orientation.
PLACE 0,0
REPORT

# Invalid: off table.
PLACE 0,10,NORTH
REPORT

PLACE 0,0,NORTH
REPORT
# Invalid: off table.
PLACE 5,5,NORTH
# Robot position should be unchanged.
REPORT

# Moving up the first column.
MOVE
Hello, world!
REPORT
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
RIGHT
REPORT


White space.


MOVE
REPORT
RIGHT
I believe that robots are stealing my luggage.  -- Steve Martin.
REPORT

# Down the second column.
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
LEFT
REPORT
MOVE
REPORT
/* Not a C program. */
LEFT
REPORT

# Up the third.
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
// Not a C++ program either.
RIGHT
REPORT
MOVE
REPORT
RIGHT
Good news: that gum you like is going to come back into style.
REPORT

# Down the fourth.
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
LEFT
REPORT
MOVE
REPORT
LEFT
REPORT

# Up the fifth.
MOVE
Attention, Eduardo, the moon is red.
REPORT
MOVE
REPORT
MOVE
REPORT
MOVE
REPORT
# This move should be ignored.
MOVE
REPORT
'''
)
        parser = CommandParser(robot, command_file)
        parser.run()
        report_lines = '''0,0,NORTH
0,0,NORTH
0,1,NORTH
0,2,NORTH
0,3,NORTH
0,4,NORTH
0,4,EAST
1,4,EAST
1,4,SOUTH
1,3,SOUTH
1,2,SOUTH
1,1,SOUTH
1,0,SOUTH
1,0,EAST
2,0,EAST
2,0,NORTH
2,1,NORTH
2,2,NORTH
2,3,NORTH
2,4,NORTH
2,4,EAST
3,4,EAST
3,4,SOUTH
3,3,SOUTH
3,2,SOUTH
3,1,SOUTH
3,0,SOUTH
3,0,EAST
4,0,EAST
4,0,NORTH
4,1,NORTH
4,2,NORTH
4,3,NORTH
4,4,NORTH
4,4,NORTH
'''
        self.assertMultiLineEqual(output.getvalue(), report_lines)


if __name__ == '__main__':
    unittest.main()
