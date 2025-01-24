"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config

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
    
    def initialize_grid(self):
        print("initialize_grid")
        #return
        self.rows = [
            Row(row=[
                Cell(letter="A", number=0, is_black=False, pos_x=0, pos_y=0),
                Cell(letter="B", number=0, is_black=False, pos_x=1, pos_y=0),
                Cell(letter="C", number=0, is_black=False, pos_x=2, pos_y=0)
            ]),
            Row(row=[
                Cell(letter="D", number=0, is_black=False, pos_x=0, pos_y=1),
                Cell(letter=" ", number=0, is_black=True, pos_x=1, pos_y=1),
                Cell(letter="F", number=0, is_black=False, pos_x=2, pos_y=1)
            ]),
            Row(row=[
                Cell(letter="G", number=0, is_black=False, pos_x=0, pos_y=2),
                Cell(letter="H", number=0, is_black=False, pos_x=1, pos_y=2),
                Cell(letter="I", number=0, is_black=False, pos_x=2, pos_y=2)
            ])
        ]
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
                width="100px",
                height="100px",
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
    )

def show_row(row: Row) -> rx.Component:
    return rx.table.row(
        rx.foreach(row.row, show_cell)
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
            ),
            align="center",
        ),
        center_content=True,
        width="100%",
        height="100vh",
    )


app = rx.App()
app.add_page(index)
