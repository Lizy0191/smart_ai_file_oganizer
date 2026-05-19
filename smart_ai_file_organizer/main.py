import tkinter as tk
from organizer import SmartFileOrganizer

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartFileOrganizer(root)

    root.mainloop()