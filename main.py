import tkinter as tk
from time import time
import random

# Application class
class TypingTrainer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing Trainer")

        # Load text samples
        self.text_samples = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Vivamus sagittis lacus vel augue laoreet rutrum faucibus.",
            "Sed posuere consectetur est at lobortis.",
            "Integer posuere erat a ante venenatis dapibus."
        ]
        self.sample_index = 0
        self.current_sample = self.text_samples[self.sample_index]

        # Load high score
        self.high_score = self.load_high_score()

        # Initialize variables
        self.start_time = None
        self.error_count = 0

        # UI setup
        self.create_widgets()

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                return int(f.read().strip())
        except FileNotFoundError:
            return 0

    def save_high_score(self, score):
        with open('high_score.txt', 'w') as f:
            f.write(str(score))

    def create_widgets(self):
        # Instructions
        self.instructions_label = tk.Label(self, text="Type the text below and press Enter to see your result.", font=("Helvetica", 14))
        self.instructions_label.pack(pady=(10, 5))

        # Sample text display
        self.sample_label = tk.Label(self, text=self.current_sample, font=("Helvetica", 18), wraplength=600, justify=tk.LEFT)
        self.sample_label.pack(pady=(0, 10), padx=10)

        # Text entry for typing
        self.text_entry = tk.Text(self, height=6, width=50, font=("Helvetica", 16))
        self.text_entry.pack(pady=(0, 10), padx=10)
        self.text_entry.bind("<KeyPress>", self.start_test)
        self.text_entry.bind("<KeyRelease>", self.check_typing)

        # Labels for errors and high score
        self.error_label = tk.Label(self, text="Errors: 0", font=("Helvetica", 14))
        self.error_label.pack(pady=(5, 10))

        self.high_score_label = tk.Label(self, text=f"High Score: {self.high_score} WPM", font=("Helvetica", 14))
        self.high_score_label.pack(pady=(5, 10))

        # Result display
        self.result_label = tk.Label(self, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=(5, 10))

        # Next sample button
        self.next_button = tk.Button(self, text="Next Sample", command=self.next_sample)
        self.next_button.pack(pady=(0, 10))

        # Bind the Return key to the calculate_speed function
        self.bind('<Return>', self.calculate_speed)

    def start_test(self, event):
        if self.start_time is None:
            self.start_time = time()

    def check_typing(self, event):
        typed_text = self.text_entry.get("1.0", tk.END).rstrip("\n")
        sample = self.current_sample[:len(typed_text)]
        self.error_count = sum(1 for a, b in zip(typed_text, sample) if a != b)
        self.error_label.config(text=f"Errors: {self.error_count}")

    def calculate_speed(self, event):
        if self.start_time is not None:
            end_time = time()
            time_taken = (end_time - self.start_time) / 60
            typed_text = self.text_entry.get("1.0", tk.END).strip()
            word_count = len(typed_text.split())
            wpm = word_count / time_taken - (2 * self.error_count)  # 2 WPM penalty for each error
            self.result_label.config(text=f"Your typing speed: {wpm:.2f} WPM with {self.error_count} errors")

            # Update high score if needed
            if wpm > self.high_score:
                self.high_score = wpm
                self.save_high_score(wpm)
                self.high_score_label.config(text=f"High Score: {self.high_score:.2f} WPM")

    def next_sample(self):
        self.sample_index = (self.sample_index + 1) % len(self.text_samples)
        self.current_sample = self.text_samples[self.sample_index]
        self.sample_label.config(text=self.current_sample)
        self.reset_test()

    def reset_test(self):
        self.start_time = None
        self.error_count = 0
        self.error_label.config(text="Errors: 0")
        self.result_label.config(text="")
        self.text_entry.delete("1.0", tk.END)
        self.text_entry.focus()

# Main application
if __name__ == "__main__":
    app = TypingTrainer()
    app.mainloop()
