*This project has been created as part of the 42 curriculum by bgix, cschwart*

# A_MAZE_ING

## Description

    In this project we are required to generate custom maze, and output them in a output file.
    The maze must be displayed on a custom interface, in our case we selected MLX.

### Required
 - We can be able to show or hide the path from then entry to exit from the display.
 - The maze display must be able to change color.
 - The maze must be able to be re-generated from the display.
 - The 42 icon must be displayed within the maze if the maze's size allows it.

### Output file
- Must contain in hexa decimal the maze with [hight] lines and [width] characters.
- The block representing the maze must be followed by a new line.
- The entry and exit must be shown, a new line separeting the two.
- And the end the path to the exit must be displayed

### Reusability
- The entire project must be compiled into a downloadable of our choice (.whl for us)
- The project must be able to be downloaded and used from this file.

### Configurations
- The projects must get its settings from the config.txt file.
- Six settings are mendatory in this folder: Width, Height, Perfect, Output_file, Entry and exit.

## Instruction

### Makefile

#### make install
    Starts a venv and download all dependencies needed for the projects to works correctly.

#### make run
    Runs the projects fron the venv, it is required to use this for MLX to work due to the nature of these computers restricting access to some modules.

#### make lint
    Runs flake8 and mypy with a series of flags to make sure our projects follows the classic norms of python and readability.

#### make lint-strict
    Same as above but this time, mypy uses --strict to not allow any kind of norm mistakes.

#### make clean
    Cleans the workspace from any cache or unwanted 

## Resources

### bgix:
    MLX: Students.
    Algo: Several sources online.
    Algo to draw line: Online searches and youtube videos for explainations.

    AI Uses:
        None

### cschwart:
    AI Uses:
        ???

## Config Format
    The config must be in this format:
    KEY=VALUE

    # put the following text in comment.
    Spaces are allowed: SIZE=0                   ,1 #it works

    These following keys are mendatory and the program will not execute if they are not correct or present:
    HEIGHT Define the height of the maze
    WIDTH Define the width of the maze
    ENTRY Define the starting point of the maze
    EXIT Define the exit point of the maze
    PERFECT Define if the maze is perfect or not
    OUTPUT_FILE Define the name of the output file

## Algorithm
    The algoritm used was the backtrack_recursive algorythim
    
    It moves from cells to cells until it is blocked and can no longer move into an other cell (exluding the one the head come froms).
    In wich case it will go backward until it find a cells that has not been checked and will continue its path from it.
    Once it moved into every cell it means the maze is completed.

    The only difference from perfect and not perfect is that if it reach a cul-de-sac, it will break down the wall in front of where it comes from if it iss not a border.

### Why ?
    Because this one is pretty interesting to do but also satisfying to watch as the maze generate on the screen
    The most interesting to do was to addapt it to play steps by steps using generators.

## Reusability
    The code can be reused and addapted, the Vector2 class made it easy to addapt to other module or to edit.

## project management
    The project was mostly handled by bgix, as he is used to work on project 