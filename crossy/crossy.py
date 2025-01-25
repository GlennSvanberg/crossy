"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

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
    
    def create_crossword(self):
        print("Creating a new crossword puzzle")
        #build_crossword_puzzle("Pizza", 10, 10)
    
    def initialize_grid(self):
        print("initialize_grid")
        rows = 20
        cols = 20
        num_words = 8
        crossword = Crossword(rows,cols)
        try:
            word_pattern = generate_word_pattern(rows, cols, num_words)
            for word in word_pattern:
                crossword.add_word(word)

            # Convert crossword grid to our Row/Cell format
            grid = crossword._initialize_grid()
            grid = crossword._fill_grid_with_words(grid)
            
            # Convert to Reflex Row/Cell format
            new_rows = []
            for y, row in enumerate(grid):
                cells = []
                for x, letter in enumerate(row):
                    is_black = letter == ' '
                    cells.append(Cell(
                        letter=" " if is_black else letter,
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