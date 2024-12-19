import pandas as pd
import matplotlib.pyplot as plt 

def process_file(filepath):
    """
    Process the given file and generate a graph if it's a valid CSV.
    """
    if not filepath.endswith('.csv'):
        print("Please provide a valid CSV file.")
        return

    try:
        data = pd.read_csv(filepath)
        print("File loaded successfully!")
        print(data.head())  

        if len(data.columns) >= 2:
            for i in range(1, len(data.columns)):
                plt.plot(data.iloc[:, 0], data.iloc[:, i], marker='o', linestyle='-', label=data.columns[i])
            
            plt.xlabel(data.columns[0])
            plt.ylabel('Value')
            plt.title("Line Graph with Multiple Columns")
            plt.legend()
            plt.show()
        else:
            print("CSV file does not have enough columns to plot.")
    except Exception as e:
        print(f"An error occurred: {e}")
