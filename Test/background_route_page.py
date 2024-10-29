import tkinter as tk
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Page Routing with Background Image")
        self.geometry("800x600")

        self.frames = {}
        for F in (HomePage, PageOne, PageTwo):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='white')

        # Set background image
        self.background_image = ImageTk.PhotoImage(Image.open("Assets/background.jpg"))
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self, text="Home Page", font=("Helvetica", 24))
        label.pack(pady=20)

        button1 = tk.Button(self, text="Go to Page One", command=lambda: parent.show_frame(PageOne))
        button1.pack(pady=10)

        button2 = tk.Button(self, text="Go to Page Two", command=lambda: parent.show_frame(PageTwo))
        button2.pack(pady=10)

class PageOne(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='white')

        # Set background image
        self.background_image = ImageTk.PhotoImage(Image.open("Assets/background.jpg"))
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self, text="Page One", font=("Helvetica", 24))
        label.pack(pady=20)

        button = tk.Button(self, text="Back to Home", command=lambda: parent.show_frame(HomePage))
        button.pack(pady=10)

class PageTwo(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg='white')

        # Set background image
        self.background_image = ImageTk.PhotoImage(Image.open("Assets/background.jpg"))
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        label = tk.Label(self, text="Page Two", font=("Helvetica", 24))
        label.pack(pady=20)

        button = tk.Button(self, text="Back to Home", command=lambda: parent.show_frame(HomePage))
        button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()
