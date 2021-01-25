import argparse
import pandas as pd
from typing import Dict, List

from enum import Enum

ABECEDARY = "abcdefghijklmnñopqrstuvwxyzáéíóúü"

class WordsDatabase:
    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name

class SpanishDatabase(WordsDatabase):
    def __init__(self):
        path = "words_dbs/espanol.txt"
        name = "Spanish"
        super().__init__(path, name)

    def get_db(self) -> pd.DataFrame:
        self.words = pd.read_csv(self.path, header=None, sep=" ", names=["word", "comment"], encoding="ISO-8859-1")
        return self.words


class AvailableDatabases(Enum):
    SPANISH = SpanishDatabase()


class EncodeSystem:
    def __init__(self, config: Dict[str, List[str]], abecedary: str=ABECEDARY):
        self.abecedary = {letter for letter in abecedary}

        self.config = config
        self.used_letters = set()
        for letters_for_number in self.config.values():
            for letter in letters_for_number:
                self.used_letters.add(letter)
        self.unused_letters = self.abecedary - self.used_letters

    @property
    def unused(self):
        return "".join(self.unused_letters)


    def encode(self, number: str, words: pd.DataFrame) -> pd.DataFrame:
        regex = f"^[{self.unused}]*"
        for d in number:
            digit_letters = "|".join(self.config[d])
            digit_regex = f"[{digit_letters}]"
            regex += digit_regex
            regex += f"[{self.unused}]*"
        regex += "$"
        print(f"regex for {args.number} {repr(regex)}")
        filtered_words = words[words.word.str.contains(regex)]
        return filtered_words


class MyEncodeSystem(EncodeSystem):
    def __init__(self):
        config = {
            "0": ["r"],
            "1": ["d", "t"],
            "2": ["n", "ñ"],
            "3": ["m"],
            "4": ["c", "k", "q"],
            "5": ["l"],
            "6": ["s", "z", "x"],
            "7": ["f", "j"],
            "8": ["g", "ch"],
            "9": ["b", "p", "v"]
        }
        super().__init__(config)


class AvailableEncodeSystems(Enum):
    MINE = MyEncodeSystem()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate to words')
    parser.add_argument("--number", "-n", type=str, help='number to convert to words')

    args = parser.parse_args()
    print(f"Number: {args.number}")
    number = args.number


    word_database = AvailableDatabases.SPANISH.value
    words = word_database.get_db()

    encoder = AvailableEncodeSystems.MINE.value

    encoded_words = encoder.encode(number, words)


    results = encoded_words.word.tolist()

    print("\n".join(results))
