import tkinter as tk
from tkinter import ttk, messagebox

class UnitConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Unit Converter")
        self.root.geometry("520x480")
        self.root.configure(bg="#ecf9f1")
        self.root.resizable(False, False)

        # Style settings
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background="#ecf9f1")
        self.style.configure("TLabel", background="#ecf9f1", font=("Calibri", 12))
        self.style.configure("Header.TLabel", font=("Calibri", 20, "bold"), foreground="#004d40", background="#ecf9f1")
        self.style.configure("TButton", font=("Calibri", 12, "bold"), background="#26a69a", foreground="white", padding=6)
        self.style.map("TButton",
                       background=[("active", "#00796b")],
                       foreground=[("active", "white")])
        self.style.configure("TCombobox", font=("Calibri", 12), padding=4)
        self.style.configure("TEntry", font=("Calibri", 12))

        # Frame
        self.main_frame = ttk.Frame(root, padding="25 15 25 15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Unit Converter", style="Header.TLabel")
        self.title_label.pack(pady=(0, 25))

        # Conversion Type Dropdown
        self.conversion_type = tk.StringVar(value="Temperature")
        self.type_menu = ttk.Combobox(
            self.main_frame,
            textvariable=self.conversion_type,
            values=["Temperature", "Weight", "Length", "Volume"],
            state="readonly",
            width=20
        )
        self.type_menu.pack(pady=10)
        self.type_menu.bind("<<ComboboxSelected>>", self.update_units)

        # Input area
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(pady=25)

        self.input_value = tk.DoubleVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_value, width=12)
        self.input_entry.grid(row=0, column=0, padx=8)

        self.from_unit = tk.StringVar()
        self.from_menu = ttk.Combobox(self.input_frame, textvariable=self.from_unit, state="readonly", width=10)
        self.from_menu.grid(row=0, column=1, padx=8)

        self.to_unit = tk.StringVar()
        self.to_menu = ttk.Combobox(self.input_frame, textvariable=self.to_unit, state="readonly", width=10)
        self.to_menu.grid(row=0, column=2, padx=8)

        # Convert button
        self.convert_button = ttk.Button(self.main_frame, text="Convert", command=self.convert)
        self.convert_button.pack(pady=10)

        # Result display
        self.result_label = ttk.Label(self.main_frame, text="", font=("Calibri", 14, "bold"), foreground="#00695c")
        self.result_label.pack(pady=15)

        # Footer
        self.footer_label = ttk.Label(self.main_frame, text="Made with Python & Tkinter", font=("Calibri", 10), foreground="#555")
        self.footer_label.pack(pady=(30, 0))

        # Set initial units
        self.update_units()

    def update_units(self, event=None):
        units_map = {
            "Temperature": ["°C", "°F", "K"],
            "Weight": ["kg", "lbs", "oz"],
            "Length": ["m", "km", "miles", "ft"],
            "Volume": ["L", "gal", "mL"]
        }

        units = units_map.get(self.conversion_type.get(), [])
        self.from_menu["values"] = units
        self.to_menu["values"] = units
        if units:
            self.from_unit.set(units[0])
            self.to_unit.set(units[1])

    def convert(self):
        try:
            value = float(self.input_value.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            conversion_type = self.conversion_type.get()

            result = self.perform_conversion(value, from_unit, to_unit, conversion_type)
            if result is not None:
                self.result_label.config(
                    text=f"{value:.2f} {from_unit} = {result:.2f} {to_unit}")
            else:
                self.result_label.config(text="Invalid conversion!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def perform_conversion(self, value, from_unit, to_unit, conversion_type):
        if from_unit == to_unit:
            return value

        if conversion_type == "Temperature":
            return self.convert_temperature(value, from_unit, to_unit)
        elif conversion_type == "Weight":
            return self.convert_weight(value, from_unit, to_unit)
        elif conversion_type == "Length":
            return self.convert_length(value, from_unit, to_unit)
        elif conversion_type == "Volume":
            return self.convert_volume(value, from_unit, to_unit)

    def convert_temperature(self, value, from_unit, to_unit):
        if from_unit == "°C":
            return (value * 9/5 + 32) if to_unit == "°F" else value + 273.15 if to_unit == "K" else value
        elif from_unit == "°F":
            return (value - 32) * 5/9 if to_unit == "°C" else (value - 32) * 5/9 + 273.15 if to_unit == "K" else value
        elif from_unit == "K":
            return value - 273.15 if to_unit == "°C" else (value - 273.15) * 9/5 + 32 if to_unit == "°F" else value

    def convert_weight(self, value, from_unit, to_unit):
        conversions = {
            "kg": {"lbs": value * 2.20462, "oz": value * 35.274},
            "lbs": {"kg": value / 2.20462, "oz": value * 16},
            "oz": {"kg": value / 35.274, "lbs": value / 16}
        }
        return conversions.get(from_unit, {}).get(to_unit)

    def convert_length(self, value, from_unit, to_unit):
        conversions = {
            "m": {"km": value / 1000, "miles": value / 1609.34, "ft": value * 3.28084},
            "km": {"m": value * 1000, "miles": value / 1.60934, "ft": value * 3280.84},
            "miles": {"m": value * 1609.34, "km": value * 1.60934, "ft": value * 5280},
            "ft": {"m": value / 3.28084, "km": value / 3280.84, "miles": value / 5280}
        }
        return conversions.get(from_unit, {}).get(to_unit)

    def convert_volume(self, value, from_unit, to_unit):
        conversions = {
            "L": {"gal": value / 3.78541, "mL": value * 1000},
            "gal": {"L": value * 3.78541, "mL": value * 3785.41},
            "mL": {"L": value / 1000, "gal": value / 3785.41}
        }
        return conversions.get(from_unit, {}).get(to_unit)

if __name__ == "__main__":
    root = tk.Tk()
    app = UnitConverterApp(root)
    root.mainloop()
