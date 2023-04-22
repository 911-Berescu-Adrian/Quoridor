from src.ui.console import Console
from src.ui.gui import Gui

user_ui=input("type your ui of choice (1 or 2):\n1. gui\n2. cli\n")
if user_ui=="1":
    g=Gui()
    g.start_screen()
elif user_ui=="2":
    c=Console()
    c.run_console()
