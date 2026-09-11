import tkinter as tk
from login import LoginPage


root = tk.Tk()

root.title("Gola - Your Digital Closet")
root.geometry("1000x650")
root.resizable(False, False)

LoginPage(root)

root.mainloop()