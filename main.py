import tkinter as tk
from tkinter import ttk
from types_editor import TypesEditor
from market_editor import MarketEditor
from market_creator import MarketCreator
from market_bulk_update import MarketEditorBulk
from event_creator import EventCreator  # Import the new EventCreator

class TypesEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Relliks Really Useful DayZ Tool")
         
        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        # Initialize Tabs
        self.types_editor = TypesEditor(self.notebook)
        self.market_editor = MarketEditor(self.notebook)
        self.market_creator_bulk = MarketEditorBulk(self.notebook)
        self.market_creator = MarketCreator(self.notebook)
        self.event_creator = EventCreator(self.notebook)  # Create an instance of EventCreator

        self.notebook.add(self.types_editor.frame, text="Types Editor")
        self.notebook.add(self.market_editor.frame, text="Expansion - Market Editor")
        self.notebook.add(self.market_creator_bulk.frame, text="Market Editor (Bulk)")
        self.notebook.add(self.market_creator.frame, text="Market Creator")
        self.notebook.add(self.event_creator.frame, text="Event Creator")  # Add the new tab

if __name__ == "__main__":
    root = tk.Tk()
    app = TypesEditorApp(root)
    root.mainloop()
