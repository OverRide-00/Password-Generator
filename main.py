import tkinter as tk
from tkinter import filedialog  # Import filedialog
import random
import string
import json
from pathlib import Path
import os
import subprocess  # For opening the directory in the file explorer

# Define the config path
config_path = Path.home() / "Documents" / "password_app_config.json"

# Check if the config file exists, if not, create it with default settings
if not config_path.exists():
    # Default settings
    save_path = str(Path.home() / "Documents" / "Saved Passwords")
    dark_mode = False
    
    # Create default config file
    with open(config_path, "w") as config_file:
        json.dump({"save_path": save_path, "dark_mode": dark_mode}, config_file)
else:
    # Load existing config
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    save_path = config.get("save_path", str(Path.home() / "Documents" / "Saved Passwords"))
    dark_mode = config.get("dark_mode", False)

def save_config():
    # Save the current config (path and dark mode) to the config file
    with open(config_path, "w") as config_file:
        json.dump({"save_path": save_path, "dark_mode": dark_mode}, config_file)

def get_theme_colors():
    if dark_mode:
        return {
            "background_color": "#000000",
            "foreground_color": "#FFFFFF",
            "button_color": "#333333",
            "button_text_color": "#FFFFFF",
            "label_color": "#FFFFFF",
            "spinbox_border_color": "#FFFFFF",
            "error_color": "#FF0000",  # Red for errors
            "normal_text_color": "#FFFFFF"  # White for normal text
        }
    else:
        return {
            "background_color": "#FFFFFF",
            "foreground_color": "#000000",
            "button_color": "#DDDDDD",
            "button_text_color": "#000000",
            "label_color": "#000000",
            "spinbox_border_color": "#000000",
            "error_color": "#FF0000",  # Red for errors
            "normal_text_color": "#000000"  # Black for normal text
        }

def toggle_theme():
    colors = get_theme_colors()
    root.configure(bg=colors["background_color"])
    password.configure(bg=colors["background_color"], fg=colors["normal_text_color"])
    generate.configure(bg=colors["button_color"], fg=colors["button_text_color"])
    save.configure(bg=colors["button_color"], fg=colors["button_text_color"])
    copy.configure(bg=colors["button_color"], fg=colors["button_text_color"])
    divider.configure(bg=colors["foreground_color"])
    password_length_text.configure(bg=colors["background_color"], fg=colors["normal_text_color"])
    password_length.configure(bg=colors["background_color"], fg=colors["normal_text_color"], highlightbackground=colors["spinbox_border_color"])
    upper_latters.configure(bg=colors["background_color"], fg=colors["normal_text_color"], selectcolor=colors["button_color"])
    lower_letters.configure(bg=colors["background_color"], fg=colors["normal_text_color"], selectcolor=colors["button_color"])
    numbers.configure(bg=colors["background_color"], fg=colors["normal_text_color"], selectcolor=colors["button_color"])
    symbols.configure(bg=colors["background_color"], fg=colors["normal_text_color"], selectcolor=colors["button_color"])
    settings.configure(bg=colors["button_color"], fg=colors["button_text_color"])
    password_name_text.configure(bg=colors["background_color"], fg=colors["normal_text_color"])
    password_name.configure(bg=colors["background_color"], fg=colors["normal_text_color"], highlightbackground=colors["spinbox_border_color"])

    # Apply the theme to the settings window if it exists
    if 'settings_window' in globals():
        settings_window.configure(bg=colors["background_color"])
        for widget in settings_window.winfo_children():
            widget.configure(bg=colors["background_color"], fg=colors["normal_text_color"])

def open_settings():
    global settings_window
    settings_window = tk.Toplevel(root)
    settings_window.iconbitmap("icon.ico")
    settings_window.title("Settings")
    settings_window.geometry("600x150")
    colors = get_theme_colors()
    settings_window.configure(bg=colors["background_color"])

    theme_var = tk.BooleanVar(value=dark_mode)
    theme_toggle = tk.Checkbutton(
        settings_window, 
        text="Dark Mode", 
        variable=theme_var, 
        bg=colors["background_color"], 
        fg=colors["normal_text_color"]
    )
    theme_toggle.grid(row=0, column=0, columnspan=2, pady=(20, 5), sticky="w")

    # Path input field and text
    path_text = tk.Label(
        settings_window, 
        text="Path:", 
        bg=colors["background_color"], 
        fg=colors["normal_text_color"]
    )
    path_input = tk.Entry(settings_window, width=40)
    path_input.insert(0, save_path)  # Load the current save_path from the config

    path_text.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="e")
    path_input.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")

    browse_button = tk.Button(
        settings_window, 
        text="Browse", 
        command=lambda: browse_folder(path_input),
        bg=colors["button_color"],
        fg=colors["button_text_color"]
    )
    browse_button.grid(row=1, column=2, padx=(5, 10), pady=(0, 10))

    view_button = tk.Button(
        settings_window, 
        text="View", 
        command=lambda: view_folder(),
        bg=colors["button_color"],
        fg=colors["button_text_color"]
    )
    view_button.grid(row=1, column=3, padx=(5, 10), pady=(0, 10))

    # Apply button
    apply_button = tk.Button(
        settings_window, 
        text="Apply", 
        command=lambda: apply_theme_and_save(theme_var.get(), path_input.get()),
        bg=colors["button_color"],
        fg=colors["button_text_color"]
    )
    apply_button.grid(row=2, column=0, columnspan=4, pady=10, sticky="e")

