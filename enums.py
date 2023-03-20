from enum import Enum

class Color(Enum):
    BLACK = 0
    RED = 1
    BLUE = 2
    GREEN = 3

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class ActionType(Enum):
    GO = 0
    PICK = 1
    DIG = 2
    DROP = 3
    SKIP = 4
    READ = 5
    CREATE = 6
    PROPOSE = 7
    ACCEPT = 8

class Square(Enum):
    EMPTY = 0
    BASE = 1
    SHARP = 2
    STRONG = 3
    FAST = 4
    GLASSES = 5
    GLOVES = 6
    BOOTS = 7
    GOLD = 8
    WATER = 9
    TREE = 10
    STONE = 11
    SCROLL = 12
    UNKNOWN = 13

class AgentType(Enum):
    DRUID = -1
    SHARP = Square.SHARP
    STRONG = Square.STRONG
    FAST = Square.FAST