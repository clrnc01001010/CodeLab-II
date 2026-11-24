import random
import tkinter as tk
from tkinter import messagebox

TOTAL_QUESTIONS = 10

# difficulty key: (button text, lowest number, highest number)
DIFFICULTIES = {
    "easy": ("Easy (0 - 99)", 0, 99),
    "moderate": ("Moderate (100 - 999)", 100, 999),
    "advanced": ("Advanced (1000 - 9999)", 1000, 9999),
}

MESSAGES = [
    (100, "Excellent! Perfect score!"),
    (80, "Great job! You did well!"),
    (60, "Good effort! Keep practicing!"),
    (40, "Not bad! You can improve!"),
    (0, "Keep trying! Practice makes perfect!"),
]

class MathQuizApp:
    def __init__(self, root):
        root.title("Math Quiz")
        root.geometry("400x400")
        root.configure(bg="lightblue")

        self.main_frame = tk.Frame(root, bg="lightblue")
        self.main_frame.pack(expand=True, fill="both")

        self.show_start_screen()

    # ---------- Helpers ----------
    def create_label(self, text, size=16, color="black", pady=10):
        tk.Label(
            self.main_frame, text=text, font=("Helvetica", size),
            bg="lightblue", fg=color, pady=pady
        ).pack(pady=pady)

    def create_button(self, text, command):
        tk.Button(
            self.main_frame, text=text, command=command, bg="blue",
            fg="black", font=("Helvetica", 12), relief="raised",
            activebackground="darkblue", cursor="hand2"
        ).pack(pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ---------- Screens ----------
    def show_start_screen(self):
        self.clear_frame()
        self.create_label("Welcome to the Math Quiz!", 18, "darkblue", 20)
        self.create_button("Start Quiz", self.show_difficulty_selection)

    def show_difficulty_selection(self):
        self.clear_frame()
        self.create_label("Select Difficulty Level:", 14)

        for key, (text, _, _) in DIFFICULTIES.items():
            self.create_button(text, lambda d=key: self.start_quiz(d))

    def start_quiz(self, difficulty):
        self.difficulty = difficulty
        self.question_number = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        if self.question_number == TOTAL_QUESTIONS:
            self.show_quiz_complete()
            return

        self.clear_frame()
        self.question_number += 1
        self.attempts = 0

        # Generate a random addition or subtraction problem
        _, low, high = DIFFICULTIES[self.difficulty]
        num1, num2 = random.randint(low, high), random.randint(low, high)
        operation = random.choice(["+", "-"])
        self.current_answer = num1 + num2 if operation == "+" else num1 - num2

        self.create_label(
            f"Question {self.question_number} of {TOTAL_QUESTIONS}", 14)
        self.create_label(f"{num1} {operation} {num2} = ?", 14)

        self.answer_entry = tk.Entry(
            self.main_frame, font=("Helvetica", 14), width=10)
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus_set()

        self.create_button("Submit Answer", self.check_answer)

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter a valid integer.")
            return

        if user_answer == self.current_answer:
            points = 10 if self.attempts == 0 else 5
            self.score += points
            messagebox.showinfo(
                "Correct!",
                f"Your answer is correct! You earned {points} points!")
            self.show_question()
            return

        self.attempts += 1
        if self.attempts == 1:
            messagebox.showwarning(
                "Try Again!", "Incorrect answer! You have one more chance.")
            self.answer_entry.delete(0, tk.END)
            self.answer_entry.focus_set()
        else:
            messagebox.showerror(
                "Incorrect",
                f"Both attempts were incorrect! "
                f"The correct answer was {self.current_answer}.")
            self.show_question()

    def show_quiz_complete(self):
        self.clear_frame()

        max_score = TOTAL_QUESTIONS * 10
        percentage = self.score / max_score * 100
        message = next(text for minimum, text in MESSAGES
                       if percentage >= minimum)

        self.create_label("Quiz Complete!", 18, "darkblue", 20)
        self.create_label(f"Your Score: {self.score} out of {max_score}", 14)
        self.create_label(f"Percentage: {percentage:.2f}%", 14)
        self.create_label(message, 14)
        self.create_button("Play Again", self.show_difficulty_selection)


if __name__ == "__main__":
    root = tk.Tk()
    MathQuizApp(root)
    root.mainloop()