def browse_folder(path_input):
    folder_selected = filedialog.askdirectory()  # Use the imported filedialog
    if folder_selected:
        path_input.delete(0, tk.END)
        path_input.insert(0, folder_selected)

def view_folder():
    if os.path.exists(save_path):
        subprocess.run(['explorer', save_path])
    else:
        tk.messagebox.showerror("Error", "The path does not exist!")

def apply_theme_and_save(dark_mode_setting, new_path):
    global dark_mode, save_path  # Declare global variables at the start
    dark_mode = dark_mode_setting
    save_path = new_path

    # Update the theme and save the new config
    toggle_theme()
    save_config()

def on_generate():
    global generated_password  # Declare global variable to store password
    length = int(password_length.get())
    characters = ""
    
    if upper_latters_var.get():
        characters += string.ascii_uppercase
    if lower_letters_var.get():
        characters += string.ascii_lowercase
    if numbers_var.get():
        characters += string.digits
    if symbols_var.get():
        characters += string.punctuation

    if characters:
        generated_password = ''.join(random.choice(characters) for _ in range(length))
        colors = get_theme_colors()
        password.config(text=generated_password, fg=colors["normal_text_color"])  # Set text color based on theme
    else:
        colors = get_theme_colors()
        password.config(text="Select at least one option", fg=colors["error_color"])  # Red for error messages

def save_password():
    if not generated_password:
        colors = get_theme_colors()
        password.config(text="Generate a password first", fg=colors["error_color"])  # Red for error messages
        return

    name = password_name.get()
    if not name.strip():
        colors = get_theme_colors()
        password.config(text="Enter a password name", fg=colors["error_color"])  # Red for error messages
        return

    if not os.path.exists(save_path):
        colors = get_theme_colors()
        password.config(text="Path does not exist!", fg=colors["error_color"])  # Red for path error messages
        return

    file_path = Path(save_path) / f"{name}.txt"
    with open(file_path, "w") as file:
        file.write(generated_password)
    colors = get_theme_colors()
    password.config(text=f"Password saves Succsesfully!", fg="#00FF00")  # Normal text color

def copy_to_clipboard():
    if not generated_password:
        colors = get_theme_colors()
        password.config(text="Generate a password first", fg=colors["error_color"])  # Red for error messages
        return
    else:
        root.clipboard_clear()
        root.clipboard_append(password.cget("text"))
        root.update()
        # Update the label text to confirm the action
        password.config(text="Password Copied to Clipboard!", fg="#00FF00")

root = tk.Tk()
root.title("Password Generator")
root.iconbitmap("icon.ico")

# Create widgets
settings = tk.Button(root, text=" ⁝ ", bg="#333333", fg="#FFFFFF", command=open_settings)
generate = tk.Button(
    root, 
    text="GENERATE", 
    command=on_generate, 
    font=("Helvetica", 14, "bold"),  # Set font to bold and larger size
    bg="#DDDDDD", 
    fg="#000000", 
    padx=10,  # Add padding to make it larger
    pady=5
)
password = tk.Label(
    root, 
    text="Click it!!!",  
    font=("Helvetica", 11, "bold"),  # Set font to bold and larger size
    bg="#DDDDDD", 
    fg="#000000", 
    padx=10,  # Add padding to make it larger
    pady=5
)
save = tk.Button(root, text="Save", command=save_password)
copy = tk.Button(root, text="Copy", command=copy_to_clipboard)
divider = tk.Canvas(root, height=2, bd=0, highlightthickness=0)
password_name_text = tk.Label(root, text="Password Name: ")
password_name = tk.Entry(root)
password_length_text = tk.Label(root, text="Password Length: ")
password_length = tk.Spinbox(root, from_=1, to=100, width=15, highlightthickness=1, bd=1, relief="solid")
password_length.delete(0, "end")
password_length.insert(0, 10)  # Set default length to 10
upper_latters_var = tk.BooleanVar(value=True)
lower_letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
upper_latters = tk.Checkbutton(root, text="UPPERCASE LETTERS", variable=upper_latters_var)
lower_letters = tk.Checkbutton(root, text="LOWERCASE LETTERS", variable=lower_letters_var)
numbers = tk.Checkbutton(root, text="NUMBERS", variable=numbers_var)
symbols = tk.Checkbutton(root, text="SYMBOLS", variable=symbols_var)

# Layout widgets
settings.grid(row=0, column=0, sticky="w", pady=(0, 5))
generate.grid(row=1, column=0, columnspan=2, sticky="ew")
password.grid(row=2, column=0, columnspan=2, sticky="ew")
save.grid(row=3, column=0, sticky="e", padx=(0, 5))
copy.grid(row=3, column=1, sticky="w", padx=(5, 0))
divider.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(5, 5))
password_name_text.grid(row=5, column=0, sticky="e")
password_name.grid(row=5, column=1, sticky="w", pady=(3, 3))
password_length_text.grid(row=6, column=0, sticky="e")
password_length.grid(row=6, column=1, sticky="w")
upper_latters.grid(row=8, column=0, columnspan=2, sticky="ew")
lower_letters.grid(row=9, column=0, columnspan=2, sticky="ew")
numbers.grid(row=10, column=0, columnspan=2, sticky="ew")
symbols.grid(row=11, column=0, columnspan=2, sticky="ew")

# Initialize the global variable
generated_password = None

# Apply the initial theme based on the config file
toggle_theme()

root.mainloop()
