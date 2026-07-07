import tkinter as tk

def press_key(letter):
    """Simulates a key input inside the secure app text box."""
    current = display_var.get()
    
    if letter == "Space":
        display_var.set(current + " ")
    elif letter == "Clear":
        display_var.set("")
    elif letter == "Backspace":
        # Removes the very last character typed
        display_var.set(current[:-1])
    else:
        display_var.set(current + letter)

# Setup Tkinter Window
root = tk.Tk()
root.title("Secure Virtual Keyboard")
root.geometry("650x330")  # Made wider to easily fit a full keyboard layout
root.attributes("-topmost", True) # Keeps the defense tool visible on top

display_var = tk.StringVar()

# Header Warning Label
label = tk.Label(
    root, 
    text="Countermeasure: Virtual Typing Panel\n(Bypasses pynput hooks)", 
    fg="green", 
    font=("Arial", 11, "bold")
)
label.pack(pady=5)

# Visual Display showing your secure text entry
entry = tk.Entry(root, textvariable=display_var, font=("Arial", 14), justify='center', width=45)
entry.pack(pady=10)

# Keyboard Layout Frame
frame = tk.Frame(root)
frame.pack(pady=5)

# Full standard QWERTY keyboard layout broken down by rows
keyboard_rows = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Backspace'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Space', 'Clear']
]

# Build the layout grid row by row
for row_index, row_content in enumerate(keyboard_rows):
    for col_index, btn_text in enumerate(row_content):
        # Using a default argument inside lambda to correctly bind the text value
        action = lambda x=btn_text: press_key(x)
        
        # Style specific action keys differently to look organized
        if btn_text in ["Space", "Clear", "Backspace"]:
            btn = tk.Button(
                frame, 
                text=btn_text, 
                width=10, 
                command=action, 
                bg="#d3d3d3", 
                activebackground="#b8b8b8", 
                font=("Arial", 9, "bold")
            )
        else:
            btn = tk.Button(
                frame, 
                text=btn_text, 
                width=4, 
                height=2, 
                command=action,
                font=("Arial", 10)
            )
            
        btn.grid(row=row_index, column=col_index, padx=3, pady=3)

root.mainloop()
