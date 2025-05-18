from typing import List

import tkinter as tk
from tkinter import messagebox

from game import Game
from enums import DigitStatus, GameStatus

# Tkinter UI
class NumberleApp(tk.Tk):
    CELL_SIZE = 50
    PADDING = 5
    COLORS = {
        DigitStatus.CORRECT: '#6aaa64',    # green
        DigitStatus.MISPLACED: '#c9b458',  # yellow
        DigitStatus.WRONG: '#787c7e',      # gray
        None: 'white'
    }

    def __init__(self):
        super().__init__()
        self.title('Numberle')
        self.game = Game()
        self.cells: List[List[tk.Label]] = []
        self._build_ui()

    def _build_ui(self):
        # Grid of labels
        for row in range(Game.ATTEMPT_LIMIT):
            row_cells = []
            for col in range(4):
                lbl = tk.Label(self, text=' ', width=2, height=1,
                               font=('Helvetica', 24, 'bold'),
                               borderwidth=2, relief='groove',
                               bg='white')
                lbl.grid(row=row, column=col, padx=self.PADDING, pady=self.PADDING)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        # Entry and submit
        self.entry = tk.Entry(self, font=('Helvetica', 18), width=4, justify='center')
        self.entry.grid(row=Game.ATTEMPT_LIMIT, column=0, columnspan=2, pady=(10,0))
        self.entry.focus()
        submit_btn = tk.Button(self, text='Submit', command=self.on_submit)
        submit_btn.grid(row=Game.ATTEMPT_LIMIT, column=2, columnspan=2, pady=(10,0))

    def on_submit(self):
        guess = self.entry.get().strip()
        # Validate: must be 4 digits
        if not (guess.isdigit() and len(guess) == 4):
            messagebox.showwarning('Invalid', 'Enter exactly 4 digits.')
            return
        # Process guess
        feedback = self.game.submit_guess(guess)
        row = self.game.attempt_count - 1
        for col, cell_info in enumerate(feedback):
            val = cell_info['value']
            status = cell_info['status']
            lbl = self.cells[row][col]
            lbl.config(text=val, bg=self.COLORS[status], fg='white')

        self.entry.delete(0, tk.END)

        # Check end of game
        if self.game.game_status == GameStatus.WON:
            messagebox.showinfo('Numberle', f'You won in {self.game.attempt_count} attempts!')
            self.entry.config(state='disabled')
        elif self.game.game_status == GameStatus.LOST:
            messagebox.showinfo('Numberle', f'You lost! Code was {self.game.secret}')
            self.entry.config(state='disabled')

if __name__ == '__main__':
    app = NumberleApp()
    app.mainloop()