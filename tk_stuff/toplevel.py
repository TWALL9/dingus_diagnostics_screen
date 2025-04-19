import tkinter as tk


def create_new_window():
    # Create a new Toplevel window
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    new_window.geometry("200x150")

    label = tk.Label(new_window, text="This is a new window!", font=("Arial", 12))
    label.pack(pady=30)


# Create the main root window
root = tk.Tk()
root.title("Main Window")
root.geometry("400x200")

# Button to create a new window
button = tk.Button(root, text="Open New Window", command=create_new_window)
button.pack(pady=50)

# Start the main loop
root.mainloop()
