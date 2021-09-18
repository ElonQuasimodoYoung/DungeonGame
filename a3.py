"""
CSSE1001 Assignment 3
Semester 2, 2020
"""

# Fill these in with your details
__author__ = "{{Donghao Yang}} ({{45930032}})"
__email__ = "donghao.yang@uqconnect.edu.au"
__date__ = "10/25/2020"

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

TASK_ONE = 1
TASK_TWO = 2

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}

DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1),
    "w": (-1, 0),
    "s": (1, 0),
    "d": (0, 1),
    "a": (0, -1)
}

INVALID = "That's invalid."
WIN_TEXT = "You have won the game with your strength and honour!"
LOSE_TEXT = "You have lost all your strength and honour."


class Entity:
    """A generic Entity within the game.

    """
    _id = "Entity"

    def __init__(self):
        """
        Something the player can interact with
        """
        self.valid = True
        self.name = ''
        self._collidable = True
        self.img, self.tk_img = None, None

    def get_id(self):
        """Returns a string that represents the Entity’s ID.

        """
        return self._id

    def set_collide(self, collidable):
        """ Set the collision state for the Entity to be True.

        """
        self._collidable = collidable

    def can_collide(self):
        """Returns True if the Entity can be collided with (another
            Entity can share the position that this one is in)
            and False otherwise.

        """
        return self._collidable

    def __str__(self):
        """Returns the string representation of the Entity.

        """
        return f"{self.__class__.__name__}({self._id!r})"

    def __repr__(self):
        """Same as str(self)

        """
        return str(self)

    def img_path(self):
        raise NotImplementedError

    def get_img(self, size):
        """ get the image

        """
        if self.img is None:
            self.img = Image.open(self.img_path())
            self.img = self.img.resize(size, Image.ANTIALIAS)
            self.tk_img = ImageTk.PhotoImage(self.img)
        return self.tk_img


class Wall(Entity):
    """A Wall is a special type of an Entity within the game.

    """

    _id = WALL
    
    def __init__(self):
        """Constructor of the Wall class.

        """
        super().__init__()
        self.name = ''
        self.set_collide(False)

    def get_color(self):
        """get the color of wall

        """
        return 'gray65'

    def img_path(self):
        """the path for importing the image

        """
        return 'images/wall.png'


class Item(Entity):
    """An Item is a special type of an Entity within the game.
        This is an abstract class.

    """
    def on_hit(self, game):
        """This function should raise the NotImplementedError.

        """
        raise NotImplementedError


class Key(Item):
    """ A Key is a special type of Item within the game.

    """

    _id = KEY

    def __init__(self):
        """Constructor of the Key class.

        """
        super().__init__()
        self.name = 'Trash'

    def on_hit(self, game):
        """When the player takes the Key the Key should be added to the Player's
            inventory.The Key should then be removed from the dungeon once it's
            in the Player's inventory

        """
        if self.valid:
            player = game.get_player()
            player.add_item(self)
            game.get_game_information().pop(player.get_position())
            self.valid = False

    def get_color(self):
        """get the color of key

        """
        return 'yellow'

    def img_path(self):
        """the path for importing key image

        """
        return 'images/key.png'


class MoveIncrease(Item):
    """MoveIncrease is a special type of Item within the game.

    """

    _id = MOVE_INCREASE

    def __init__(self, moves=5):
        """Constructor of the MoveIncrease class.

        """
        super().__init__()
        self._moves = moves
        self.name = 'Banana'

    def on_hit(self, game):
        """When the player hits the MoveIncrease item the number of moves for
            the player increases and the M item is removed from the game

        """
        if self.valid:
            player = game.get_player()
            player.change_move_count(self._moves)
            game.get_game_information().pop(player.get_position())
            self.valid = False

    def get_color(self):
        """get the color of move_increase

        """
        return 'orange'

    def img_path(self):
        """the path for importing move_increase image

        """
        return 'images/moveIncrease.png'


class Door(Entity):
    """A Door is a special type of an Entity within the game.

    """
    _id = DOOR

    def __init__(self):
        """Constructor of the Door class.

        """
        super().__init__()
        self.name = 'Nest'

    def on_hit(self, game):
        """If the Player's inventory contains a Key Entity then this method
            should set the 'game over' state to be True

        """
        player = game.get_player()
        for item in player.get_inventory():
            if item.get_id() == KEY:
                game.set_win(True)
                return
        print("You don't have the key!")

    def get_color(self):
        """get the color of door

        """
        return 'red'

    def img_path(self):
        """the path for importing door image

        """
        return 'images/door.png'


