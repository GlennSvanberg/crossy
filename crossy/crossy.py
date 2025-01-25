"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from .generate import generate_word, LetterConstraint

from .model import Crossword, Word, Direction, generate_word_pattern
from .agent import build_crossword_puzzle
class Cell(rx.Base):
    letter: str
    number: int
    is_black: bool
    pos_x: int
    pos_y: int

class Row(rx.Base):
    row: list[Cell]

            
class State(rx.State):
    rows: list[Row] = []
    crossword: Crossword = None
    
    def create_crossword(self):
        print("Creating a new crossword puzzle")
        #build_crossword_puzzle("Pizza", 10, 10)
        language = "English"
        theme = "Food"
        for word in self.crossword.words:
            print(word)
            print(f"length: {len(word.word)}")
            letter_constraints = self.crossword.get_letter_constraints_for_word(word)
            print(f"Letter constraints: {letter_constraints}")
            length = len(word.word)
            
            generated_word = generate_word(theme, language, length, letter_constraints)
            print(f"Result: {generated_word.word}")
            print(f"Clue: {generated_word.clue}")
            word.word = generated_word.word
            word.clue = generated_word.clue
        self.crossword.print_crossword()
            
            
            
    
    def initialize_grid(self):
        print("initialize_grid")
        width = 20
        height = 5
        num_words = 2
        crossword = Crossword(width,height)
        try:
            print("Generating word pattern")
            word_pattern = generate_word_pattern(width, height, num_words)
            print(f"Word pattern: {word_pattern}")
            for word in word_pattern:
                # Replace dashes with spaces in the word pattern
                word.word = word.word.replace("-", " ")
                crossword.add_word(word)
            self.crossword = crossword

            # Convert crossword grid to our Row/Cell format
            grid = crossword._initialize_grid()
            grid = crossword._fill_grid_with_words(grid)
            
            # Convert to Reflex Row/Cell format
            new_rows = []
            for y, row in enumerate(grid):
                cells = []
                for x, letter in enumerate(row):
                    # Change the logic here - only consider it black if it's outside the word pattern
                    is_black = True
                    for word in crossword.words:
                        if any((x, y) == coord for coord in crossword._get_word_coordinates(word)):
                            is_black = False
                            break
                        
                    cells.append(Cell(
                        letter=" ",  # Always initialize with space
                        number=0,
                        is_black=is_black,
                        pos_x=x,
                        pos_y=y
                    ))
                new_rows.append(Row(row=cells))
            
            self.rows = new_rows
            
        except ValueError as e:
            print(f"Error creating crossword: {e}")

    def set_cell_letter(self, pos_x: int, pos_y: int, letter: str):
        print(f"set_cell_letter: {pos_x}, {pos_y}, {letter}")
        if len(letter) > 1:
            print("too long")
            letter = letter[0]
        self.rows[pos_y].row[pos_x].letter = letter

    def reveal_solution(self):
        """Reveal the solution by filling in all letters from the crossword."""
        if not self.crossword:
            return
            
        # Get the filled grid from crossword
        grid = self.crossword._initialize_grid()
        grid = self.crossword._fill_grid_with_words(grid)
        
        # Update each cell in our rows with the solution
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                if not self.rows[y].row[x].is_black:
                    self.rows[y].row[x].letter = letter

def show_cell(cell: Cell) -> rx.Component:
    return rx.table.cell(
        rx.cond(
            cell.is_black,
            rx.text(" "),
            rx.input(
                value=cell.letter, 
                on_change=State.set_cell_letter(cell.pos_x, cell.pos_y),
                width="80px",
                height="80px",
                padding="0",
                margin="0",
                text_align="center",
                display="flex",
                align_items="center",
                justify_content="center",
                font_size="24px",
                
            )
        ),
        padding="0",
        margin="0",
        border="none",
        box_shadow="0px 0px 0px white",
        
    )

def show_row(row: Row) -> rx.Component:
    return rx.table.row(
        rx.foreach(row.row, show_cell),
        border="none",
        box_shadow="0px 0px 0px white",
        
    )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.vstack(
            rx.button("Initialize Grid", on_click=State.initialize_grid),
            rx.button("Create Crossword", on_click=State.create_crossword),
            rx.button("Reveal Solution", on_click=State.reveal_solution),
            rx.table.root(
                rx.table.body(
                    rx.foreach(State.rows, show_row),
                    spacing="0",
                    width="100%",
                ),
                spacing="0",
                border_spacing="0",
                width="min-content",
                padding="0",
                border="solid blue",
                
                
            ),
            align="center",
        ),
        center_content=True,
        width="100%",
        height="100vh",
    )


app = rx.App()
app.add_page(index)
# --table-row-box-shadow: inset 0 -1px var(--gray-a5); Need to find a way of disabling this