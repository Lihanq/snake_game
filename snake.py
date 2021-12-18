from designer import *
from random import randint

SNAKE_SPEED = 2
World = {
    """
    a dictionary to keep track of the snake game elements, which includes
    
    head: a DesignerObject to represent the head of a snake, 
    speed: a int controls the moving speed of snake, 
    direction: a str representing the direction that snake moving towards, 
    apple: a DesignerObject that keeps track of apple, 
    segments: a list of DesignerObject storing body segments of a snake, 
    game_over_panel: a DesignerObject that print "GAME OVER!" when the game is over
    score: a int that keeps track of player score
    score_panel: a DesignerObject that prints player score on the window    
    """
    
    "head": DesignerObject,
    "speed": int,
    "direction": str,
    "apple": DesignerObject,
    "segments": [DesignerObject],
    "game_over_panel": DesignerObject,
    "score": int,
    "score_panel": DesignerObject
    }

def create_world() -> World:
    """
    function initializes values for keys in a World variable to start the snake game
    
    args: function takes no arguments
    
    return:
        a initialized World variable with starting setting of the snake game
    """
    return {
        "head": image("head.png"),
        "speed": SNAKE_SPEED,
        "direction": "right",
        "apple": create_apple(), 
        "segments": [],
        "game_over_panel": text("black", "", 20),
        "score": 0,
        "score_panel": text("black", "Score: 0", 15, get_width() / 2, 15)
        }

#################
# Control apple #
#################

def create_apple() -> DesignerObject:
    """
    function creates an apple at a random postion on the game window
    
    args: function takes no arguments
    
    return:
        a DesignerObject with a image of apple
    """
    return image("apple.png", randint(0 + 15, get_width() - 15), randint(0 + 15, get_height() - 15))
        
def teleport_apple(world):
    """
    function changes apple's current position to a distant position
    
    args:
        world(World): a variable keeps track of all elements of a game, including apple DesignerObject
        
    return: None
    """
    new_x = world["apple"]["x"] + randint(50, 300)
    new_y = world["apple"]["y"] + randint(50, 300)
    if new_x > get_width() - 15:
        new_x = new_x % (get_width() - 15)
        if new_x < 15:
            new_x += randint(15, 60)
    if new_y > get_height() - 15:
        new_y = new_y % (get_height() - 15)
        if new_y < 15:
            new_y += randint(15, 60)
    world["apple"]["x"] = new_x
    world["apple"]["y"] = new_y
        
#######################
# Colliding and Score #
#######################

def colliding_apple_head(world):
    """
    function add more snake body segments, and score add 1 if snake head collides with apple.
    
    args:
        world(World): a variable keeps track of all elements of a game, including apple and snake head DesignerObject
        
    return: None
    """
    if colliding(world["apple"], world["head"]):
        teleport_apple(world)
        add_segment(world)
        move_snake(world)
        count_score(world)

def count_score(world):
    """
    function add 1 to player score and update player view by updating text of score panel in world.
    
    args:
        world(World): a variable keeps track of all elements of a game, including score and score panel DesignerObject
        
    return: None
    """
    world["score"] += 1
    world["score_panel"]["text"] = "Score: " +  str(world["score"])
        
###################
# Segment control #
###################

def create_segment() -> DesignerObject:
    """
    function creates and returns one snake body segment DesignerObject
    
    args: function takes no argument
        
    return:
        DesignerObject: a snake body segment
    """
    return image("segment.png")

def add_segment(world):
    """
    function add 6 more snake body segments into world dictionary, segments key
    
    args:
        world(World): a variable keeps track of all elements of a game, including snake body segements
        
    return: None
    """
    i = 6
    while i > 0:
        i -= 1
        new_segment = create_segment()
        world["segments"].append(new_segment)
        
################################
# Snake direction and movement #
################################

# When changeing direction of one image, x, y, and angle needs to be changed

def move_snake(world:World):
    """
    function moves snake head to the newest position by adding 2 to either y coordinate or x coordinate
    accroding to current direction, and update snake first body segments to the previous head position and
    the rest of the body segments to the position of cooresponding preceding segments
    
    args:
        world(World): a variable keeps track of all elements of a game, including position of all snake elements
        
    return: None
    """
    update_first_segment(world)
    update_rest_segments(world)
    move_head(world)
    
def move_head(world):
    """
    function moves the head of snake at the speed of sepficied by the "speed" key in world
    
    args:
        world(World): variable keeps track of every element of snake game,
        including speed of snake movement and the position of snake head
        
    reutrn: None
    """
    if world["direction"] == "right":
        world["head"]['x'] += world["speed"]
    elif world["direction"] == "left":
        world["head"]["x"] -= world["speed"]
    elif world["direction"] == "up":
        world["head"]["y"] -= world["speed"]
    elif world["direction"] == "down":
        world["head"]["y"] += world["speed"]
    
        
def update_first_segment(world):
    """
    function updates the first snake body segment's postition and angle to the position and angle of snake head
    
    args:
        world(World): a variable keeps track of all elements of a game, including positions and angles of all snake elements
        
    return: None
    """
    if world["segments"]: 
        world["segments"][0]["x"] = world["head"]['x']
        world["segments"][0]["y"] = world["head"]['y']
        world["segments"][0]["angle"] = world["head"]['angle']
        adjust_position(world, world["head"], world["segments"][0])
    
