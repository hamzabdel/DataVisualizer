import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD #adding drag and drop later
import userside

def handle_drop(event):
    filepath = event.data.strip()
    userside.process_file(filepath)

def open_file():
    filepath = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV Files", "*.csv"), ("All files", "*.*"))
    )
    if filepath:
        userside.process_file(filepath)

root = TkinterDnD.Tk()
root.title("File Upload")
root.geometry("400x200")

label = tk.Label(root, text="Click below to select your file!", wraplength=300)
label.pack(pady=20)

button = tk.Button(root, text="Choose File", command=open_file)
button.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

root.mainloop()
