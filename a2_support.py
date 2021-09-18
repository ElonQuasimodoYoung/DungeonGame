GAME_LEVELS = {
    # dungeon layout: max moves allowed
    "game1.txt": 7,
    "game2.txt": 12,
    "game3.txt": 19,
}

PLAYER = "O"
KEY = "K"
DOOR = "D"
WALL = "#"
MOVE_INCREASE = "M"
SPACE = " "

DIRECTIONS = {
    "W": (-1, 0),
    "S": (1, 0),
    "D": (0, 1),
    "A": (0, -1)
}

INVESTIGATE = "I"
QUIT = "Q"
HELP = "H"

VALID_ACTIONS = [INVESTIGATE, QUIT, HELP, *DIRECTIONS.keys()]

HELP_MESSAGE = f"Here is a list of valid actions: {VALID_ACTIONS}"

INVALID = "That's invalid."

WIN_TEXT = "You have won the game with your strength and honour!"

LOSE_TEST = "You have lost all your strength and honour."
LOSE_TEXT = "You have lost all your strength and honour."


class Display:
    """Display of the dungeon."""

    def __init__(self, game_information, dungeon_size):
        """Construct a view of the dungeon.

        Parameters:
            game_information (dict<tuple<int, int>: Entity): Dictionary 
                containing the position and the corresponding Entity
            dungeon_size (int): the width of the dungeon.
        """
        self._game_information = game_information
        self._dungeon_size = dungeon_size

    def display_game(self, player_pos):
        """Displays the dungeon.
        
        Parameters:
            player_pos (tuple<int, int>): The position of the Player
        """
        dungeon = ""

        for i in range(self._dungeon_size):
            rows = ""
            for j in range(self._dungeon_size):
                position = (i, j)
                entity = self._game_information.get(position)

                if entity is not None:
                    char = entity.get_id()
                elif position == player_pos:
                    char = PLAYER
                else:
                    char = SPACE
                rows += char
            if i < self._dungeon_size - 1:
                rows += "\n"
            dungeon += rows
        print(dungeon)

    def display_moves(self, moves):
        """Displays the number of moves the Player has left.
        
        Parameters:
            moves (int): THe number of moves the Player can preform. 
        """
        print(f"Moves left: {moves}\n")


def load_game(filename):
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

    return dungeon_layout
