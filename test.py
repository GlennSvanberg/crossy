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
        
    def _check_boundaries(self, word: Word) -> None:
        """Verify if the word fits within the grid boundaries."""
        for curr_x, curr_y in self._get_word_coordinates(word):
            if not (0 <= curr_x < self.width and 0 <= curr_y < self.height):
                raise ValueError(f"Word '{word.word}' extends beyond grid boundaries")

    def _check_letter_conflicts(self, word: Word) -> None:
        """Check for letter conflicts with existing words."""
        for i, letter in enumerate(word.word):
            curr_x, curr_y = self._get_coordinate_at_index(word, i)
            
            for existing_word in self.words:
                for j, existing_letter in enumerate(existing_word.word):
                    check_x, check_y = self._get_coordinate_at_index(existing_word, j)
                    
                    if curr_x == check_x and curr_y == check_y:
                        if letter != existing_letter:
                            raise ValueError(
                                f"Letter conflict at position ({curr_x}, {curr_y}): "
                                f"'{letter}' vs '{existing_letter}'"
                            )

    def _get_coordinate_at_index(self, word: Word, index: int) -> tuple[int, int]:
        """Get the (x, y) coordinate for a letter at the given index in the word."""
        if word.direction == Direction.ACROSS:
            return word.pos_x + index, word.pos_y
        return word.pos_x, word.pos_y + index

    def _get_word_coordinates(self, word: Word) -> list[tuple[int, int]]:
        """Get all coordinates that a word occupies."""
        return [self._get_coordinate_at_index(word, i) for i in range(len(word.word))]

    def add_word(self, word: Word):
        """Add a word to the crossword after validating position and conflicts."""
        self._check_boundaries(word)
        self._check_letter_conflicts(word)
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
    
        


