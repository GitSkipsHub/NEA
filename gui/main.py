import tkinter as tk

from gui.start import StartWindow

def main():
    root = tk.Tk()
    StartWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
