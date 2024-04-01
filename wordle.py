import os
import argparse
import json
from termcolor import colored


class Wordle:
    def __init__(self):
        self.state_file = "./data/current_state.json"
        self.words_file = "./data/words.json"
        self.state = {}
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                self.state = json.load(f)
        else:
            with open(self.state_file, "w") as f:
                self.state = {
                    "guesses": [],
                    "word_index": 0,
                }
                json.dump(self.state_file, f)

    def load_word(self):
        if os.path.exists(self.words_file):
            with open(self.words_file, "r") as f:
                words = json.load(f)
        else:
            with open(self.words_file, "w") as f:
                words = ["apple", "baked", "chairs", "sours", "juice", "pasta", "pizza", "sugar", "syrup", "water"]
                json.dump(words, f)
        return words[self.state["word_index"]]

    def save_state(self, guess):
        with open(self.state_file, "w") as f:
            if len(self.state["guesses"]) >= len(self.load_word()):
                self.state["word_index"] += 1
                self.state["guesses"] = []
            elif guess == self.load_word():
                self.state["word_index"] += 1
                self.state["guesses"] = []


            json.dump(self.state, f)

    def eval_guess(self, guess):
        res = []
        target_word = self.load_word()
        for i, letter in enumerate(guess):
            if letter == target_word[i]:
                res.append(colored(letter, 'green'))
            elif letter in target_word:
                res.append(colored(letter, 'yellow'))
            else:
                res.append(colored(letter, 'red'))
        return " ".join(res)

    def get_guesses(self):
        return self.state["guesses"]

    def new_word(self):
        self.state["word_index"] = 0
        self.state["guesses"] = []

    def play_wordle(self, guess):
        target_word = self.load_word()
        res = self.eval_guess(guess)
        print(res)
        self.state["guesses"].append(guess)
        if guess == target_word:
            print('Congratulations! You won!')
        elif len(self.state["guesses"]) == len(target_word):
            print(f'You lost! The word was {target_word}')
            self.new_word()
        else:
            print(f"Guess {len(self.state['guesses'])} of {len(target_word)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play Wordle')
    parser.add_argument('guess', type=str, help='Your five-letter guess')
    args = parser.parse_args()
    wordle = Wordle()
    wordle.play_wordle(args.guess)
    wordle.save_state(args.guess)
