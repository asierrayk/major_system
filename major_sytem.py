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
        self.config = config
        max_len_coded_key = max([len(key) for key in self.config.keys()])
        if max_len_coded_key > 2:
            raise ValueError("Patterns should be composed by at most 2 letters")


    def decode(self, encoded_word: str) -> str:
        decoded_word = ""
        letter_index = 0
        while letter_index < len(encoded_word)-1:
            current_letter = encoded_word[letter_index]
            next_letter = encoded_word[letter_index+1]

            key = self.config.get(current_letter + next_letter)
            if key is not None:
                decoded_word += key
                letter_index += 2
            else:
                key = self.config.get(current_letter)
                if key is not None:
                    decoded_word += key
                letter_index += 1

        if letter_index == len(encoded_word) - 1:
            last_letter = encoded_word[-1]
            key = self.config.get(last_letter)
            if key is not None:
                decoded_word += key
        return decoded_word


    def encode(self, number: str, words: pd.DataFrame) -> pd.DataFrame:
        words["decoded"] = words.word.apply(self.decode)
        filtered_words = words[words.decoded == number]
        return filtered_words


class MyEncodeSystem(EncodeSystem):
    def __init__(self):
        config = {
            "r": "0",
            "d": "1",
            "t": "1",
            "n": "2",
            "gn": "2",
            "ñ": "2",
            "m": "3",
            "c": "4",
            "k": "4",
            "q": "4",
            "l": "5",
            "s": "6",
            "x": "6",
            "z": "6",
            "f": "7",
            "j": "7",
            "g": "8",
            "ch": "8",
            "b": "9",
            "p": "9",
            "v": "9",
        }
        super().__init__(config)


class AvailableEncodeSystems(Enum):
    MINE = MyEncodeSystem()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate to words')
    parser.add_argument("--number", "-n", type=str, help='number to convert to words')
    parser.add_argument("--encoder", "-e", type=str, default="mine", help='number to convert to words')

    args = parser.parse_args()
    print(f"Number: {args.number}")
    number = args.number


    word_database = AvailableDatabases.SPANISH.value
    words = word_database.get_db()

    encoder = AvailableEncodeSystems[args.encoder.upper()].value

    encoded_words = encoder.encode(number, words)


    results = encoded_words.word.tolist()

    print("\n".join(results))
