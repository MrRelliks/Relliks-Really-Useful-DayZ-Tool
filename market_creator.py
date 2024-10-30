import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
import json
import xml.etree.ElementTree as ET

class MarketCreator:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.create_ui()
        self.items = []  # To store items from the XML

    def create_ui(self):
        # Button to load XML
        self.load_button = tk.Button(self.frame, text="Load XML File", command=self.load_xml)
        self.load_button.pack(pady=10)

        # Entry fields for item properties
        self.display_name_entry = tk.Entry(self.frame, width=50)
        self.display_name_entry.pack(pady=5)
        self.display_name_entry.insert(0, "Display Name")

        self.initial_stock_percent_entry = tk.Entry(self.frame, width=50)
        self.initial_stock_percent_entry.pack(pady=5)
        self.initial_stock_percent_entry.insert(0, "Initial Stock Percent (default 75.0)")

        # New entry fields for price thresholds
        self.max_price_threshold_entry = tk.Entry(self.frame, width=50)
        self.max_price_threshold_entry.pack(pady=5)
        self.max_price_threshold_entry.insert(0, "Max Price Threshold (default 930)")

        self.min_price_threshold_entry = tk.Entry(self.frame, width=50)
        self.min_price_threshold_entry.pack(pady=5)
        self.min_price_threshold_entry.insert(0, "Min Price Threshold (default 930)")

        # Button to create Market JSON
        self.create_button = tk.Button(self.frame, text="Create Market JSON", command=self.create_market_json)
        self.create_button.pack(pady=10)

        # Listbox to display loaded items
        self.item_listbox = Listbox(self.frame, height=10, width=50, selectmode=tk.MULTIPLE)  # Changed to MULTIPLE
        self.item_listbox.pack(pady=10)

        # Scrollbar for the listbox
        self.scrollbar = Scrollbar(self.frame, command=self.item_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.item_listbox.config(yscrollcommand=self.scrollbar.set)

        # Button to remove selected items
        self.remove_button = tk.Button(self.frame, text="Remove Selected", command=self.remove_selected)
        self.remove_button.pack(pady=5)

    def load_xml(self):
        # Load XML file
        xml_file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not xml_file_path:
            return

        try:
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            self.items.clear()  # Clear previous items
            self.item_listbox.delete(0, tk.END)  # Clear the listbox

            # Look for type elements and get the name attribute
            for item in root.findall('type'):  # Directly search for type elements
                class_name = item.get('name')  # Get the name attribute
                if class_name:  # Only append if class_name is not None
                    self.items.append(class_name)
                    self.item_listbox.insert(tk.END, class_name)  # Add to listbox

            messagebox.showinfo("Success", f"Loaded {len(self.items)} items from XML.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading XML file: {e}")

    def remove_selected(self):
        # Remove selected items from the listbox and internal items list
        selected_indices = self.item_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "No items selected to remove.")
            return

        # Store selected items to remove
        items_to_remove = [self.item_listbox.get(i) for i in selected_indices]

        for item in items_to_remove:
            self.items.remove(item)  # Remove from internal list
            self.item_listbox.delete(self.item_listbox.get(0, tk.END).index(item))  # Remove from listbox

        messagebox.showinfo("Success", f"Removed {len(items_to_remove)} items from the list.")

    def create_market_json(self):
        # Base market data structure
        market_data = {
            "m_Version": 12,
            "DisplayName": self.display_name_entry.get(),
            "Icon": "Deliver",  # Default value
            "Color": "FBFCFEFF",  # Default value
            "IsExchange": 0,  # Default value
            "InitStockPercent": float(self.initial_stock_percent_entry.get() or 75.0),  # Default to 75 if not provided
            "Items": []
        }

        # Get user-defined price thresholds
        max_price_threshold = float(self.max_price_threshold_entry.get() or 930)  # Default to 930 if not provided
        min_price_threshold = float(self.min_price_threshold_entry.get() or 930)  # Default to 930 if not provided

        # Iterate over loaded items to create the Items list in the JSON
        for item in self.items:
            market_data["Items"].append({
                "ClassName": item,
                "MaxPriceThreshold": max_price_threshold,
                "MinPriceThreshold": min_price_threshold,
                "SellPricePercent": -1,  # Default value
                "MaxStockThreshold": 100,  # Default value
                "MinStockThreshold": 100,  # Default value
                "QuantityPercent": -1,  # Default value
                "SpawnAttachments": [],  # Default value
                "Variants": []  # This can be populated based on additional logic if needed
            })

        # Save to JSON file
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, 'w') as json_file:
                json.dump(market_data, json_file, indent=4)
            messagebox.showinfo("Success", "Market JSON Created Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving JSON file: {e}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Market Creator")
    market_creator = MarketCreator(root)
    market_creator.frame.pack()
    root.mainloop()
