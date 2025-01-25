import random
import reflex as rx
from enum import Enum
from .generate import LetterConstraint
class Direction(str, Enum):
    ACROSS = "across"
    DOWN = "down"

class Word(rx.Base):
    word: str
    pos_x: int
    pos_y: int
    direction: Direction
    clue: str
    
    def __init__(self, word: str, pos_x: int, pos_y: int, direction: Direction, clue: str = ""):
        super().__init__(
            word=word.upper(),
            pos_x=pos_x,
            pos_y=pos_y,
            direction=direction,
            clue=clue
        )

class Cell(rx.Base):
    pos_x: int
    pos_y: int 
    letter: str
    number: int
    is_black: bool
    
    def __init__(self, pos_x: int, pos_y: int, letter: str, number: int, is_black: bool):
        super().__init__(
            pos_x=pos_x,
            pos_y=pos_y,
            letter=letter,
            number=number,
            is_black=is_black
        )
    
class Crossword(rx.Base):
    width: int
    height: int
    words: list[Word]
    topic: str
    
    def __init__(self, width: int, height: int):
        super().__init__(
            width=width,
            height=height,
            words=[],
            topic=""
        )
        
    def _check_boundaries(self, word: Word) -> None:
        """Verify if the word fits within the grid boundaries."""
        #print("Checking boundaries for word: ", word.word)
        for curr_x, curr_y in self._get_word_coordinates(word):
            if not (0 <= curr_x < self.width and 0 <= curr_y < self.height):
                raise ValueError(f"Word '{word.word}' extends beyond grid boundaries")
            

    def _check_letter_conflicts(self, word: Word) -> None:
        """Check for letter conflicts with existing words."""
        #print("Checking letter conflicts for word: ", word.word)
        for i, letter in enumerate(word.word):
            curr_x, curr_y = self._get_coordinate_at_index(word, i)
            
            for existing_word in self.words:
                for j, existing_letter in enumerate(existing_word.word):
                    check_x, check_y = self._get_coordinate_at_index(existing_word, j)
                    
                    if curr_x == check_x and curr_y == check_y:
                        if existing_letter == ' ' or existing_letter == "":
                            continue
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

    def _has_intersection(self, word: Word) -> bool:
        """Check if the word intersects with any existing words in the grid."""
        if not self.words:  # First word doesn't need intersection
            return True
            
        word_coords = set(self._get_word_coordinates(word))
        existing_coords = set()
        for existing_word in self.words:
            existing_coords.update(self._get_word_coordinates(existing_word))
            
        return bool(word_coords & existing_coords)  # Return True if there's any intersection

    def add_word(self, word: Word):
        """Add a word to the crossword after validating position and conflicts."""
       # print("Adding word: ", word.word, " to crossword")
        self._check_boundaries(word)
        self._check_letter_conflicts(word)
        
        if not self._has_intersection(word):
            raise ValueError(f"Word '{word.word}' must intersect with existing words")
            
        #print("Word added to crossword")
        self.words.append(word)
        
        
    def _initialize_grid(self):
        """Initialize an empty grid with spaces."""
        print("Initializing grid with width: ", self.width, " and height: ", self.height)
        return [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def _fill_grid_with_words(self, grid):
        """Place all words in the grid."""
        print("Filling grid with words, we have ", len(self.words), " words")
        for word in self.words:
            x, y = word.pos_x, word.pos_y
            for letter in word.word:
                if 0 <= x < self.width and 0 <= y < self.height:
                    grid[y][x] = letter
                    if word.direction == Direction.ACROSS:
                        x += 1
                    else:  # Direction.DOWN
                        y += 1
        return grid

    def _print_coordinates_header(self):
        """Print the x-coordinates header."""
        print('   ', end='')
        for x in range(self.width):
            print(f'{x:2}', end='')
        print()

    def _print_horizontal_border(self):
        """Print horizontal border of the grid."""
        print('  ' + '-' * (self.width * 2 + 1))

    def _print_grid_rows(self, grid):
        """Print the grid rows with y-coordinates."""
        for y, row in enumerate(grid):
            print(f'{y:2}|', end=' ')
            for cell in row:
                print(cell, end=' ')
            print('|')

    def _get_sorted_clues(self):
        """Get sorted lists of across and down clues."""
        across_clues = []
        down_clues = []
        
        for word in self.words:
            clue_text = f"{word.word} - {word.clue}" if word.clue else word.word
            if word.direction == Direction.ACROSS:
                across_clues.append(f"({word.pos_x}, {word.pos_y}) {clue_text}")
            else:
                down_clues.append(f"({word.pos_x}, {word.pos_y}) {clue_text}")
        
        return across_clues, down_clues

    def _print_clues(self, across_clues, down_clues):
        """Print the across and down clues."""
        print("\nClues:")
        if across_clues:
            print("\nAcross:")
            for clue in across_clues:
                print(f"  {clue}")
        
        if down_clues:
            print("\nDown:")
            for clue in down_clues:
                print(f"  {clue}")

    def print_crossword(self):
        """Print the complete crossword puzzle with grid and clues."""
        grid = self._initialize_grid()
        grid = self._fill_grid_with_words(grid)
        
        self._print_coordinates_header()
        self._print_horizontal_border()
        self._print_grid_rows(grid)
        self._print_horizontal_border()
        
        across_clues, down_clues = self._get_sorted_clues()
        self._print_clues(across_clues, down_clues)

    def get_crossword_string(self) -> str:
        """Return the complete crossword puzzle with grid and clues as a string."""
        lines = []
        grid = self._initialize_grid()
        grid = self._fill_grid_with_words(grid)
        
        # Add coordinates header
        header = '   '
        header += ''.join(f'{x:2}' for x in range(self.width))
        lines.append(header)
        
        # Add horizontal border
        border = '  ' + '-' * (self.width * 2 + 1)
        lines.append(border)
        
        # Add grid rows
        for y, row in enumerate(grid):
            grid_line = f'{y:2}|'
            grid_line += ' '.join(cell for cell in row)
            grid_line += ' |'
            lines.append(grid_line)
        
        # Add bottom border
        lines.append(border)
        
        # Add clues
        across_clues, down_clues = self._get_sorted_clues()
        
        lines.append("\nClues:")
        if across_clues:
            lines.append("\nAcross:")
            for clue in across_clues:
                lines.append(f"  {clue}")
        
        if down_clues:
            lines.append("\nDown:")
            for clue in down_clues:
                lines.append(f"  {clue}")
        
        return '\n'.join(lines)

    def get_letter_constraints_for_word(self, new_word: Word) -> LetterConstraint:
        """
        Returns a LetterConstraint for 'new_word' by scanning the current Crossword grid
        to see if any letters are already fixed at the positions where 'new_word' would go.
        """
        # Create a fresh grid that includes all previously added words.
        grid = self._initialize_grid()
        grid = self._fill_grid_with_words(grid)

        # Prepare a blank constraint list for the new word (all None initially).
        constraints = [None] * len(new_word.word)

        # For each position in the new word, check if the grid has a letter (non-blank).
        for i in range(len(new_word.word)):
            x, y = self._get_coordinate_at_index(new_word, i)
            if grid[y][x] != ' ':
                # Use the already placed letter from the grid as a constraint.
                constraints[i] = grid[y][x].upper()

        # Build and return a LetterConstraint object.
        return LetterConstraint(constraints)

def create_crossword():
    print("Creating crossword")
    """
    Not used by reflex, only for testing stuff
    """
    width = 20
    height = 10
    crossword = Crossword(width=width, height=height)
    crossword.words = []
    words = generate_word_pattern(width, height, 1)
    for word in words:
        crossword.add_word(word)
        print(word.word)
    """
    crossword.add_word(Word("Strawberry", pos_x=0, pos_y=0, direction=Direction.ACROSS, 
                           clue="Sweet red fruit"))
    crossword.add_word(Word("Bananas", pos_x=5, pos_y=0, direction=Direction.DOWN, 
                           clue="Yellow curved fruit"))
    crossword.add_word(Word("Raw", pos_x=7, pos_y=0, direction=Direction.DOWN, 
                           clue="Uncooked"))
    crossword.add_word(Word("New", pos_x=5, pos_y=2, direction=Direction.ACROSS, 
                           clue="Not old"))
    """
    crossword.print_crossword()
    
def generate_word_pattern(width: int, height: int, num_words: int) -> list[Word]:
    """Generate a pattern of intersecting words suitable for a crossword puzzle."""
    words = []
    min_word_length = 3
    max_word_length = 8
    
    # Place first word near the center
    first_word_length = random.randint(5, max_word_length)
    middle_y = height // 4
    start_x = (width - first_word_length) // 2
    
    words.append(Word("-" * first_word_length, start_x, middle_y, Direction.ACROSS))
    print(f"First word length: {first_word_length}")
    attempts = 0
    max_attempts = 1000
    
    def would_extend_existing_word(new_word: Word) -> bool:
        """Check if the new word would extend an existing word."""
        new_coords = set([(x, y) for x, y in crossword._get_word_coordinates(new_word)])
        
        # Check one position before and after each existing word
        for word in words:
            if word.direction == Direction.ACROSS:
                start_x = word.pos_x - 1
                end_x = word.pos_x + len(word.word)
                y = word.pos_y
                if (start_x, y) in new_coords or (end_x, y) in new_coords:
                    return True
            else:  # Direction.DOWN
                start_y = word.pos_y - 1
                end_y = word.pos_y + len(word.word)
                x = word.pos_x
                if (x, start_y) in new_coords or (x, end_y) in new_coords:
                    return True
        return False
    
    while len(words) < num_words and attempts < max_attempts:
        print(f"Attempts: {attempts}")
        parent_word = random.choice(words)
        new_direction = Direction.DOWN if parent_word.direction == Direction.ACROSS else Direction.ACROSS
        intersect_pos = random.randint(0, len(parent_word.word) - 1)
        
        # Calculate new word position
        if new_direction == Direction.ACROSS:
            new_y = parent_word.pos_y + (0 if parent_word.direction == Direction.ACROSS else intersect_pos)
            max_x = width - min_word_length
            possible_x = list(range(max(0, parent_word.pos_x - max_word_length + 1), max_x + 1))
            if possible_x:
                new_x = random.choice(possible_x)
                max_length = min(width - new_x, max_word_length)
            else:
                attempts += 1
                continue
        else:  # Direction.DOWN
            new_x = parent_word.pos_x + (0 if parent_word.direction == Direction.DOWN else intersect_pos)
            max_y = height - min_word_length
            possible_y = list(range(max(0, parent_word.pos_y - max_word_length + 1), max_y + 1))
            if possible_y:
                new_y = random.choice(possible_y)
                max_length = min(height - new_y, max_word_length)
            else:
                attempts += 1
                continue
        
        # Try different word lengths
        word_length = random.randint(min_word_length, max_length)
        temp_word = Word("-" * word_length, new_x, new_y, new_direction)
        print(f"New word length: {word_length}") 
        try:
            # Create temporary crossword for validation
            crossword = Crossword(width, height)
            for existing_word in words:
                crossword.add_word(existing_word)
            
            # Check if word would extend any existing words
            if would_extend_existing_word(temp_word):
                attempts += 1
                continue
                
            crossword.add_word(temp_word)
            
            # Check spacing between parallel words
            has_proper_spacing = True
            for word in words:
                if word.direction == temp_word.direction:
                    if word.direction == Direction.ACROSS:
                        if abs(word.pos_y - temp_word.pos_y) == 1:
                            has_proper_spacing = False
                            break
                    else:  # Direction.DOWN
                        if abs(word.pos_x - temp_word.pos_x) == 1:
                            has_proper_spacing = False
                            break
            
            if has_proper_spacing:
                words.append(temp_word)
                attempts = 0  # Reset attempts after successful placement
            else:
                attempts += 1
                
        except ValueError:
            attempts += 1
            continue
            
    return words
if __name__ == "__main__":
    create_crossword()
    
        


