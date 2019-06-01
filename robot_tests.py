#!/usr/bin/env python3.6

import io
import unittest

from robot import Robot, Point, Orientation, CommandParser


class TestTurns(unittest.TestCase):

    def setUp(self):
        self.robot = Robot()
        self.robot.place(Point(0, 0), Orientation.NORTH)

    def testLeftTurns(self):
        # Check that robot does a 360 counter-clockwise turn.
        self.assertEqual(self.robot.orientation, Orientation.NORTH)
        for orientation in [
            Orientation.WEST,
            Orientation.SOUTH,
            Orientation.EAST,
            Orientation.NORTH
        ]:
            self.robot.turn_left()
            self.assertEqual(self.robot.orientation, orientation)

    def testRightTurns(self):
        # Check that robot does a 360 clockwise turn.
        self.assertEqual(self.robot.orientation, Orientation.NORTH)
        for orientation in [
            Orientation.EAST,
            Orientation.SOUTH,
            Orientation.WEST,
            Orientation.NORTH
        ]:
            self.robot.turn_right()
            self.assertEqual(self.robot.orientation, orientation)


class TestPlacement(unittest.TestCase):

    def setUp(self):
        self.robot = Robot()

    def testCommandSequence(self):
        # Check that robot ignores invalid placements.
        self.assertFalse(self.robot.on_board())
        for invalid in [(-1, -1), (-1, 0), (0, -1), (0, 5), (5, 0), (5, 5)]:
            self.robot.place(Point(*invalid), Orientation.NORTH)
            self.assertFalse(self.robot.on_board())
        self.robot.place(Point(0, 0), Orientation.NORTH)
        # Thunderbirds Are Go!
        self.assertTrue(self.robot.on_board())


class TestCommandParserAndReports(unittest.TestCase):

    def setUp(self):
        self.output = io.StringIO()
        self.robot = Robot(report_file=self.output)

    def test(self):
        # Traverse whole grid and check that parser correctly dispatches commands,
        # including ignoring invalid commands, and robot correctly reports its position,
        # and ignores commands that would move it off the board.
        command_file = io.StringIO(
'''
# Invalid: no orientation.
PLACE 0,0
REPORT

# Invalid: off board.
PLACE 0,10,NORTH
REPORT

PLACE 0,0,NORTH
REPORT
# Invalid: off board.
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
        parser = CommandParser(self.robot, command_file)
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
        self.assertMultiLineEqual(self.output.getvalue(), report_lines)


if __name__ == '__main__':
    unittest.main()
