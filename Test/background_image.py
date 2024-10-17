import tkinter as tk
from PIL import Image, ImageTk

class BackgroundWindow(tk.Tk):
    def __init__(self, image_path, width=800, height=600):
        super().__init__()
        self.geometry(f"{width}x{height}")
        self.title("Tkinter Window with Resizable Background Image")

        # Load the image
        self.original_image = Image.open(image_path)

        # Create a frame with a custom background color
        self.main_frame = tk.Frame(self, bg="lightblue")
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create a label to display the background image inside the frame
        self.background_label = tk.Label(self.main_frame)
        self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Bind the window resizing event
        self.bind("<Configure>", self.resize_background)

    def resize_background(self, event=None):
        # Get the current window dimensions
        width = self.winfo_width()
        height = self.winfo_height()

        # Resize the image to fit the current window size
        resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)

        # Convert the resized image to ImageTk format
        self.tk_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the new image
        self.background_label.config(image=self.tk_image)

# Usage
if __name__ == "__main__":
    app = BackgroundWindow("Assets/test-background.png", 800, 600)
    app.mainloop()
