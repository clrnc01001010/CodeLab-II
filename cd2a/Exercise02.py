import random
import tkinter as tk
from tkinter import messagebox


class JokeAssistant:
    def __init__(self, root):
        root.title("Joke Telling Assistant")
        root.geometry("450x350")
        root.configure(bg="lightblue")

        self.current_joke = None

        try:
            with open("randomJokes.txt", encoding="utf-8") as file:
                lines = [line.strip().split("|") for line in file]
            self.jokes = [parts for parts in lines if len(parts) == 2]
        except FileNotFoundError:
            messagebox.showerror("File Error",
                                 "randomJokes.txt could not be found!")
            root.destroy()
            raise SystemExit

        tk.Label(root, text="Joke Telling Assistant",
                 font=("Arial", 18, "bold"), bg="lightblue").pack(pady=15)

        tk.Button(root, text="Alexa tell me a Joke",
                  command=self.tell_joke).pack(pady=5)

        self.setup_label = tk.Label(
            root, text="Click the button to hear a joke!",
            font=("Arial", 12), bg="lightblue", wraplength=400)
        self.setup_label.pack(pady=10)

        self.punchline_label = tk.Label(
            root, text="", font=("Arial", 12, "bold"),
            bg="lightblue", wraplength=400)
        self.punchline_label.pack(pady=10)

        tk.Button(root, text="Show Punchline",
                  command=self.show_punchline).pack(pady=5)
        tk.Button(root, text="Next Joke",
                  command=self.tell_joke).pack(pady=5)
        tk.Button(root, text="Quit", command=root.destroy).pack(pady=5)

    def tell_joke(self):
        if not self.jokes:
            messagebox.showwarning("No Jokes",
                                   "There are no jokes available in the file.")
            return

        self.current_joke = random.choice(self.jokes)
        self.setup_label.config(text=self.current_joke[0])
        self.punchline_label.config(text="")

    def show_punchline(self):
        if self.current_joke is None:
            messagebox.showinfo(
                "No Joke", "Please click 'Alexa tell me a Joke' first!")
        else:
            self.punchline_label.config(text=self.current_joke[1])


if __name__ == "__main__":
    root = tk.Tk()
    JokeAssistant(root)
    root.mainloop()