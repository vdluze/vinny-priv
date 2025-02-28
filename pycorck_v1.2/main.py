# main.py

import tkinter as tk
from petergui import (
    create_date_range_file_sorter,
    create_file_sorter_by_extension
)

def main():
    # Create the main window and set initial theme.
    root = tk.Tk()
    root.title("File Management Tool")
    root.geometry("600x800")

    # Theme definitions
    dark_bg = "#2E2E2E"    # dark background
    dark_fg = "#F2F2F2"    # light text
    light_bg = "#FFFFFF"   # white background
    light_fg = "#000000"   # dark text

    # Start in dark theme
    current_theme = {"mode": "dark", "bg": dark_bg, "fg": dark_fg}
    root.config(bg=current_theme["bg"])

    # Dictionary to hold frames
    frames = {}

    def create_frames():
        # Remove existing frames (if any)
        for frame in frames.values():
            frame.destroy()

        # Create frames with updated theme
        tk.Label(root, text="Date Range File Filter", bg=current_theme["bg"],
                 fg=current_theme["fg"], font=("Helvetica", 16, "bold")).pack(pady=10)
        frames["date_filter"] = create_date_range_file_sorter(
            root, current_theme["bg"], current_theme["fg"]
        )

        tk.Label(root, text="File Extension Sorter", bg=current_theme["bg"],
                 fg=current_theme["fg"], font=("Helvetica", 16, "bold")).pack(pady=10)
        frames["extension_sorter"] = create_file_sorter_by_extension(
            root, current_theme["bg"], current_theme["fg"]
        )

    def toggle_theme():
        # Toggle theme
        if current_theme["mode"] == "dark":
            current_theme.update({"mode": "light", "bg": light_bg, "fg": light_fg})
        else:
            current_theme.update({"mode": "dark", "bg": dark_bg, "fg": dark_fg})

        root.config(bg=current_theme["bg"])
        create_frames()
        # Update toggle button color
        toggle_button.config(bg=current_theme["bg"], fg=current_theme["fg"])

    # Initial creation of frames
    create_frames()

    # Toggle Theme button
    toggle_button = tk.Button(
        root, text="Toggle Theme",
        command=toggle_theme,
        bg=current_theme["bg"], fg=current_theme["fg"]
    )
    toggle_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
