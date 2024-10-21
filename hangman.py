import random

def log(func):
    def wrapper(hangman_game):
        result = func(hangman_game)
        guessed_letter = hangman_game.latest_guess
        is_correct = guessed_letter in hangman_game.word
        with open('hangman_log.txt', 'a') as f:
            f.write(f"Guessed: {guessed_letter}, Correct: {is_correct}, State: {hangman_game}\n")
        return result
    return wrapper

class Hangman:
    def __init__(self, word, attempts=6):
        self.word = word.lower()
        self.guessed_letters = set()
        self.attempts = attempts
        self.wrong_attempts = 0
        self.latest_guess = ''

    @log
    def guess_letter(self):
        while True:
            letter = input("Guess a letter: ").lower()
            if not letter.isalpha() or len(letter) != 1:
                print("Enter a single letter.")
                continue
            elif letter in self.guessed_letters:
                print("You already guessed that letter.")
                continue

            self.latest_guess = letter
            self.guessed_letters.add(letter)
            if letter in self.word:
                print(f"Good Guess! Word: {self.display_word()}")
            else:
                self.wrong_attempts += 1
                print(f"Wrong guess! Attempts left: {self.attempts - self.wrong_attempts}")
                self.display_hangman()
            break

    def display_word(self):
        return " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])

    def display_hangman(self):
        stages = [
            """
            ------
               |    |
                    |
                    |
                    |
                    |
              --------
            """,
            """
               ------
               |    |
               O    |
                    |
                    |
                    |
              --------
            """,
            """
               ------
               |    |
               O    |
               |    |
                    |
                    |
              --------
            """,
            """
               ------
               |    |
               O    |
              /|    |
                    |
                    |
              --------
            """,
            """
               ------
               |    |
               O    |
              /|\   |
                    |
                    |
              --------
            """,
            """
               ------
               |    |
               O    |
              /|\   |
              /     |
                    |
              --------
            """,
            """
               ------
               |    |
               O    |
              /|\   |
              / \   |
                    |
              --------
            """
        ]
        print(stages[self.wrong_attempts])

    def is_game_over(self):
        return self.wrong_attempts >= self.attempts or self.has_won()

    def has_won(self):
        for letter in self.word:
            if letter not in self.guessed_letters:
                return False
        return True

    def __str__(self):
        return f"Word: {self.display_word()} | Wrong Attempts: {self.wrong_attempts}"

if __name__ == "__main__":
    with open('words.txt', 'r') as file:
        words = file.read().split('\n')
        random_word = random.choice(words)
        game = Hangman(random_word)

        print("Welcome to Hangman!")
        while not game.is_game_over():
            print(game)
            game.guess_letter()

        if game.has_won():
            print(f"Congratulations, you've won! The word was: {game.word}")
        else:
            print(f"Game Over. The word was: {game.word}")
