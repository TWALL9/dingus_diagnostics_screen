import tkinter as tk

# Function to handle button click event
def on_button_click(event):
    # Change the color of the circle when clicked
    current_color = canvas.itemcget(circle_button, "fill")
    new_color = "green" if current_color == "red" else "red"
    canvas.itemconfig(circle_button, fill=new_color)

# Create the main window
root = tk.Tk()
root.title("Circular Button")
root.geometry("300x300")

# Create a Canvas to draw the circle button
canvas = tk.Canvas(root, width=100, height=100, bg="white", bd=0, highlightthickness=0)
canvas.pack(pady=50)

# Draw a circular button
circle_button = canvas.create_oval(10, 10, 90, 90, fill="red", outline="red")

# Bind the click event to the circular button
canvas.tag_bind(circle_button, "<Button-1>", on_button_click)

# Run the main loop
root.mainloop()
