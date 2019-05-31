# Lawn-mower

(The mower can be programmed to mow the entire surface.)
The position of the mower can be represented by coordinates (x,y) and by a letter giving the cardinal direction (N,E,W,S). The lawn is divided into a grid to simplify the navigation.

For example, a mower position can be « 0, 0, N », it means that this mower is located at the lower-left corner of the lawn, and it is oriented North.
The mower is controlled by sending it a sequence of letters. Possible letters are « R », « L » and « F ». « R » and « L » make the mower rotate of 90° respectively to the left or to the right, without moving. « F » means that the mower is moving forward on the cell in front of it, without changing its orientation.

If the position after the move is outside the lawn, then the mower do not move, it keeps its orientation and process the next command.
The cell directly at North of the position (x, y) has for coordinates (x, y+1).
An input file following these rules is given to program the mower:

..* The first line is the coordinates of the upper-right corner of the lawn, coordinates of
lower-left corner are supposed to be (0,0)
..* Next lines of the file drive all mowers. There are two lines for each mower:
..* First line give the initial position and orientation of the mower. Position and orientation are given by 2 numbers and a letter, separated by a space
..* Second line is a sequence of instruction driving the mower across the lawn. Instructions are a sequence of letters without space.

Each mower moves sequentially, it means that the second mower moves only after the first one execute all its instructions.
When the mower has executed all its instructions, it outputs its position and orientation.

GOAL
Design and write a program implementing the above specifications and validating the following test.

TEST
This file is given in input: 
```
5 5
1 2 N
LFLFLFLFF
3 3 E
FFRFFRFRRF
```

This output is expected (final positions of mowers): 
```
1 3 N
5 1 E
```


# Installation

Note: This code was etsted using `Python 3.7`

First you need to create a python3 virtual environement and activate it
```
$ virtualenv -p python3 venv
$ source ./venv/bin/activate
```

Then install all needed dependencies
```
$ pip install -r requirements.txt
```

# Running tests

To run units t`sts, just go at root of the repo and run
Use option `-v` to get a vcerbose result
```
$ pytest src 
```

# Usage

Before running the programm, you should put your input instructions in the file called `input.txt` (at the root of the repo)
Example:
```
5 5
1 2 N
LFLFLFLFF
3 3 E
FFRFFRFRRF
```
To run the programm as required by th eexercise you can run
```
$ python src/main.py
```

To add logs and see what all steps executed by mowers run
```
$ python src/main.py --logs
```

There is also a GUI interface that required PyQt5 to work but it's a nice to have sometimes
```
$ python src/main.py --gui
```

And to start the simulation you just have to press the start button. 
Obviously, the exit button will quit the programm.


![Alt text](gui.png?raw=true "GUI Screenshot")