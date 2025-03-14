import tkinter as tk
from tkinter import filedialog, Toplevel
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import messagebox
import pandas as pd #pandas functions TMRW
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

file_data = None

def on_exit():
    print("Application is closing!")
    root.destroy()
    exit()


def open_file():
    filepath = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=(("CSV Files", "*.csv"), ("All files", "*.*"))
    )
    if filepath:
        process_file(filepath)


def process_file(filepath):
    global db_connection
    global db_cursor

    if not filepath.endswith('.csv'):
        print("Provide a valid CSV file.")
        return
    
    try:
        db_connection = sqlite3.connect("data_analysis.db")
        db_cursor = db_connection.cursor()

        with open(filepath, 'r') as file:
            df = pd.read_csv(file)
            df.to_sql("data_table", db_connection, if_exists="replace", index=False)
        
        print("File loaded into SQLite database!")
        print("Sample Data: ", df.head())
        show_graph_window(filepath)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")


def show_graph_window(filepath):
    if not db_cursor:
        print("No data loaded in the database.")
        return

    try:
        graph_window = Toplevel(root)
        graph_window.title(f"Graph Analysis - {filepath.split('/')[-1]}")
        graph_window.geometry("600x500")

        db_cursor.execute("SELECT * FROM data_table")
        rows = db_cursor.fetchall()
        column_names = [description[0] for description in db_cursor.description]

        x_values = [row[0] for row in rows]
        fig, ax = plt.subplots(figsize=(6, 4))
        for i in range(1, len(column_names)):
            y_values = [row[i] for row in rows]
            ax.plot(x_values, y_values, marker='o', linestyle='-', label=column_names[i])

        ax.set_xlabel(column_names[0])
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

    except Exception as e:
        print(f"An error occurred while plotting data: {e}")

def analyze_data():
    try:
        db_cursor.execute("PRAGMA table_info(data_table)")
        columns_info = db_cursor.fetchall()

        numeric_columns = [
            col[1] for col in columns_info if col[2] in ("INTEGER", "REAL")
        ]

        if not numeric_columns:
            print("No numeric columns found for analysis.")
            return

        stats = {}
        for col in numeric_columns:
            db_cursor.execute(
                f"""
                SELECT 
                    AVG({col}) AS avg_value, 
                    MIN({col}) AS min_value, 
                    MAX({col}) AS max_value 
                FROM data_table
                """
            )
            result = db_cursor.fetchone()
            stats[col] = {
                "Average": result[0],
                "Minimum": result[1],
                "Maximum": result[2],
            }

        formatted_stats = "\n".join(
            f"{col:<15} AVG: {values['Average']:.2f} MIN: {values['Minimum']} MAX: {values['Maximum']}"
            for col, values in stats.items()
        )
        print("Summary Statistics: ")
        print(formatted_stats)

        result_window = Toplevel(root)
        result_window.title("Statistical Analysis Results")
        result_window.geometry("1000x800")

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

def download_statistics():
    try:
        filepath = filedialog.asksaveasfilename(
            title="Save Statistics As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        numeric_data = file_data.select_dtypes(include='number')
        stats = numeric_data.describe()

        if filepath.endswith('.csv'):
            stats.to_csv(filepath, index=True)
        else:
            with open(filepath, 'w') as file:
                file.write(stats.to_string(justify="center", float_format="{:.2f}".format))
        
        messagebox.showinfo("Success", f"Statistics successfully saved to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving statistics:\n{e}")


root = TkinterDnD.Tk()
root.title("File Upload")
root.geometry("500x400")

label = tk.Label(root, text="Click below to select your file!", wraplength=300)
label.pack(pady=20)

button_file = tk.Button(
    root,
    text="Choose File",
    command=open_file,
    bg='darkblue',
    fg='white'
)
button_file.pack(expand=True, pady=10)


root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()