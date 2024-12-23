import tkinter as tk
from tkinter import filedialog, Toplevel
from tkinterdnd2 import DND_FILES, TkinterDnD
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

file_data = None

def on_exit():
    print("Application is closing!")
    root.destroy()
    exit()

def handle_drop(event): # planning to implement drag and drop functionality on .csv files!
    filepath = event.data.strip()
    process_file(filepath)


def open_file():
    filepath = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV Files", "*.csv"), ("All files", "*.*"))
    )
    if filepath:
        process_file(filepath)


def process_file(filepath):
    global file_data
    if not filepath.endswith('.csv'):
        print("Provide a valid CSV file.")
        return

    try:
        file_data = pd.read_csv(filepath)
        print("File loaded!")
        print(file_data.head())
        show_graph_window(filepath)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")


def show_graph_window(filepath):
    global file_data
    if file_data is None or len(file_data.columns) < 2:
        print("CSV file does not have enough columns to plot.")
        return

    graph_window = Toplevel(root)
    graph_window.title(f"Graph Analysis - {filepath.split('/')[-1]}")
    graph_window.geometry("600x500")

    fig, ax = plt.subplots(figsize=(6, 4))
    for i in range(1, len(file_data.columns)):
        ax.plot(file_data.iloc[:, 0], file_data.iloc[:, i], marker='o', linestyle='-', label=file_data.columns[i])

    ax.set_xlabel(file_data.columns[0])
    ax.set_ylabel("Value")
    ax.set_title("Statistical Analysis Graph")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    analysis_button = tk.Button(
        graph_window,
        text="Statistical Analysis!",
        command=analyze_data,
        bg='green',
        fg='white'
    )
    analysis_button.pack(pady=10)


def analyze_data():
    try:
        numeric_data = file_data.select_dtypes(include='number')
        stats = numeric_data.describe()

        formatted_stats = stats.to_string(justify="center", float_format="{:.2f}".format)
        print("Summary Statistics: ")
        print(stats)

        result_window = Toplevel(root)
        result_window.title("Statistical Analysis Results")
        result_window.geometry("500x400")

        result_label = tk.Label(result_window, text="Descriptive Statistics:", font=("Arial", 16, "bold"))
        result_label.pack(pady=10)

        result_text = tk.Text(result_window, wrap=tk.NONE, font=("Courier", 12), height=20, width=60)
        result_text.insert(tk.END, formatted_stats)
        result_text.pack(pady=10, expand=True, fill=tk.BOTH)

        result_text.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(result_window, command=result_text.yview)
        result_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")

root = TkinterDnD.Tk()
root.title("File Upload")
root.geometry("500x400")

label = tk.Label(root, text="Click below to select your file!", wraplength=300)
label.pack(pady=20)

button_file = tk.Button(
    root,
    text="Choose File",
    command=open_file,
    bg='blue',
    fg='white'
)
button_file.pack(expand=True, pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', handle_drop)

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()