def update_rest_segments(world):
    """
    funtion updates the positions and angles of a list of elements (only apply to the second or later items),
    which change one item's position and angle to the position and angle of its preceding item.
    
    args:
        world(World): a variable keeps track of all elements of a game, including position of all snake elements
        
    return: None
    """
    segments = world["segments"]
    item_num = len(segments)
    if item_num >= 2:
        i = -1
        while item_num > 1:
            segments[i]["x"] = segments[i - 1]["x"]
            segments[i]["y"] = segments[i - 1]["y"]
            segments[i]["angle"] = segments[i - 1]["angle"]
            item_num -= 1
            i -= 1   
            
def adjust_position(world: World, former: DesignerObject, later: DesignerObject):
    """
    function adjust the position of a element according to the position of another element.
    
    args:
        former(DesignerObject): the preceding element
        later(DesgnerObject): the element whose position will the adjusted accroding to the preceding element
        
    return: None
    """
    if later["angle"] == former["angle"]:
        if world["direction"] == "right":
            later["x"] = former["x"] - 14
        elif world["direction"] == "left":
            later["x"] = former["x"] + 14
        elif world["direction"] == "up":
            later["y"] = former["y"] + 14
        elif world["direction"] == "down":
            later["y"] = former["y"] - 14
            
def turn_right(world: World):
    """
    function changes the angle to make the snake head to head right according to the current value of the "direction" key of world
    
    args:
        world(World): a variable keeps track of all elements of a game,
        including the angle of snake head and the direction which snake head is heading
    
    return: None
    """
    if world["direction"] == "left":
        world["head"]["angle"] += 180
    elif world["direction"] == "up":
        world["head"]["angle"] -= 90
    elif world["direction"] == "down":
        world["head"]["angle"] += 90
 
def turn_left(world: World):
    """
    function changes the angle to make the snake head to head left according to the current value of the "direction" key of world
    
    args:
        world(World): a variable keeps track of all elements of a game,
        including the angle of snake head and the direction which snake head is heading
    
    return: None
    """
    if world["direction"] == "right":
        world["head"]["angle"] += 180
    elif world["direction"] == "up":
        world["head"]["angle"] += 90
    elif world["direction"] == "down":
        world["head"]["angle"] -= 90

def turn_up(world):
    """
    function changes the angle to make the snake head to head up according to the current value of the "direction" key of world
    
    args:
        world(World): a variable keeps track of all elements of a game,
        including the angle of snake head and the direction which snake head is heading
    
    return: None
    """
    if world["direction"] == "right":
        world["head"]["angle"] += 90
    elif world["direction"] == "left":
        world["head"]["angle"] -= 90
    elif world["direction"] == "down":
        world["head"]["angle"] += 180
    
def turn_down(world):
    """
    function changes the angle to make the snake head to head down according to the current value of the "direction" key of world
    
    args:
        world(World): a variable keeps track of all elements of a game,
        including the angle of snake head and the direction which snake head is heading
    
    return: None
    """
    if world["direction"] == "right":
        world["head"]["angle"] -= 90
    elif world["direction"] == "left":
        world["head"]["angle"] += 90
    elif world["direction"] == "up":
        world["head"]["angle"] += 180
        
def change_direction(world: World, key: str):
    """
    function changes the value of the "direction" key in the created World according to which key is pressed on keyboard
    
    args:
        world(World): a variable that keeps track of all elements of a game, including the direction which snake head is heading
        key(str): a variable to indicate which key is pressed on keyboard
        
    return: None
    """
    if key == "right":
        turn_right(world)
        world["direction"] = "right"
    elif key == "left":
        turn_left(world)
        world["direction"] = "left"
    elif key == "up":
        turn_up(world)
        world["direction"] = "up"
    elif key == "down":
        turn_down(world)
        world["direction"] = "down"

######################
# Game over criteria #
######################
def colliding_body_wall(world) -> bool:
    """
    function returns whether the snake head collides with any body segments or the edges of the drawing window
    
    args:
        world(World): a variable that keeps track of all elements of a game
        
    return:
        bool: a bool value indicate that the snake head collides with any body segments or the edges of the drawing window
    """
    collided = False
    if world["segments"]: 
        for i, segment in enumerate(world["segments"]):
            if i > 1:
                collided = collided or colliding(segment, world["head"])
    return collided or colliding_head_wall(world)

def colliding_head_wall(world) -> bool:
    """
    function returns whether snake head collides with any edge of the drawing window
    
    args:
        world(World): a variable that keeps track of all elements of a game
        
    return:
        bool: a bool value indicate snake head collides with any edge of the drawing window
    """
    colliding_left_right = world["head"]["x"] > (get_width() - 16) or world["head"]["x"] < 16
    colliding_up_down = world["head"]["y"] > (get_height() - 16) or world["head"]["y"] < 16
    return colliding_left_right or colliding_up_down

def game_over(world):
    """
    function informs player game is end by changing the text in the game over panel to "GAME OVER!"
    
    args:
        world(World): a variable that keeps track of all elements of a game, including the game over panel
        
    return: None
    """
    world["game_over_panel"]["text"] = "GAME OVER!"
        
when("starting", create_world)
when("updating", move_snake)
when("updating", colliding_apple_head)
when("updating", colliding_body_wall)
when("typing", change_direction)
when(colliding_body_wall, game_over, pause)

start()
    