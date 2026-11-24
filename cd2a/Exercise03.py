import copy
import tkinter as tk
from tkinter import messagebox, simpledialog

FILE_NAME = "studentMarks.txt"


class StudentManager:
    def __init__(self, root):
        root.title("Student Manager")
        root.geometry("850x600")
        root.configure(bg="lightblue")
        self.students = []

        tk.Label(root, text="Student Manager", font=("Arial", 20, "bold"),
                 bg="lightblue").pack(pady=10)

        menu = tk.Frame(root, bg="lightblue")
        menu.pack(pady=5)
        buttons = [
            ("1. View All Records", self.view_all),
            ("2. View Individual", self.view_individual),
            ("3. Highest Score", lambda: self.show_extreme(max, "HIGHEST")),
            ("4. Lowest Score", lambda: self.show_extreme(min, "LOWEST")),
            ("5. Sort Records", self.sort_records),
            ("6. Add Student", self.add_student),
            ("7. Delete Student", self.delete_student),
            ("8. Update Student", self.update_student),
        ]
        for i, (text, command) in enumerate(buttons):
            tk.Button(menu, text=text, width=19, command=command).grid(
                row=i // 4, column=i % 4, padx=4, pady=5)

        self.output = tk.Text(root, width=100, height=23,
                              font=("Courier New", 10), wrap="none")
        self.output.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Button(root, text="Quit", width=15, command=root.destroy).pack(pady=8)

        self.load_students()

    # ---------- File handling ----------
    def load_students(self):
        try:
            with open(FILE_NAME, encoding="utf-8") as file:
                lines = [line.strip() for line in file if line.strip()]
            if not lines:
                raise ValueError("The file is empty.")

            students = []
            for line in lines[1:]:
                parts = line.split(",")
                if len(parts) != 6:
                    raise ValueError("Invalid student record: " + line)

                code, name = int(parts[0]), parts[1].strip()
                marks = [int(p) for p in parts[2:5]]
                exam = int(parts[5])

                if not 1000 <= code <= 9999:
                    raise ValueError("Student code must have 4 digits.")
                if not name:
                    raise ValueError("Student name cannot be empty.")
                if not all(0 <= m <= 20 for m in marks):
                    raise ValueError("Coursework marks must be 0 to 20.")
                if not 0 <= exam <= 100:
                    raise ValueError("Exam mark must be 0 to 100.")
                if any(s["code"] == code for s in students):
                    raise ValueError("Duplicate student code: " + str(code))

                students.append({"code": code, "name": name,
                                 "marks": marks, "exam": exam})

            if int(lines[0]) != len(students):
                raise ValueError("The student count on the first line "
                                 "does not match the number of records.")
            self.students = students

        except (FileNotFoundError, ValueError) as error:
            messagebox.showerror("File Error", str(error))
            self.students = []

    def save_students(self):
        try:
            with open(FILE_NAME, "w", encoding="utf-8") as file:
                file.write(f"{len(self.students)}\n")
                for s in self.students:
                    fields = [s["code"], s["name"], *s["marks"], s["exam"]]
                    file.write(",".join(map(str, fields)) + "\n")
            return True
        except OSError as error:
            messagebox.showerror("Save Error", str(error))
            return False

    # ---------- Calculations ----------
    def total_score(self, student):
        return sum(student["marks"]) + student["exam"]

    def percentage(self, student):
        return self.total_score(student) / 160 * 100

    def grade(self, student):
        pct = self.percentage(student)
        for minimum, letter in [(70, "A"), (60, "B"), (50, "C"), (40, "D")]:
            if pct >= minimum:
                return letter
        return "F"

    # ---------- Display helpers ----------
    def format_student(self, student):
        return (
            f"Name: {student['name']}\n"
            f"Student Number: {student['code']}\n"
            f"Coursework Mark: {sum(student['marks'])}/60\n"
            f"Exam Mark: {student['exam']}/100\n"
            f"Total Mark: {self.total_score(student)}/160\n"
            f"Overall Percentage: {self.percentage(student):.2f}%\n"
            f"Grade: {self.grade(student)}\n"
            + "-" * 45 + "\n"
        )

    def show_output(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def show_list(self, title, students):
        text = f"{title}\n" + "=" * 45 + "\n"
        text += "".join(self.format_student(s) for s in students)
        return text

    def has_students(self):
        if not self.students:
            self.show_output("No student records available.")
        return bool(self.students)

    def find_student(self):
        search = simpledialog.askstring(
            "Find Student", "Enter student name or student code:")
        if not search or not search.strip():
            return None

        search = search.strip()
        for s in self.students:
            if search.lower() == s["name"].lower() or search == str(s["code"]):
                return s

        messagebox.showwarning("Not Found",
                               "No student matches that name or code.")
        return None

    def ask_code(self, prompt, current=None):
        """Ask for a unique 4-digit code. Returns None if cancelled/duplicate."""
        code = simpledialog.askinteger("Student Code", prompt,
                                       minvalue=1000, maxvalue=9999)
        if code is None:
            return None
        if any(s["code"] == code and s is not current for s in self.students):
            messagebox.showerror("Duplicate Code",
                                 "This student code already exists.")
            return None
        return code

    def ask_marks(self, prefix="Enter"):
        marks = []
        for i in range(1, 4):
            mark = simpledialog.askinteger(
                "Enter Mark", f"{prefix} coursework mark {i} (0-20):",
                minvalue=0, maxvalue=20)
            if mark is None:
                return None
            marks.append(mark)
        return marks

    def ask_exam(self, prefix="Enter"):
        return simpledialog.askinteger(
            "Enter Mark", f"{prefix} exam mark (0-100):",
            minvalue=0, maxvalue=100)

    # ---------- Menu actions ----------
    def view_all(self):
        if not self.has_students():
            return
        average = (sum(self.percentage(s) for s in self.students)
                   / len(self.students))
        text = self.show_list("ALL STUDENT RECORDS", self.students)
        text += (f"\nCLASS SUMMARY\n"
                 f"Number of students: {len(self.students)}\n"
                 f"Average percentage: {average:.2f}%\n")
        self.show_output(text)

    def view_individual(self):
        student = self.find_student()
        if student:
            self.show_output(self.format_student(student))

    def show_extreme(self, func, label):
        if self.has_students():
            best = func(self.students, key=self.total_score)
            self.show_output(self.show_list(
                f"STUDENT WITH {label} OVERALL SCORE", [best]))

    def sort_records(self):
        if not self.has_students():
            return
        ascending = messagebox.askyesno(
            "Sort Records",
            "Sort in ascending order?\n\n"
            "Yes = Lowest to Highest\nNo = Highest to Lowest")
        self.students.sort(key=self.total_score, reverse=not ascending)
        self.show_output(self.show_list("SORTED STUDENT RECORDS",
                                        self.students))

    def add_student(self):
        code = self.ask_code("Enter a 4-digit student code:")
        if code is None:
            return

        name = simpledialog.askstring("Add Student",
                                      "Enter the student's full name:")
        if not name or not name.strip():
            return

        marks = self.ask_marks()
        if marks is None:
            return

        exam = self.ask_exam()
        if exam is None:
            return

        student = {"code": code, "name": name.strip(),
                   "marks": marks, "exam": exam}
        self.students.append(student)

        if self.save_students():
            messagebox.showinfo("Success", "Student record added successfully.")
            self.show_output(self.format_student(student))
        else:
            self.students.remove(student)

    def delete_student(self):
        student = self.find_student()
        if student is None:
            return
        if not messagebox.askyesno(
                "Delete Student", f"Delete the record for {student['name']}?"):
            return

        index = self.students.index(student)
        self.students.remove(student)
        if self.save_students():
            messagebox.showinfo("Success", "Student record deleted.")
            self.show_output("Student record deleted successfully.")
        else:
            self.students.insert(index, student)

    def update_student(self):
        student = self.find_student()
        if student is None:
            return

        choice = simpledialog.askstring(
            "Update Student",
            "What would you like to update?\n"
            "1 = Name\n2 = Student code\n3 = Coursework marks\n4 = Exam mark")
        if choice is None:
            return

        backup = copy.deepcopy(student)

        if choice == "1":
            name = simpledialog.askstring("Update Name", "Enter the new name:")
            if not name or not name.strip():
                return
            student["name"] = name.strip()
        elif choice == "2":
            code = self.ask_code("Enter the new 4-digit code:", current=student)
            if code is None:
                return
            student["code"] = code
        elif choice == "3":
            marks = self.ask_marks("Enter new")
            if marks is None:
                return
            student["marks"] = marks
        elif choice == "4":
            exam = self.ask_exam("Enter the new")
            if exam is None:
                return
            student["exam"] = exam
        else:
            messagebox.showwarning("Invalid Option",
                                   "Please choose an option from 1 to 4.")
            return

        if self.save_students():
            messagebox.showinfo("Success",
                                "Student record updated successfully.")
            self.show_output(self.format_student(student))
        else:
            student.update(backup)


if __name__ == "__main__":
    root = tk.Tk()
    StudentManager(root)
    root.mainloop()