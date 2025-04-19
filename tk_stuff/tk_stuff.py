import tkinter as tk


def clear_section():
    # Clear specific shapes by item ID
    canvas.delete(rect)  # Removes the rectangle

    # Optionally, clear everything within a bounding box
    canvas.delete("section")  # Removes items with the tag "section"


def draw_shapes():
    # Create a rectangle (item ID returned)
    global rect
    rect = canvas.create_rectangle(50, 50, 200, 150, fill="blue", tags="section")

    # Create other shapes to demonstrate deletion
    canvas.create_oval(100, 100, 300, 200, fill="green", tags="section")
    canvas.create_text(150, 200, text="Hello", tags="section")


# Set up the root window
root = tk.Tk()
root.title("Clear Section Example")

# Create the canvas widget
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Draw shapes
draw_shapes()

# Button to clear section
clear_button = tk.Button(root, text="Clear Section", command=clear_section)
clear_button.pack()

# Start the Tkinter main loop
root.mainloop()
