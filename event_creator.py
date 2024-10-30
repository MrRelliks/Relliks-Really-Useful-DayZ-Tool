import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import xml.etree.ElementTree as ET

class EventCreator:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(master)
        self.frame.pack(fill='both', expand=True)

        self.event_type = tk.StringVar()
        self.event_suffix = tk.StringVar()  # Suffix for the event name
        self.nominal = tk.IntVar()
        self.min_value = tk.IntVar()
        self.max_value = tk.IntVar()
        self.children = []

        self.create_widgets()

    def create_widgets(self):
        # Event type selection
        ttk.Label(self.frame, text="Select Event Type:").grid(row=0, column=0)
        self.event_type_combobox = ttk.Combobox(self.frame, textvariable=self.event_type, 
                                                 values=["Vehicle", "Animal", "Mission"])
        self.event_type_combobox.grid(row=0, column=1)

        # Event suffix input
        ttk.Label(self.frame, text="Event Name:").grid(row=1, column=0)
        ttk.Entry(self.frame, textvariable=self.event_suffix).grid(row=1, column=1)

        # Nominal value
        ttk.Label(self.frame, text="Nominal Value:").grid(row=2, column=0)
        ttk.Entry(self.frame, textvariable=self.nominal).grid(row=2, column=1)

        # Min and Max values
        ttk.Label(self.frame, text="Min Value:").grid(row=3, column=0)
        ttk.Entry(self.frame, textvariable=self.min_value).grid(row=3, column=1)

        ttk.Label(self.frame, text="Max Value:").grid(row=4, column=0)
        ttk.Entry(self.frame, textvariable=self.max_value).grid(row=4, column=1)

        # Child Definitions
        self.child_frame = ttk.LabelFrame(self.frame, text="Children")
        self.child_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky='ew')

        self.child_type = tk.StringVar()
        self.child_min = tk.IntVar()
        self.child_max = tk.IntVar()

        self.create_child_widgets()

        ttk.Button(self.frame, text="Add Child", command=self.add_child).grid(row=6, column=0, sticky='ew')
        ttk.Button(self.frame, text="Generate XML", command=self.generate_xml).grid(row=6, column=1, sticky='ew')

        # Save Directory
        ttk.Label(self.frame, text="Save Directory:").grid(row=7, column=0)
        self.save_directory = tk.StringVar()
        ttk.Entry(self.frame, textvariable=self.save_directory).grid(row=7, column=1)
        ttk.Button(self.frame, text="Browse", command=self.browse_directory).grid(row=7, column=2)

    def create_child_widgets(self):
        # Child Type
        ttk.Label(self.child_frame, text="Child Type:").grid(row=0, column=0)
        ttk.Entry(self.child_frame, textvariable=self.child_type).grid(row=0, column=1)

        # Child Min and Max values
        ttk.Label(self.child_frame, text="Min:").grid(row=1, column=0)
        ttk.Entry(self.child_frame, textvariable=self.child_min).grid(row=1, column=1)

        ttk.Label(self.child_frame, text="Max:").grid(row=2, column=0)
        ttk.Entry(self.child_frame, textvariable=self.child_max).grid(row=2, column=1)

    def add_child(self):
        child_info = {
            'type': self.child_type.get(),
            'min': self.child_min.get(),
            'max': self.child_max.get()
        }
        self.children.append(child_info)
        self.child_type.set('')
        self.child_min.set(0)
        self.child_max.set(1)

    def generate_xml(self):
        event_suffix = self.event_suffix.get().strip()  # Get the event suffix from user input
        event_type = self.event_type.get()

        # Validate the event suffix
        if not event_suffix:
            messagebox.showwarning("Warning", "Event suffix cannot be empty!")
            return

        # Construct the event name based on the event type
        if event_type == "Vehicle":
            event_name = f"Vehicle{event_suffix}"
        elif event_type == "Animal":
            event_name = f"Animal{event_suffix}"
        elif event_type == "Mission":
            event_name = f"Static{event_suffix}"
        else:
            messagebox.showerror("Error", "Invalid event type selected.")
            return

        events_elem = ET.Element("events")
        event_elem = ET.SubElement(events_elem, "event", name=event_name)

        for field, value in [('nominal', self.nominal.get()), 
                             ('min', self.min_value.get()), 
                             ('max', self.max_value.get()), 
                             ('lifetime', '300'), 
                             ('restock', '0'), 
                             ('saferadius', '500'), 
                             ('distanceradius', '500'), 
                             ('cleanupradius', '200'), 
                             ('active', '1')]:
            ET.SubElement(event_elem, field).text = str(value)

        flags_elem = ET.SubElement(event_elem, "flags", deletable="0", init_random="0", remove_damaged="1")
        ET.SubElement(event_elem, "position").text = "fixed"
        ET.SubElement(event_elem, "limit").text = "mixed"

        children_elem = ET.SubElement(event_elem, "children")
        for child in self.children:
            ET.SubElement(children_elem, "child", 
                          lootmax="0", 
                          lootmin="0", 
                          max=str(child['max']), 
                          min=str(child['min']), 
                          type=child['type'])

        # Create events.xml
        self.save_xml(events_elem, "events.xml")

        # Create cfgeventspawns.xml
        self.create_event_spawns_xml(event_name)

    def create_event_spawns_xml(self, event_name):
        cfgeventspawns_elem = ET.Element("eventposdef")
        event_elem = ET.SubElement(cfgeventspawns_elem, "event", name=event_name)

        # Here you would gather positions, for now, we will use sample positions.
        sample_positions = [(6719.09, 5988.08), (4971.89, 9055.77)]
        for x, z in sample_positions:
            ET.SubElement(event_elem, "pos", x=str(x), z=str(z), a="0")

        self.save_xml(cfgeventspawns_elem, "cfgeventspawns.xml")

    def save_xml(self, elem, filename):
        directory = self.save_directory.get()
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)
        tree = ET.ElementTree(elem)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        messagebox.showinfo("Success", f"{filename} saved successfully!")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory.set(directory)