class Player(Entity):
    """A Player is a special type of an Entity within the game.

    """

    _id = PLAYER

    def __init__(self, move_count):
        """Constructor of the Player class

        """
        super().__init__()
        self._move_count = move_count
        self._inventory = []
        self._position = None
        self.name = 'Ibis'

    def set_position(self, position):
        """Sets the position of the player

        """
        self._position = position

    def get_position(self):
        """Returns a tuple of ints representing the position
           of the Player. If the Player’s position hasn’t
           been set yet then this method should return None.

        """
        return self._position

    def change_move_count(self, number):
        """
        Parameters:
            number (int): number to be added to move count
        """
        self._move_count += number

    def moves_remaining(self):
        """number to be added to the Player's move count.

        """
        return self._move_count

    def add_item(self, item):
        """Adds item (Item) to inventory

        """
        self._inventory.append(item)

    def get_inventory(self):
        """Returns a list that represents the Player’s
           inventory. If the Player has nothing in their
           inventory then an empty list should be returned.

        """
        return self._inventory

    def get_color(self):
        """get the color of player

        """
        return 'SpringGreen2'

    def img_path(self):
        """the path for importing player image"""
        return 'images/player.png'


def load_game(filename, load):
    """Create a 2D array of string representing the dungeon to display.
    
    Parameters:
        filename (str): A string representing the name of the level.

    Returns:
        (list<list<str>>): A 2D array of strings representing the 
            dungeon.
    """
    dungeon_layout = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            dungeon_layout.append(list(line))
    if not load:
        return dungeon_layout
    else:
        n = int(''.join(dungeon_layout[0]))
        return dungeon_layout[1:], Player(n)


class GameLogic:
    """ GameLogic contains all the game information and how
        the game should play out

    """
    def __init__(self, dungeon_name="game2.txt", load=False):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level

        """
        if not load:
            self._dungeon = load_game(dungeon_name, load)
            self._player = Player(GAME_LEVELS[dungeon_name])        
        else:
            self._dungeon, self._player = load_game(dungeon_name, load)
        self._dungeon_size = len(self._dungeon)
        self._game_information = self.init_game_information()
        self._win = False

    def get_positions(self, entity):
        """Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.

        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row, col))

        return positions

    def init_game_information(self):
        """This method should return a dictionary containing the position and
        the corresponding Entity as the keys and values respectively.

        """
        player_pos = self.get_positions(PLAYER)[0]
        key_position = self.get_positions(KEY)[0]
        door_position = self.get_positions(DOOR)[0]
        wall_positions = self.get_positions(WALL)
        move_increase_positions = self.get_positions(MOVE_INCREASE)
        
        self._player.set_position(player_pos)

        information = {
            key_position: Key(),
            door_position: Door(),
        }

        for wall in wall_positions:
            information[wall] = Wall()

        for move_increase in move_increase_positions:
            information[move_increase] = MoveIncrease()

        return information

    def get_player(self):
        """This method returns the Player object within the game

        """
        return self._player

    def get_entity(self, position):
        """Returns an Entity at a given position in the dungeon.Entity in the
            given direction or if the position is off map then this function
            should return None

        """
        return self._game_information.get(position)

    def get_entity_in_direction(self, direction):
        """Returns an Entity at a given direction of the Player's position.
            If there is no Entity in the given direction or if the direction is
            off map then this function should return None.

        """
        new_position = self.new_position(direction)
        return self.get_entity(new_position)

    def get_game_information(self, player=False):
        """Returns a dictionary containing the position and the corresponding
            Entity, as the keys and values, for the current dungeon

        """
        ret = self._game_information.copy()
        if player:
            ret[self._player.get_position()] = self._player
        return ret

    def get_dungeon_size(self):
        """Returns the width of the dungeon as an integer.

        """
        return self._dungeon_size

    def move_player(self, direction):
        """ Update the Player's position to place them one position in the given
             direction

        """
        new_pos = self.new_position(direction)
        self.get_player().set_position(new_pos)

    def collision_check(self, direction):
        """
        Check to see if a player can travel in a given direction
        Parameters:
            direction (str): a direction for the player to travel in.

        Returns:
            (bool): False if the player can travel in that direction without colliding otherwise True.
        """
        new_pos = self.new_position(direction)
        entity = self.get_entity(new_pos)
        if entity is not None and not entity.can_collide():
            return True
        
        return not (0 <= new_pos[0] < self._dungeon_size and 0 <= new_pos[1] < self._dungeon_size)

    def new_position(self, direction):
        """Returns a tuple of integers that represents the new position given
            the direction

        """
        x, y = self.get_player().get_position()
        dx, dy = DIRECTIONS[direction]
        return x + dx, y + dy

    def check_game_over(self):
        """Return True if the game has been lost and False otherwise.

        """
        return self.get_player().moves_remaining() <= 0

    def set_win(self, win):
        """Set the game's win state to be True or False.

        """
        self._win = win

    def won(self):
        """Return game's win state

        """
        return self._win

    def save_game(self, filename):
        """save the game

        """
        info = self.get_game_information(player=True)
        with open(filename, 'w') as f:
            f.write(f'{self._player.moves_remaining()}\n')
            for i in range(self._dungeon_size):
                for j in range(self._dungeon_size):
                    if (i, j) in info:
                        f.write(info[(i, j)]._id)
                    else:
                        f.write(' ')
                f.write('\n')


