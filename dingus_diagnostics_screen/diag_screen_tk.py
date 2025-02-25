from queue import Queue
import tkinter as tk
import threading
import time

import modes

def create_screen(queue: Queue):
    root = tk.Tk()
    root.title("Dingus Diagnostics")
    root.geometry("640x480")

    mode = tk.IntVar(value=modes.Mode.COMP_STATS)

    # Create a Canvas widget to simulate the LCD screen
    lcd_canvas = tk.Canvas(root, width=380, height=180, bg="black", bd=10, relief="sunken")
    lcd_canvas.pack(pady=20)

    # Draw a border to resemble an LCD screen
    lcd_canvas.create_rectangle(30, 30, 380, 180, outline="green", width=3)

    # Add text to simulate the screen display
    lcd_canvas.create_text(190, 90, text="LCD Screen", font=("Courier", 20, "bold"), fill="green")

    # Simulate an LCD-like font with glowing green text
    lcd_canvas.create_text(190, 120, text="Hello, World!", font=("Courier", 16), fill="green")

    # Add a simulated effect by changing text color or adding more text periodically
    def update_display():
        text = ""
        if not queue.empty():
            text = queue.get()
            lcd_canvas.delete("diag")
            text += str(mode.get())
        lcd_canvas.create_text(190, 150, text=text, font=("Courier", 12), fill="light green", tags="diag")
        root.after(100, update_display)

    def change_mode(_event):
        local_mode = mode.get()
        mode.set(modes.next_mode(local_mode))

    button_canvas = tk.Canvas(root, width=200, height=200)
    button_canvas.pack(pady=20)
    circle = button_canvas.create_oval(50, 50, 150, 150, fill="red", outline="black")
    button_canvas.tag_bind(circle, "<Button-1>", change_mode)

    update_display()
    root.mainloop()

def main(args=None):
    queue = Queue()
    t = threading.Thread(target=create_screen, args=[queue])
    t.daemon = True
    t.start()

    while True:
        for i in range(0, 5):
            queue.put(str(i))
            time.sleep(1)


if __name__ == "__main__":
    main()
