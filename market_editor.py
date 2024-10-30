import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json

class MarketEditor:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.json_data = None
        self.create_ui()

    def create_ui(self):
        # UI Elements for Expansion Market Editor
        self.load_json_button = tk.Button(self.frame, text="Load JSON File", command=self.load_json)
        self.load_json_button.pack(pady=10)

        self.items_frame = tk.Frame(self.frame)
        self.items_frame.pack(pady=10)

        self.edit_button = tk.Button(self.frame, text="Edit Selected Item", command=self.edit_selected_item)
        self.edit_button.pack(pady=5)

        self.bulk_edit_button = tk.Button(self.frame, text="Bulk Edit", command=self.bulk_edit)
        self.bulk_edit_button.pack(pady=5)

        self.output_text_market = tk.Text(self.frame, height=15, width=50)
        self.output_text_market.pack(pady=10)

        self.items_listbox = tk.Listbox(self.items_frame, width=50, height=10)
        self.items_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.items_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.items_listbox.yview)

        # Bind selection change event to update the preview
        self.items_listbox.bind('<<ListboxSelect>>', self.on_item_select)

        # Additional Buttons for Market Editor
        self.adjust_price_button = tk.Button(self.frame, text="Adjust Prices by Percentage", command=self.adjust_prices)
        self.adjust_price_button.pack(pady=5)

        self.apply_max_to_min_button = tk.Button(self.frame, text="Apply Max to Min", command=self.apply_max_to_min)
        self.apply_max_to_min_button.pack(pady=5)

        

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, 'r') as json_file:
                self.json_data = json.load(json_file)
            self.populate_items_list()
            messagebox.showinfo("Success", "JSON File Loaded Successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading JSON file: {e}")

    def populate_items_list(self):
        self.items_listbox.delete(0, tk.END)  # Clear previous items
        if "Items" in self.json_data:
            for item in self.json_data["Items"]:
                self.items_listbox.insert(tk.END, item["ClassName"])
        self.update_output_preview()  # Show the full JSON data on load

    def update_output_preview(self):
        if self.json_data:
            self.output_text_market.delete(1.0, tk.END)  # Clear the text area
            if self.items_listbox.curselection():  # If an item is selected
                selected_index = self.items_listbox.curselection()[0]
                item_name = self.items_listbox.get(selected_index)
                for item in self.json_data["Items"]:
                    if item["ClassName"] == item_name:
                        self.output_text_market.insert(tk.END, json.dumps(item, indent=4))
                        return
            else:  # No item selected, show the entire JSON
                self.output_text_market.insert(tk.END, json.dumps(self.json_data, indent=4))

    def on_item_select(self, event):
        self.update_output_preview()  # Update preview when an item is selected

    def edit_selected_item(self):
        selected_index = self.items_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select an item to edit.")
            return

        item_name = self.items_listbox.get(selected_index)
        for item in self.json_data["Items"]:
            if item["ClassName"] == item_name:
                new_max_price = simpledialog.askfloat("Edit Max Price", "Enter new Max Price:", initialvalue=item["MaxPriceThreshold"])
                new_min_price = simpledialog.askfloat("Edit Min Price", "Enter new Min Price:", initialvalue=item["MinPriceThreshold"])

                if new_max_price is not None:
                    item["MaxPriceThreshold"] = new_max_price

                if new_min_price is not None:
                    item["MinPriceThreshold"] = new_min_price

                messagebox.showinfo("Success", "Item edited successfully!")
                self.populate_items_list()  # Refresh the list
                return

    def bulk_edit(self):
        percentage = simpledialog.askfloat("Bulk Edit", "Enter percentage to adjust prices:")
        if percentage is None:
            return

        for item in self.json_data["Items"]:
            item["MaxPriceThreshold"] = round(item["MaxPriceThreshold"] * (1 + percentage / 100.0))
            item["MinPriceThreshold"] = round(item["MinPriceThreshold"] * (1 + percentage / 100.0))

        messagebox.showinfo("Success", "Prices adjusted!")
        self.populate_items_list()  # Refresh the list

    def adjust_prices(self):
        percentage = simpledialog.askfloat("Adjust Prices", "Enter percentage to adjust prices:")
        if percentage is None:
            return

        for item in self.json_data["Items"]:
            item["MaxPriceThreshold"] = round(item["MaxPriceThreshold"] * (1 + percentage / 100.0))
            item["MinPriceThreshold"] = round(item["MinPriceThreshold"] * (1 + percentage / 100.0))

        messagebox.showinfo("Success", "Prices adjusted!")

        # Ask user where to save the new JSON file
        save_file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if save_file_path:
            try:
                with open(save_file_path, 'w') as json_file:
                    json.dump(self.json_data, json_file, indent=4)
                messagebox.showinfo("Success", "Changes saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving JSON file: {e}")

        self.populate_items_list()  # Refresh the list

    def apply_max_to_min(self):
        for item in self.json_data["Items"]:
            item["MinPriceThreshold"] = item["MaxPriceThreshold"]

        messagebox.showinfo("Success", "Max prices applied to min prices!")
        self.update_output_preview()  # Update preview after applying max to min

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    editor = MarketEditor(root)
    editor.frame.pack(padx=10, pady=10)
    root.mainloop()
