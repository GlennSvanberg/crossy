from pydantic import BaseModel
from openai import OpenAI
from typing import List

client = OpenAI()

class Word(BaseModel):
    word: str
    clue: str

class LetterConstraint:
    def __init__(self, pattern: List[str | None]):
        """Initialize with a list of letters or None, e.g. [None, 'A', None, 'T', None]"""
        self.pattern = pattern

    def to_string(self) -> str:
        """Convert the pattern to a readable string format like '_A_T_'"""
        return ''.join('_' if letter is None else letter for letter in self.pattern)

    @classmethod
    def from_string(cls, pattern: str) -> 'LetterConstraint':
        """Create from a string like '_A_T_'"""
        return cls([None if c == '_' else c for c in pattern])

SYSTEM_PROMPT = """
You are a crossword puzzle expert generator.
You are given a topic and a word length. Based on this you will create a fitting word 
for a crossword puzzle. 

You will return a JSON object with the word and a clue.
*The clue must be super short
*The word should be a single word and not a phrase.
*The word should be in the language provided.
*The clue should be in the language provided.
*The word should be of the length provided.

*The word MUST match the letter pattern provided, where '_' means any letter and other characters must match exactly.
*The word MUST be a real COMMON word in the language provided.

"""

USER_PROMPT = """
Theme: {theme}
Language: {language}
Word length: {word_length}
Letter pattern: {letter_pattern}
Additional constraints: {constraints}
"""

def generate_word(
    theme: str,
    language: str,
    word_length: int,
    letter_constraints: LetterConstraint | None = None,
    additional_constraints: str = ""
) -> Word:
    print(f"Generating word for theme: {theme}, language: {language}, word length: {word_length}, letter constraints: {letter_constraints}, additional constraints: {additional_constraints}")
    if letter_constraints is None:
        letter_pattern = '_' * word_length
    else:
        letter_pattern = letter_constraints.to_string()
        
    formatted_prompt = USER_PROMPT.format(
        theme=theme,
        language=language,
        word_length=word_length,
        letter_pattern=letter_pattern,
        constraints=additional_constraints
    )
    
    last_error = None
    max_attempts = 6
    
    for attempt in range(max_attempts):
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": formatted_prompt},
            ]
            
            # Add error feedback from previous attempt if it exists
            if last_error:
                messages.append({
                    "role": "user",
                    "content": f"Previous attempt failed with error: {last_error}. Please try again with a valid word."
                })
            
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06", #gpt-4o-mini-2024-07-18
                messages=messages,
                response_format=Word,
            )
            word = completion.choices[0].message.parsed

            # Validate word length
            if len(word.word) != word_length:
                raise ValueError(f"Generated word '{word.word}' length ({len(word.word)}) does not match required length ({word_length})")

            # Validate letter constraints if they exist
            if letter_constraints:
                for i, (constraint, letter) in enumerate(zip(letter_constraints.pattern, word.word)):
                    if constraint is not None and constraint.lower() != letter.lower():
                        raise ValueError(f"Generated word '{word.word}' violates letter constraint at position {i}: expected '{constraint}', got '{letter}'")

            return word
            
        except ValueError as e:
            last_error = str(e)
            if attempt == max_attempts - 1:
                raise ValueError(f"Failed to generate valid word after {max_attempts} attempts. Last error: {last_error}")

if __name__ == "__main__":
    constraints = LetterConstraint([None, None, "V", None, None])
    print(generate_word("Winter", "Swedish", 5, constraints))