class AbstractGrid(tk.Canvas):
    """abstract class for grid layouts 

    """
    def __init__(self, master, rows, cols, width, height, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.size = width, height
        self.gripos = rows, cols
        self.gsize = int(width / cols), int(height / rows)


class DungeonMap(AbstractGrid):
    """dungeon map layouts

    """
    def __init__(self, master, size, width, **kwargs):
        super().__init__(master, rows=size, cols=size, width=width, height=width, **kwargs)
        self.pack()

    def paint(self, gamedata, task):
        """print the layout based on game data

        """
        print('paint')
        self.create_rectangle(0, 0, self.size[0], self.size[1], fill='gray80')
        
        for loc, obj in gamedata.items():
            if obj.valid:
                self.create_rectangle(loc[1] * self.gsize[0],
                                    loc[0] * self.gsize[1],
                                    (loc[1] + 1) * self.gsize[0],
                                    (loc[0] + 1) * self.gsize[1],
                                    fill=obj.get_color())
                self.create_text(((loc[1] + 0.5) * self.gsize[0], (loc[0] + 0.5) * self.gsize[1]), text=f'{obj.name}')


class AdvancedDungeonMap(DungeonMap):
    """dungeon map layouts of task 2

    """
    def __init__(self, master, size, width, **kwargs):
        super().__init__(master, size, width, **kwargs)
        self.img = Image.open('images/empty.png')
        self.img = self.img.resize((self.gsize[0], self.gsize[1]), Image.ANTIALIAS)
        self.tk_img = ImageTk.PhotoImage(self.img)

    def paint(self, gamedata, task):
        """the layout based on game data using images instead of pure color

        """
        print('paint')
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.create_image((j * self.gsize[1], i * self.gsize[0]), image=self.tk_img)
        
        for loc, obj in gamedata.items():
            if obj.valid:
                self.create_image(((loc[1] + 0.5) * self.gsize[0], (loc[0] + 0.5) * self.gsize[1]), image=obj.get_img((self.gsize[0], self.gsize[1])))


class KeyPad(AbstractGrid):
    """the key pad

    """
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, rows=2, cols=3, width=width, height=height, **kwargs)

    def paint(self):
        """the key pad on the right of the screen
            in forms of 3 by 2 array with two empty box

        """
        loc = [(0,1), (1,0), (1,1), (1,2)]
        text = ['N', 'W', 'S', 'E']
        for l, s in zip(loc, text):
            self.create_rectangle(l[1] * self.gsize[0],
                                  l[0] * self.gsize[1],
                                  (l[1] + 1) * self.gsize[0],
                                  (l[0] + 1) * self.gsize[1],
                                  fill='gray65')
            self.create_text((l[1] + 0.5) * self.gsize[0],
                             (l[0] + 0.5) * self.gsize[1],
                             text=s)
        self.pack()

class StatusBar(tk.Frame):
    """class for status bar

    """
    def __init__(self, root, game):
        super().__init__(master=root)
        self.pack(fill=tk.X, expand=True)
        self.game = game
        self.status_bar = tk.Canvas(master=self, width=800, height=100)
        self.status_bar.pack()
        self.btn_ng = tk.Button(text='New Game', command=game.new_game, anchor=tk.W)
        self.btn_ng_window = self.status_bar.create_window(140, 10, anchor=tk.NW, window=self.btn_ng)
        self.btn_q = tk.Button(text='Quit', command=game._display.quit, anchor=tk.W)
        self.btn_q_window = self.status_bar.create_window(160, 50, anchor=tk.NW, window=self.btn_q)
        import time
        self.start = time.time()
        self.img_clock = Image.open('images/clock.gif')
        self.img_clock = self.img_clock.resize((50, 70), Image.ANTIALIAS)
        self.tk_img_clock = ImageTk.PhotoImage(self.img_clock)
        self.img_life = Image.open('images/lightning.png')
        self.img_life = self.img_life.resize((50, 70), Image.ANTIALIAS)
        self.tk_img_life = ImageTk.PhotoImage(self.img_life)

    def paint(self):
        """the necessary componets os status bar

        """
        import time
        delta = time.time() - self.start
        self.status_bar.create_rectangle(320, 30, 430, 70, outline=self.game._display.cget('bg'), fill=self.game._display.cget('bg'))
        self.status_bar.create_image((300, 50), image=self.tk_img_clock)
        self.status_bar.create_text((370, 50), text=f'Time elapsed\n{int(delta) // 60}m{int(delta) % 60}s')
        self.status_bar.create_image((550, 50), image=self.tk_img_life)
        self.status_bar.create_rectangle(570, 30, 700, 70, outline=self.game._display.cget('bg'), fill=self.game._display.cget('bg'))
        self.status_bar.create_text((640, 50), text=f'Moves left\n{self.game._game._player.moves_remaining()} moves remaining')


