# IRESS Toy Robot Challenge Solution

## Requirements

Python 3.6+

## Example Usage

	$ ./robot.py < test_commands.txt 
	2,2,NORTH
	0,2,WEST
	4,2,EAST
	2,4,NORTH
	2,0,SOUTH
	2,2,NORTH

	$ ./robot.py < example_input.txt | md5sum - example_output.txt 
	b2c08b97b75e4ad8fac5bc5f588aec6e  -
	b2c08b97b75e4ad8fac5bc5f588aec6e  example_output.txt

## Testing

	$ ./robot_tests.py
