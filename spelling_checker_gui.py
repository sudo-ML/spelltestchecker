import os
import tkinter as tk
from tkinter import filedialog, messagebox

def load_words_from_file(filepath):
    """Load words from a .txt file, one word per line, into a set."""
    with open(filepath, 'r') as file:
        words = set(line.strip().lower() for line in file if line.strip())
    return words

def find_repeated_words(new_words, past_files):
    """Compare words in the new list with all past lists in the folder."""
    repeated_words = {}
    for filename in past_files:
        past_words = load_words_from_file(filename)
        # Find intersection of new words with this past file's words
        common_words = new_words.intersection(past_words)
        if common_words:
            repeated_words[filename] = common_words
    return repeated_words

def check_repeated_words():
    # Verify new_words.txt exists in the selected folder
    new_words_file = os.path.join(folder_path.get(), 'new_words.txt')
    if not os.path.isfile(new_words_file):
        messagebox.showerror("Error", "'new_words.txt' not found in the selected folder.")
        return
    
    # Load words from new_words.txt
    new_words = load_words_from_file(new_words_file)
    
    # Get list of past files (all other .txt files excluding new_words.txt)
    past_files = [os.path.join(folder_path.get(), f) 
                  for f in os.listdir(folder_path.get()) 
                  if f.endswith('.txt') and f != 'new_words.txt']
    
    if not past_files:
        messagebox.showinfo("Info", "No past .txt files found in the selected folder.")
        return
    
    # Find repeated words across past lists
    repeated_words = find_repeated_words(new_words, past_files)
    
    # Display results
    result_text.delete(1.0, tk.END)  # Clear previous results
    if repeated_words:
        result_text.insert(tk.END, "Repeated words found:\n")
        for filename, words in repeated_words.items():
            result_text.insert(tk.END, f"In {os.path.basename(filename)}: {', '.join(words)}\n")
    else:
        result_text.insert(tk.END, "No repeated words found.")

def select_folder():
    path = filedialog.askdirectory()
    if path:
        folder_path.set(path)

# GUI setup
app = tk.Tk()
app.title("Spelling Bear Checker By Matt L v0.5")

folder_path = tk.StringVar()



# Folder selection section
warning_label = tk.Label(app, text="Warning: The new word list must be named new_words.txt and be placed in the same folder!", fg="red")
warning_label.pack(pady=5)
folder_label = tk.Label(app, text="Select folder containing old spelling bear lists and new_words.txt:")
folder_label.pack(pady=5)
folder_button = tk.Button(app, text="Browse", command=select_folder)
folder_button.pack(pady=5)

# Run check button
check_button = tk.Button(app, text="Check for Repeated Words", command=check_repeated_words)
check_button.pack(pady=10)

# Results display
result_text = tk.Text(app, width=50, height=15)
result_text.pack(pady=5)

# Add default text that will be replaced once the check is run
result_text.insert(tk.END, "Results will appear here...\n")

# Start the application
app.mainloop()
