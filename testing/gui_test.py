import tkinter as tk

from gui.baseWindow import BaseWindow
from gui.match import CreateMatchDetailsPage, SelectTeamPage
from gui.start import StartWindow

root=tk.Tk()
#StartWindow(root)
SelectTeamPage(root, CreateMatchDetailsPage, "kaushal")
root.mainloop()