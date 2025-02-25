from queue import Queue
import tkinter as tk
import threading
import time

import modes
from utils import get_comp_stats

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

    text = ""
    # Add a simulated effect by changing text color or adding more text periodically
    def update_display(text):
        lcd_canvas.delete("diag")
        if not queue.empty():
            text = queue.get()
            text += str(mode.get())
        
        mode_i = mode.get()
        lcd_text = []
        if mode_i == modes.Mode.COMP_STATS:
            lcd_text = get_comp_stats()
        elif mode_i == modes.Mode.URGENT_DIAGS:
            lcd_text = [text]

        y_pad = 60
        for line in lcd_text:
            lcd_canvas.create_text(190, y_pad, text=line, font=("Courier", 12), fill="light green", tags="diag")
            y_pad += 30

        root.after(100, lambda: update_display(text))

    def change_mode(_event):
        local_mode = mode.get()
        mode.set(modes.next_mode(local_mode))

    button_canvas = tk.Canvas(root, width=200, height=200)
    button_canvas.pack(pady=20)
    circle = button_canvas.create_oval(50, 50, 150, 150, fill="red", outline="black")
    button_canvas.tag_bind(circle, "<Button-1>", change_mode)

    update_display(text)
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
