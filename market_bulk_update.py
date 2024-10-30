import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import json
import os

class MarketEditorBulk:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack(fill='both', expand=True)

        self.create_ui()

    def create_ui(self):
        # Create UI for Bulk Update
        self.bulk_update_button = tk.Button(self.frame, text="Bulk Update Prices", command=self.bulk_update_prices)
        self.bulk_update_button.pack(pady=20)

    def bulk_update_prices(self):
        input_directory = filedialog.askdirectory(title="Select Directory Containing JSON Files")
        if not input_directory:
            return

        percentage = simpledialog.askfloat("Bulk Update Prices", "Enter percentage to adjust prices:")
        if percentage is None:
            return

        output_directory = filedialog.askdirectory(title="Select Directory to Save Updated JSON Files")
        if not output_directory:
            return

        success_count = 0
        error_count = 0

        for filename in os.listdir(input_directory):
            if filename.endswith('.json'):
                file_path = os.path.join(input_directory, filename)
                if self.adjust_prices_in_file(file_path, percentage, output_directory):
                    success_count += 1
                else:
                    error_count += 1

        messagebox.showinfo("Bulk Update Complete", f"Successfully updated {success_count} files. Failed to update {error_count} files.")

    def adjust_prices_in_file(self, file_path, percentage, output_directory):
        try:
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)

            # Adjust prices
            for item in json_data.get("Items", []):
                item["MaxPriceThreshold"] = round(item["MaxPriceThreshold"] * (1 + percentage / 100.0))
                item["MinPriceThreshold"] = round(item["MinPriceThreshold"] * (1 + percentage / 100.0))

            # Define new file path in the output directory
            new_file_path = os.path.join(output_directory, os.path.basename(file_path))
            with open(new_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

            return True
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return False
