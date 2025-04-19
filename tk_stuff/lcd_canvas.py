import tkinter as tk


def create_lcd_screen():
    # Create the main window
    root = tk.Tk()
    root.title("LCD Screen Simulation")
    root.geometry("400x200")  # Set window size to resemble a small LCD screen

    # Create a Canvas widget to simulate the LCD screen
    lcd_canvas = tk.Canvas(
        root, width=380, height=180, bg="black", bd=10, relief="sunken"
    )
    lcd_canvas.pack(pady=20)

    # Draw a border to resemble an LCD screen
    lcd_canvas.create_rectangle(0, 0, 380, 180, outline="green", width=3)

    # Add text to simulate the screen display
    lcd_canvas.create_text(
        190, 90, text="LCD Screen", font=("Courier", 20, "bold"), fill="green"
    )

    # Simulate an LCD-like font with glowing green text
    lcd_canvas.create_text(
        190, 120, text="Hello, World!", font=("Courier", 16), fill="green"
    )

    # Add a simulated effect by changing text color or adding more text periodically
    def update_display():
        lcd_canvas.create_text(
            190, 150, text="Updating...", font=("Courier", 12), fill="light green"
        )
        root.after(
            1000,
            lambda: lcd_canvas.create_text(
                190, 150, text="Updating...", font=("Courier", 12), fill="green"
            ),
        )

    root.after(2000, update_display)

    # Start the Tkinter main loop
    root.mainloop()


# Run the function to create the LCD screen simulation
create_lcd_screen()
