# gui_utils.py

import os
import shutil
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry

def create_date_range_file_sorter(parent, bg_color, fg_color):
    """
    Creates a frame that allows the user to:
      - Select a date range
      - Select a directory
      - Display files within the date range
    """
    frame = tk.Frame(parent, bg=bg_color)
    frame.pack(pady=10, fill="x", padx=10)

    selected_directory = {"path": None}

    def select_directory():
        dir_path = filedialog.askdirectory(title="Select a Directory")
        if dir_path:
            selected_directory["path"] = dir_path
            directory_label.config(text=f"Selected Directory: {dir_path}")
            result_text.delete('1.0', tk.END)
        else:
            directory_label.config(text="No directory selected.")
            result_text.delete('1.0', tk.END)

    # Date Range Selection
    tk.Label(frame, text="Start Date:", bg=bg_color, fg=fg_color).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    start_date_entry = DateEntry(frame, width=12, background="darkblue", foreground="white",
                                 borderwidth=2, date_pattern="y-mm-dd")
    start_date_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="End Date:", bg=bg_color, fg=fg_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    end_date_entry = DateEntry(frame, width=12, background="darkblue", foreground="white",
                               borderwidth=2, date_pattern="y-mm-dd")
    end_date_entry.grid(row=1, column=1, padx=5, pady=5)

    # Directory Selection
    select_dir_button = tk.Button(frame, text="Select Directory", command=select_directory,
                                  bg=bg_color, fg=fg_color)
    select_dir_button.grid(row=2, column=0, columnspan=2, pady=5)

    directory_label = tk.Label(frame, text="No directory selected.", bg=bg_color, fg=fg_color)
    directory_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Text widget to display results
    result_text = tk.Text(frame, height=10, bg=bg_color, fg=fg_color)
    result_text.grid(row=6, column=0, columnspan=2, pady=5, sticky="we")

    # Function to filter files by date range
    def filter_files_by_date():
        result_text.delete('1.0', tk.END)

        dir_selected = selected_directory["path"]
        if not dir_selected:
            messagebox.showwarning("No Directory Selected", "Please select a directory first.")
            return

        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()

        files_found = []
        for item in os.listdir(dir_selected):
            full_path = os.path.join(dir_selected, item)
            if os.path.isfile(full_path):
                mod_timestamp = os.path.getmtime(full_path)
                mod_date = datetime.datetime.fromtimestamp(mod_timestamp).date()
                if start_date <= mod_date <= end_date:
                    files_found.append((item, mod_date))

        if files_found:
            files_found.sort(key=lambda x: x[1])
            result_text.insert(tk.END, "Files within date range:\n")
            for f, d in files_found:
                result_text.insert(tk.END, f"{f} - {d}\n")
        else:
            result_text.insert(tk.END, "No files found in the selected date range.\n")

    # Button to trigger filtering
    filter_button = tk.Button(frame, text="Filter Files by Date", command=filter_files_by_date,
                              bg=bg_color, fg=fg_color)
    filter_button.grid(row=4, column=0, columnspan=2, pady=10)

    return frame

def create_file_sorter_by_extension(parent, bg_color, fg_color):
    """
    Creates a frame that allows the user to:
      - Select a directory
      - Sort files in the directory by their file extensions
      - Display sorting results
    """
    frame = tk.Frame(parent, bg=bg_color)
    frame.pack(pady=10, fill="x", padx=10)

    selected_directory = {"path": None}

    def select_directory():
        dir_path = filedialog.askdirectory(title="Select a Directory")
        if dir_path:
            selected_directory["path"] = dir_path
            directory_label.config(text=f"Selected Directory: {dir_path}")
            result_text.delete('1.0', tk.END)
        else:
            directory_label.config(text="No directory selected.")
            result_text.delete('1.0', tk.END)

    # Directory selection button and label
    select_dir_button = tk.Button(
        frame, text="Select Directory",
        command=select_directory, bg=bg_color, fg=fg_color
    )
    select_dir_button.pack(pady=5)

    directory_label = tk.Label(frame, text="No directory selected.", bg=bg_color, fg=fg_color)
    directory_label.pack(pady=5)

    # Text widget to display results
    result_text = tk.Text(frame, height=10, bg=bg_color, fg=fg_color)
    result_text.pack(fill="both", expand=True, padx=5, pady=5)

    # Function to sort files by extension
    def sort_files():
        dir_path = selected_directory["path"]
        if not dir_path:
            messagebox.showwarning("No Directory Selected", "Please select a directory first.")
            return

        files_moved = 0
        errors = 0

        try:
            # Iterate over items in the directory
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if os.path.isfile(item_path):
                    # Get file extension
                    _, extension = os.path.splitext(item)
                    extension = extension[1:].lower()  # Remove dot and convert to lowercase
                    if not extension:
                        extension = "no_extension"

                    # Create directory for the extension if it doesn't exist
                    new_dir = os.path.join(dir_path, extension)
                    os.makedirs(new_dir, exist_ok=True)

                    # Move file to the new directory
                    new_path = os.path.join(new_dir, item)
                    try:
                        shutil.move(item_path, new_path)
                        result_text.insert(tk.END, f"Moved: {item} -> {extension}/\n")
                        files_moved += 1
                    except Exception as move_error:
                        result_text.insert(tk.END, f"Error moving {item}: {move_error}\n")
                        errors += 1

            result_text.insert(tk.END, f"\nOperation completed. Files moved: {files_moved}. Errors: {errors}.\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Sort Files button
    sort_button = tk.Button(
        frame, text="Sort Files by Extension",
        command=sort_files, bg=bg_color, fg=fg_color
    )
    sort_button.pack(pady=10)

    return frame
