class Direction:
    ACROSS = "across"
    DOWN = "down"

class Word:
    def __init__(self, word: str, pos_x: int, pos_y: int, direction: Direction):
        
        self.word = word.upper()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = direction
        
class Cell:
    def __init__(self, pos_x: int, pos_y: int, letter: str, number: int, is_black: bool):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.letter = letter
        self.number = number
        self.is_black = is_black
        
class Crossword:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.words = []
        
    def add_word(self, word: Word):
        # Check if word fits within grid boundaries
        x, y = word.pos_x, word.pos_y
        for i, letter in enumerate(word.word):
            if word.direction == Direction.ACROSS:
                curr_x, curr_y = x + i, y
            else:  # Direction.DOWN
                curr_x, curr_y = x, y + i
                
            # Check boundaries
            if not (0 <= curr_x < self.width and 0 <= curr_y < self.height):
                raise ValueError(f"Word '{word.word}' extends beyond grid boundaries")
            
            # Check for letter conflicts
            for existing_word in self.words:
                ex_x, ex_y = existing_word.pos_x, existing_word.pos_y
                for j, existing_letter in enumerate(existing_word.word):
                    if existing_word.direction == Direction.ACROSS:
                        check_x, check_y = ex_x + j, ex_y
                    else:  # Direction.DOWN
                        check_x, check_y = ex_x, ex_y + j
                        
                    if curr_x == check_x and curr_y == check_y:
                        if letter != existing_letter:
                            raise ValueError(
                                f"Letter conflict at position ({curr_x}, {curr_y}): "
                                f"'{letter}' vs '{existing_letter}'"
                            )
        
        self.words.append(word)
        
    def print_crossword(self):
        # Initialize empty grid with spaces
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place words in the grid
        for word in self.words:
            x, y = word.pos_x, word.pos_y
            for letter in word.word:
                if 0 <= x < self.width and 0 <= y < self.height:
                    grid[y][x] = letter
                    if word.direction == Direction.ACROSS:
                        x += 1
                    else:  # Direction.DOWN
                        y += 1
        
        # Print x coordinates on top
        print('   ', end='')
        for x in range(self.width):
            print(f'{x:2}', end='')
        print()
        
        # Print top border
        print('  ' + '-' * (self.width * 2 + 1))
        
        # Print grid with y coordinates
        for y, row in enumerate(grid):
            print(f'{y:2}|', end=' ')
            for cell in row:
                print(cell, end=' ')
            print('|')
        
        # Print bottom border
        print('  ' + '-' * (self.width * 2 + 1))

def create_crossword():
    print("Creating crossword")
    crossword = Crossword(10, 10)
    crossword.add_word(Word(word="Strawberry", direction=Direction.ACROSS, pos_x=0, pos_y=0))
    crossword.add_word(Word(word="Bananas", direction=Direction.DOWN, pos_x=5, pos_y=0))
    crossword.add_word(Word(word="Raw", direction=Direction.DOWN, pos_x=7, pos_y=0))
    crossword.add_word(Word(word="New", direction=Direction.ACROSS, pos_x=5, pos_y=2))
    
    crossword.print_crossword()

if __name__ == "__main__":
    create_crossword()
    
        


