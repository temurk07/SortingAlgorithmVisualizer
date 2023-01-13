import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    #Stores the 3 colors of grey
    GRADIENTS = [(128,128,128), (160, 160, 160), (192, 192, 192)]

    # Pygame needs a font to draw text on the window
    FONT = pygame.font.SysFont('ariel', 30)
    LARGE_FONT = pygame.font.SysFont('ariel', 40)

    SIDE_PADDING = 100
    TOP_PADDING = 150


    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visualization of sorting algorithm")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        #Determine the size (width and height) of each bar
            #Must be rounded as we can't draw fractional amounts
        self.block_width = round((self.width - self.SIDE_PADDING) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PADDING) / (self.max_val - self.min_val))

        self.start_x = self.SIDE_PADDING // 2

        # Pygame coordinate system is 0,0 at the top left corner

# We will redraw the entire canvas every frame
    #Note that we have a different method for drawing the bars
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # "1" parameter sets antialiasing to true
    controls = draw_info.FONT.render(" R - Reset | SPACE - Start sort | A - Ascedning | D - Descending", 1, draw_info.BLACK)
    # Draws the text onto the window in the center
        # y is set to 5 from the top of screen
        # we need to calculate the dead center of the x axis
    draw_info.window.blit(controls, ((draw_info.width/2 - controls.get_width()/2) ,5))

    sorting = draw_info.FONT.render(" I - Insertion Sort | B - Bubble Sort ", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, ((draw_info.width / 2 - controls.get_width() / 2), 40))

    draw_bar(draw_info)
    pygame.display.update()

# We have to:
    #Look at every single element in the list
    #Calculate its x and y coordinate
    #Calculate the width and height
    #Draw every bar/rectangle to be a slightly different color

# color positions is a dictionary, we will pass in a dictionary of indices that correspond to the color
# clear_bg is set to true ==> we only redraw the bars and override the port
    # We don't want to render the static text with the controls each frame
    # We only want to draw the bars
def draw_bar(draw_info, color_positions= {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg == True:
        clear_rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING,
                      draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        #Starting point for drawing each bar is its top left corner
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        # The mapping of dictionary of indices to a color
        if i in color_positions:
            color = color_positions[i]


        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width ,draw_info.height))

    if clear_bg == True:
        pygame.display.update()


#Generate a random height of bar as the data set we will work on
def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        #Generate a single vale between the min and max
        val = random.randint(min_val, max_val)

        #Append the single value to the array
        lst.append(val)

    return lst

#Default order is set to ascending
# Yeild makes this function a generator function,
    #The first time the function is called it will return a generator instead of calling teh actual function
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending == True) or (num1 < num2 and ascending == False):
                #Swap the elements in lst if num1 is bigger than num2
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                # Redraw the entire list, AND color the 2 bars being swapped into red and green
                draw_bar(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)

                # Yeild is set to true to call the function after each swap
                    # Yield is generator, and will pause and store the current state of the function
                    # allowing you to yield the run of theoverall program to another function
                    # Yield will also allow you to store the state of the function from the point from which it yeilded last time
                yield True
    return lst


#Main driver code
    # Renders the window
    # Sets up a game loop
    # Draws the list onto the screen
def main():
    run = True
    clock = pygame.time.Clock()
    #Clock regulates how quickly the loop will run

    n = 50
    min_val = 0
    max_val = 100

    # Instantiate the draw information class
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)


    sorting = False
    ascending = True

    #Stores the type of sorting algorithm we are currently using
        # Simply put the name of the sorting algorithm in the below variable after defining a new sorting algorithm as a function
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"

    #Stores the generator object that is created when you call you sorting algorithm function
    sorting_algorithm_generator = None

    while run:
        # Maximum of  60 frames per second
        clock.tick(60)

        # Keep calling sort until we are done
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)


        #Handles the events
            #pygame.event.get() returns the list of events that occured
            #since the last game loop
        for event in pygame.event.get():
            # Exit when clicking red X
            if event.type == pygame.QUIT:
                run = False

            # Keep running the loop when nothing is being pressed
            if event.type != pygame.KEYDOWN:
                continue

            #When you press r: reset the list
            if event.key == pygame.K_r:
                # Draw info stores the list so we need to reset it in the
                # draw info class
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)

                #If we reset the bars, we also need to reset sorting to False
                sorting = False

            #When you press the SPACE key: start the sorting algorithm
                # "and" portion is added to make sure we are can't sort if we are already sorting
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True

                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            #When you press A: ascending
                # "and" portion is added to make sure we can't switch in the middle of sorting
            elif event.key == pygame.K_a and not sorting:
                ascending = True

            # When you press D: descending
            elif event.key == pyagem.K_d and sorting == False:
                ascending = False



    pygame.quit()

if __name__ == "__main__":
    main()

