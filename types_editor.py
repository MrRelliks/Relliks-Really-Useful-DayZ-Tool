import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar
import xml.etree.ElementTree as ET
import json

class TypesEditor:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.xml_data = None
        self.type_names = []  # To store type names for selection

        self.create_ui()

    def create_ui(self):
        # UI Elements for Types Editor
        self.load_button = tk.Button(self.frame, text="Load XML File", command=self.load_xml)
        self.load_button.pack(pady=10)

        self.search_entry = tk.Entry(self.frame)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.frame, text="Search Types", command=self.search_types)
        self.search_button.pack(pady=5)

        self.type_listbox = Listbox(self.frame, height=10, width=50, selectmode=tk.MULTIPLE)  # Enable multiple selection
        self.type_listbox.pack(pady=10)

        # Scrollbar for the listbox
        self.scrollbar = Scrollbar(self.frame, command=self.type_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.type_listbox.config(yscrollcommand=self.scrollbar.set)

        self.create_market_button = tk.Button(self.frame, text="Create Market JSON", command=self.create_market_json)
        self.create_market_button.pack(pady=10)

        self.nominal_label = tk.Label(self.frame, text="Value to Adjust Nominal by:")
        self.nominal_label.pack()

        self.nominal_entry = tk.Entry(self.frame)
        self.nominal_entry.pack(pady=5)

        self.min_label = tk.Label(self.frame, text="Value to Adjust Min by:")
        self.min_label.pack()

        self.min_entry = tk.Entry(self.frame)
        self.min_entry.pack(pady=5)

        # Button to adjust both nominal and min values
        self.adjust_both_button = tk.Button(self.frame, text="Adjust Both Nominal and Min", command=self.adjust_both)
        self.adjust_both_button.pack(pady=10)

    def load_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not file_path:
            return

        try:
            self.xml_data = ET.parse(file_path)
            self.type_names = [elem.get('name') for elem in self.xml_data.findall('.//type')]
            self.type_listbox.delete(0, tk.END)  # Clear previous entries
            for name in self.type_names:
                self.type_listbox.insert(tk.END, name)  # Populate the listbox
            messagebox.showinfo("Success", "XML File Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading XML file: {e}")

    def search_types(self):
        search_term = self.search_entry.get().strip().lower()
        self.type_listbox.delete(0, tk.END)  # Clear previous entries
        for name in self.type_names:
            if search_term in name.lower():
                self.type_listbox.insert(tk.END, name)  # Insert matching names

    def create_market_json(self):
        selected_indices = self.type_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Warning", "Please select at least one type name.")
            return

        # Gather selected type names
        selected_types = [self.type_listbox.get(i) for i in selected_indices]

        # Base market data structure
        market_data = {
            "m_Version": 12,
            "DisplayName": "Market Data",
            "Icon": "Deliver",
            "Color": "FBFCFEFF",
            "IsExchange": 0,
            "InitStockPercent": 75.0,
            "Items": []
        }

        # For simplicity, using default price thresholds
        max_price_threshold = 930
        min_price_threshold = 930

        # Create items for the market JSON
        for item in selected_types:
            market_data["Items"].append({
                "ClassName": item,
                "MaxPriceThreshold": max_price_threshold,
                "MinPriceThreshold": min_price_threshold,
                "SellPricePercent": -1,
                "MaxStockThreshold": 100,
                "MinStockThreshold": 100,
                "QuantityPercent": -1,
                "SpawnAttachments": [],
                "Variants": []
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

    def adjust_both(self):
        if self.xml_data is None:
            messagebox.showwarning("Warning", "Please load an XML file first.")
            return

        try:
            nominal_adjustment = int(self.nominal_entry.get())  # Convert input to integer
            min_adjustment = int(self.min_entry.get())  # Convert input to integer
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for both nominal and min.")
            return

        for elem in self.xml_data.findall('.//type'):
            nominal_node = elem.find('nominal')
            min_node = elem.find('min')
            if nominal_node is not None:
                original_nominal = int(nominal_node.text)
                new_nominal = max(0, original_nominal + nominal_adjustment)  # Ensure non-negative
                nominal_node.text = str(new_nominal)  # Update the nominal value

            if min_node is not None:
                original_min = int(min_node.text)
                new_min = max(0, original_min + min_adjustment)  # Ensure non-negative
                min_node.text = str(new_min)  # Update the min value

        # Ask user for the file path to save the modified XML
        save_path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
        if not save_path:
            return

        try:
            self.xml_data.write(save_path)
            messagebox.showinfo("Success", "XML File Saved Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving XML file: {e}")

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Types Editor")
    types_editor = TypesEditor(root)
    types_editor.frame.pack()
    root.mainloop()
