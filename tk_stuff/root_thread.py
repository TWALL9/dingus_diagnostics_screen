import tkinter as tk
import threading
import time


# Function to run the Tkinter GUI in a separate thread
def run_gui():
    # Create the main window
    root = tk.Tk()
    root.title("Circular Button")
    root.geometry("300x300")

    # Create a Canvas to draw the circle button
    canvas = tk.Canvas(
        root, width=100, height=100, bg="white", bd=0, highlightthickness=0
    )
    canvas.pack(pady=50)

    # Draw a circular button
    circle_button = canvas.create_oval(10, 10, 90, 90, fill="red", outline="red")

    # Function to handle button click event and color change
    def on_button_click(event):
        # Change the color of the circle when clicked
        current_color = canvas.itemcget(circle_button, "fill")
        new_color = "green" if current_color == "red" else "red"
        canvas.itemconfig(circle_button, fill=new_color)

    # Bind the click event to the circular button
    canvas.tag_bind(circle_button, "<Button-1>", on_button_click)

    # Run the Tkinter main loop
    root.mainloop()


# Function to stop the Tkinter window from another thread
def stop_gui(root):
    time.sleep(5)  # Sleep for a few seconds before closing
    root.quit()  # Close the Tkinter window


# Start Tkinter in its own thread
root_thread = threading.Thread(target=run_gui)
root_thread.start()

# Get the root window instance to be able to stop it from another thread
root_window = tk.Tk()
root_window.after(
    1000, stop_gui, root_window
)  # Use after() to call stop_gui after 1 second

root_thread.join()  # Ensure that the Tkinter thread is joined back to the main thread
