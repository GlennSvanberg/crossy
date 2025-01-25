from swarm import Swarm, Agent

client = Swarm()
from .model import Crossword, Word
from typing import List, Dict

INSTRUCTIONS = """
You are a helpful agent that builds simple crossword puzzles.
You must add words to the crossword puzzle.
You must specify the row and column of the first letter of the word.
You must specify the direction of the word, either "across" or "down".
Before adding a word, you must check if it fits within the grid boundaries.
Before adding a word, you must check if it conflicts with any existing words.
Each new word must intersect with at least one existing word.
Always start with a word that intersects the middle of the grid.
Only add 3 words to the crossword puzzle.
"""

class AgentExecutor:
    
    def __init__(self, crossword: Crossword):
        self.crossword: Crossword = crossword
        self.agent = Agent(
            name="Agent",
            model="gpt-4o-mini",
            instructions=INSTRUCTIONS,
            functions=[self.add_word],
        )
    def add_word(self,word: str, row: int, column: int, direction: str) -> None:
        """
        Add a word to the crossword puzzle.
        You must specify the row and column of the first letter of the word.
        You must specify the direction of the word, either "across" or "down".
        """
        response = f"Adding word: {word}\n"
        
        # validate the direction
        if direction not in ["across", "down"]:
            error_msg = "Direction must be either 'across' or 'down'"
            response += f"{error_msg}\n{self.crossword.get_crossword_string()}"
            print(response)
            return response
            
        # validate the row and column
        if row < 0 or column < 0 or row >= self.crossword.width or column >= self.crossword.height:
            error_msg = "Row and column must be within the bounds of the crossword puzzle"
            response += f"{error_msg}\n{self.crossword.get_crossword_string()}"
            print(response)
            return response
            
        try:
            word = Word(word, row, column, direction)
            self.crossword.add_word(word)   
            response += f"Word added successfully\n{self.crossword.get_crossword_string()}"
            print(response)
            return response
            
        except ValueError as e:
            error_msg = f"Failed to add word: {str(e)}"
            response += f"{error_msg}\n{self.crossword.get_crossword_string()}"
            print(response)
            return response
        
    def show_crossword(self) -> None:
        print("Showing crossword")
        
        print(self.crossword.get_crossword_string())
        
        return(self.crossword.get_crossword_string())
    def run(self, messages: List[Dict[str, str]]) -> None:
        response = client.run(agent=self.agent, messages=messages)
        print(response.messages[-1]["content"])


def build_crossword_puzzle(topic: str, rows: int, columns: int) -> str:
    crossword = Crossword(rows, columns)
    agent_executor = AgentExecutor(crossword)
    agent_executor.run([{"role": "user", "content": "Build a simple crossword puzzle with the topic: " + topic}])
    return agent_executor.show_crossword()


if __name__ == "__main__":
    build_crossword_puzzle("Pizza", 10, 10)
