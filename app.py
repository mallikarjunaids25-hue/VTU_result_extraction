import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import re

# 1. SAMPLE DATABASE
DATA = {
    "1CR25AD053": {
        "name": "Karthik",
        "semesters": {
            1: [("BMATS101", "Mathematics", 4, 79),
                ("BPHYS102", "Physics", 4, 74)],
            2: [("BMATS201", "Mathematics", 4, 73),
                ("BCHES202", "Chemistry", 4, 78)]
        }
    },
    "1CR25AD060": {
        "name": "Mallikarjuna",
        "semesters": {
            1: [("BMATS101", "Mathematics", 4, 88),
                ("BPHYS102", "Physics", 4, 82)],
            2: [("BMATS201", "Mathematics", 4, 85),
                ("BCHES202", "Chemistry", 4, 82)],
            3: [("BCS301", "Data Structures", 4, 84),
                ("BCS302", "DDCO", 4, 79)]
        }
    },
    "1CR25AD063": {
        "name": "Nandha Kumar V",
        "semesters": {
            1: [("BMATS101", "Mathematics", 4, 33),
                ("BPHYS102", "Physics", 4, 71)]
        }
    }
}

# 2. GRADE CALCULATION
def grade(total):
    if total >= 90: return "O", 10
    if total >= 80: return "A+", 9
    if total >= 70: return "A", 8
    if total >= 60: return "B+", 7
    if total >= 55: return "B", 6
    if total >= 50: return "C", 5
    if total >= 40: return "P", 4
    return "F", 0

# 3. RESULT PROCESSING
def get_result():
    usn = usn_entry.get().strip().upper()
    sem = sem_box.get()

    if not re.match(r"^[1-4][A-Z]{2}\d{2}[A-Z]{2,3}\d{3}$", usn):
        messagebox.showerror("Error", "Invalid USN")
        return

    if usn not in DATA or not sem:
        messagebox.showerror("Error", "Result not available")
        return

    sem = int(sem)
    student = DATA[usn]

    if sem not in student["semesters"]:
        messagebox.showerror("Error", "Semester not available")
        return

    rows = student["semesters"][sem]
    result = []
    credits = points = 0
    passed = True

    for code, subject, cr, total in rows:
        g, gp = grade(total)
        status = "PASS" if g != "F" else "FAIL"

        if status == "FAIL":
            passed = False

        credits += cr
        points += cr * gp

        result.append((code, subject, cr, total, g, status))

    sgpa = round(points / credits, 2) if credits else 0
    final = "PASS" if passed else "FAIL"

    # DISPLAY RESULT
    for item in table.get_children():
        table.delete(item)

    for row in result:
        table.insert("", "end", values=row)

    name_label.config(
        text=f"Name: {student['name']} | USN: {usn} | Semester: {sem}"
    )

    sgpa_label.config(text=f"SGPA: {sgpa}")
    status_label.config(text=f"Result: {final}")

    # SEMESTER HISTORY
    history_table.delete(*history_table.get_children())

    for s in sorted(student["semesters"]):
        if s == sem:
            history_table.insert("", "end", values=(s, sgpa, final))
        else:
            history_table.insert("", "end", values=(s, "Available", "-"))

    # CSV DATA
    current_result.clear()

    current_result.extend([
        ["USN", usn],
        ["Name", student["name"]],
        ["Semester", sem],
        ["SGPA", sgpa],
        ["Result", final],
        [],
        ["Code", "Subject", "Credits", "Total", "Grade", "Status"]
    ])

    current_result.extend(result)

# 4. SAVE CSV
def save_result():
    if not current_result:
        messagebox.showerror("Error", "Get result first")
        return

    path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )

    if path:
        with open(path, "w", newline="") as f:
            csv.writer(f).writerows(current_result)

        messagebox.showinfo("Saved", "Result saved successfully")

# 5. GUI DESIGN
root = tk.Tk()
root.title("VTU Result Extraction App")
root.geometry("850x600")
root.configure(bg="#f2f5f8")

tk.Label(
    root, text="VTU RESULT EXTRACTION APP",
    font=("Arial", 20, "bold"),
    bg="#0f567f", fg="white", pady=15
).pack(fill="x")

frame = tk.Frame(root, bg="white", pady=15)
frame.pack(pady=15)

tk.Label(frame, text="Enter USN:", bg="white").grid(row=0, column=0)

usn_entry = tk.Entry(frame, width=20)
usn_entry.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Semester:", bg="white").grid(row=0, column=2)

sem_box = ttk.Combobox(
    frame, values=[1,2,3,4,5,6,7,8],
    width=8, state="readonly"
)
sem_box.grid(row=0, column=3, padx=10)

tk.Button(
    frame, text="Get Result",
    command=get_result,
    bg="#0f567f", fg="white"
).grid(row=0, column=4)

name_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
name_label.pack(pady=5)

columns = ("Code", "Subject", "Credits", "Total", "Grade", "Status")

table = ttk.Treeview(
    root, columns=columns,
    show="headings", height=6
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)

table.pack(pady=10)

sgpa_label = tk.Label(root, text="SGPA:", font=("Arial", 12, "bold"))
sgpa_label.pack()

status_label = tk.Label(root, text="Result:", font=("Arial", 12, "bold"))
status_label.pack()

tk.Label(
    root, text="Semester History",
    font=("Arial", 12, "bold")
).pack(pady=5)

history_table = ttk.Treeview(
    root, columns=("Semester", "SGPA", "Result"),
    show="headings", height=3
)

for col in ("Semester", "SGPA", "Result"):
    history_table.heading(col, text=col)
    history_table.column(col, width=150)

history_table.pack()

current_result = []

tk.Button(
    root, text="Save Result (CSV)",
    command=save_result,
    bg="#a6ce39",
    font=("Arial", 10, "bold")
).pack(pady=12)

root.mainloop()