class GameApp:
    """The game application class combine and control everything

    """
    def __init__(self, task=TASK_ONE):
        self.finished = False
        self.task = task
        self._display = tk.Tk()
  
        self.menu = tk.Menu(self._display)
        self.menu.add_command(label='Save Game', command=self.save_game)
        self.menu.add_command(label='Load Game', command=self.load_game)
        self.menu.add_command(label='New Game', command=self.new_game)
        self.menu.add_command(label='Quit', command=self._display.quit)
        self._display.config(menu=self.menu)

        self._game = GameLogic()
        import time
        self.start = time.time()

        self.top = tk.Frame(master=self._display)
        self.top.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.mid = tk.Frame(master=self._display)
        self.mid.pack(fill=tk.X, expand=True)

        label = tk.Label(self.top, text='Key Cave Adventure Game', background='spring green', font=("Helvetica", 24))
        label.pack(fill=tk.X, expand=True)

        if task == TASK_ONE:
            self.view = DungeonMap(master=self.mid, size=self._game._dungeon_size, width=600)
        else:
            self.view = AdvancedDungeonMap(master=self.mid, size=self._game._dungeon_size, width=600)
        self.view.pack(side=tk.LEFT, expand=True)
        self.keymap = KeyPad(master=self.mid, width=200, height=100)
        self.keymap.pack(side=tk.RIGHT)
        self.keymap.bind('<Button-1>', self.clicked)

        self._display.bind('<w>', self.keyPressed)
        self._display.bind('<a>', self.keyPressed)
        self._display.bind('<s>', self.keyPressed)
        self._display.bind('<d>', self.keyPressed)

        self.bot = StatusBar(self._display, self)

        self.paint()
        self._display.mainloop()

    def save_game(self):
        """Save the game into a file, the file name
            is taken in though message box
        """
        filename = filedialog.askopenfilename(parent=self._display,
                                           initialdir='.',
                                           title="Please select a folder:")
        self._game.save_game(filename)
        self.paint()

    def load_game(self):
        """Load the game from a file, the file name
            is taken in though message box

        """
        filename = filedialog.askopenfilename(parent=self._display,
                                           initialdir='.',
                                           title="Please select a folder:")
        self._game = GameLogic(filename, True)
        self.finished = False
        self.paint()
        import time
        self.start = time.time()

    def new_game(self):
        """Reinitialize the game logic object to restart a new game

        """
        self._game = GameLogic()
        self.finished = False
        self.paint()
        import time
        self.start = time.time()

    def clicked(self, event):
        """This is used for clicking on the wasd gui control panel

        """
        if not self.finished:
            j, i = int(event.x // self.keymap.gsize[0]), int(event.y // self.keymap.gsize[0])
            if i == 0 and j == 1:
                self.play('w')
            elif i == 1:
                if j == 0:
                    self.play('a')
                elif j == 1:
                    self.play('s')
                elif j == 2:
                    self.play('d')
            self.paint()

    def keyPressed(self, event):
        """This is used for key pressed event

        """
        if not self.finished:
            self.play(event.char)
            self.paint()

    def play(self, action):
        """ The main game logic, this is modified from assignment 2 solution

        """
        player = self._game.get_player()
        if action in DIRECTIONS:
            direction = action
            # if player does not collide move them
            if not self._game.collision_check(direction):
                self._game.move_player(direction)
                entity = self._game.get_entity(player.get_position())

                # process on_hit and check win state
                if entity is not None:
                    entity.on_hit(self._game)
                    if self._game.won():
                        import time
                        msg = messagebox.askquestion('Win',
                                                     f'Your score is {int(time.time() - self.start)}\nDo you want to play again?')
                        self.finished = True
                        if msg == 'yes':
                            self.new_game()
            else:
                print(INVALID)

            player.change_move_count(-1)

        else:
            print(INVALID)

        if self._game.check_game_over():
            msg = messagebox.askquestion('Loss',
                                         f'You lost\nDo you want to play again?')
            self.finished = True
            if msg == 'yes':
                self.new_game()

    def paint(self):
        """get the gui window

        """
        game_information = self._game.get_game_information(player=True)
        self.view.paint(game_information, self.task)
        self.keymap.paint()
        self.bot.paint()


def main():
    app = GameApp()

main()
