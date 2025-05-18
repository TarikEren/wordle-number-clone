import random
from typing import Optional, List, Dict

from enums import GameStatus, DigitStatus

class Game:
    """Game class for Numberle"""

    # Attempt limit
    ATTEMPT_LIMIT: int = 6

    def __init__(self, secret: Optional[str] = None):
        """
        Initialiser for the game class

        Args:
            secret (Optional[str]): For testing

        Fields:
            secret (int): Secret to guess
            all_guesses (list[list[dict]]): List containing all guesses
            attempt_count (int): How many attempts have been made
            game_status (int): Game status (Won, ongoing or lost)
        """
        self.secret: str = secret or str(random.randint(1000, 9999))
        self.all_guesses: list = []
        self.attempt_count: int = 0
        self.game_status: GameStatus = GameStatus.ONGOING
    
    @property
    def is_won(self) -> bool:
        return self.game_status == GameStatus.WON
    
    @property
    def is_over(self) -> bool:
        return self.game_status != GameStatus.ONGOING

    @property
    def is_lost(self) -> bool:
        return self.game_status == GameStatus.LOST
    
    @property
    def attempts_left(self) -> int:
        return Game.ATTEMPT_LIMIT - self.attempt_count
    
    def _update_status(self, guess: str) -> None:
        if guess == self.secret:
            self.game_status = GameStatus.WON
        elif self.attempt_count >= Game.ATTEMPT_LIMIT:
            self.game_status = GameStatus.LOST

    def __repr__(self):
        return f"<Game {self.game_status.name}, attempts={self.attempt_count}>"

    def submit_guess(self, guess: str) -> List[Dict]:
        """
        Evaluates the game
        - If the guess is equal to the secret, sets the status to won
        - Processes the guess
        - If the maximum guess count has been reached, sets the status to lost

        Args:
            guess (str): The guess being made
        
        Returns:
            (List[Dict]): The processed guess object
        """
        # Create a new guess
        new_guess: list = [None] * len(guess)

        # Turn secret into an iterable
        secret_chars: list[Optional[str]] = list(self.secret)

        # First pass for the numbers in the correct places
        for i, d in enumerate(guess):
            if d == secret_chars[i]:
                new_guess[i] = {"value": d, "status": DigitStatus.CORRECT}
                secret_chars[i] = None

        # Second pass for the misplaced and wrong ones
        for i, d in enumerate(guess):
            if new_guess[i] is None:
                if d in secret_chars:
                    new_guess[i] = {"value": d, "status": DigitStatus.MISPLACED}
                    secret_chars[secret_chars.index(d)] = None
                else:
                    new_guess[i] = {"value": d, "status": DigitStatus.WRONG}
        
        # Append the new guess to the all guesses list
        self.all_guesses.append(new_guess)

        # Increment the attempt count by one
        self.attempt_count += 1

        self._update_status(guess)

        return new_guess