import tkinter as tk
import RPi.GPIO as GPIO # type: ignore

# Set up GPIO mode
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

# Define GPIO pins
gpio_pins = [12, 32]

# Set up pins as output
for pin in gpio_pins:
    GPIO.setup(pin, GPIO.OUT)

# Create a Tkinter window
root = tk.Tk()
root.title("GPIO Control")

# Function to turn on GPIO pins (set 5V output)
def turn_on_gpio(pin):
    GPIO.output(pin, GPIO.HIGH)

# Function to turn off GPIO pins (set 0V output)
def turn_off_gpio(pin):
    GPIO.output(pin, GPIO.LOW)

# Create buttons in Tkinter to control the pins
for i, pin in enumerate(gpio_pins, start=1):
    # Create a frame for each pin's control
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Label for each pin
    label = tk.Label(frame, text=f"GPIO {pin}")
    label.pack(side=tk.LEFT)

    # Button to turn on pin
    on_button = tk.Button(frame, text=f"Turn GPIO {pin} ON", command=lambda p=pin: turn_on_gpio(p))
    on_button.pack(side=tk.LEFT, padx=5)

    # Button to turn off pin
    off_button = tk.Button(frame, text=f"Turn GPIO {pin} OFF", command=lambda p=pin: turn_off_gpio(p))
    off_button.pack(side=tk.LEFT, padx=5)

# Start the Tkinter main loop
root.mainloop()

# Clean up GPIO settings when exiting
GPIO.cleanup()
