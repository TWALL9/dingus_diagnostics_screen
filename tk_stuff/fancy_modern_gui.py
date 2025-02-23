import tkinter as tk
from tkinter import ttk

# Function to handle button click event
def on_button_click():
    text_box.insert(tk.END, "Button clicked!\n")

# Create the main window
root = tk.Tk()
root.title("Modern Dark Theme with TTK")
root.geometry("400x200")

# Apply dark theme style using ttk
root.tk_setPalette(background="#2e2e2e", foreground="#FFFFFF")  # Background color for window
style = ttk.Style(root)
style.configure("TButton",
                font=("Helvetica", 12),
                padding=10,
                relief="flat",
                background="#FF4C4C",
                foreground="white")
style.map("TButton", background=[("active", "#FF6B6B")])  # Change button color on hover
style.configure("TText", background="#333333", foreground="#FFFFFF", font=("Helvetica", 12), wrap="word")

# Create a square text box on the right side
text_box = tk.Text(root, height=10, width=20, wrap=tk.WORD)
text_box.grid(row=0, column=1, padx=10, pady=10)

# Create a ttk button that looks like a circle
button = ttk.Button(root, text="Click Me", command=on_button_click)
button.grid(row=0, column=0, padx=20, pady=20)

# Apply circular button effect using a canvas
canvas = tk.Canvas(root, width=100, height=100, bg="#2e2e2e", bd=0, highlightthickness=0)
canvas.grid(row=0, column=0)
circle_button = canvas.create_oval(10, 10, 90, 90, fill="#FF4C4C", outline="#FF4C4C")

# Function to simulate button click for circle
def on_circle_button_click(event):
    text_box.insert(tk.END, "Circle Button clicked!\n")

# Bind the button click event to the circle
canvas.tag_bind(circle_button, "<Button-1>", on_circle_button_click)

# Run the main loop
root.mainloop()
