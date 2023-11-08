import pygame as pg  # Import pygame library
from random import choice

pg.init()
win = pg.display.set_mode((350, 600))   # Initialize screen with width 350 and height 600
pg.display.set_caption("Snake Game")      # Set game title


pos = [100, 50]                           # Initial position of snake is (100,50)
pg_color = {'white': pg.Color('White'), 'red': pg.Color('Red')}        # Create a dictionary to represent different colors
fruit = False                                # Flag for presence of fruit
fruitPosX = None                              # Initialize the coordinates for the fruit as empty values
fruitPosY = None
clock = pg.time.Clock()                # Initialize clock object to control game speed
snakeSpeed = 10                            # Initial snake moving speed is set at 10 pixels per second


def draw_snake():                           # Draw a rectangle at the specified position
    rect = pg.Rect(pos[0], pos[1], 20, 10)       # Define a rectangle using given coordinates of snake. (xCoordinate, yCoordinate, width, height)
    pg.draw.rect(win, pg_color['white'], rect)    # Draw the rectangle on screen in color white defined earlier

def draw_fruit(xPos: int = None, yPos: int = None):             # Take arguments to define fruit's position if given
    if xPos != None and yPos != None :                            # If these values are not null or empty, execute following code.
        rad=10                      # Fruit has a fixed radius of 10 pixels. Define this here so it can be used in any function that uses draw_fruit() without passing arguments.
        posX = xPos - rad/2           # Calculate the center point of fruit's position with respect to its coordinates and half of its radius
        posY = yPos - rad/2           # Similarly, calculate its vertical coordinate

        draw_circle_filled(win, pg_color['red'], (posX, posY), rad)   # Draw a filled circle with color 'red' on screen at position determined above; with radius of 10 pixels as stored in variable rad.
        
        
def event_handler():                   # Create function named 'event_handler' to handle user inputs and game logic.
    global fruit, pos            # Declare 'fruit', 'pos' as globals to access their values in this function too without redeclaring them again.

    for evt in pg.event.get():       # Loop through each event occurred since last frame (game loop). Use PyGame's built-in get() method for extracting all events from its queue and store it in an iterable called 'evt'.
        if evt.type == pg.QUIT:     # If event type matches the constant defined by 'pg' module for closure of window, then close the game i.e., stop the loop forever using "running = False".
            running = False

        elif evt.type == pg.KEYDOWN:       # If user pressed a key, we check if it was ESC to exit the game or otherwise we change direction accordingly depending on which arrow key has been pressed.
            if (evt.key != pg.K_ESCAPE):   # Ignore escap key here and handle arrow keys only for snake movement.
                changeDirection(evt.key)      # Call a function named "changeDirection" with the pressed key as its argument to update direction variable accordingly. It will also prevent the movement of other directions until this event is over, meaning you don't start moving in another direction while a previous move was already made.