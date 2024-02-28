import tkinter as tk

class ResistorColorCodeApplication(tk.Frame):
    colors = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "gray", "white"]
    
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Resistor Code Finder")
        self.grid()
        
        # Resistor Color Code GUI elements
        self.resistance_label = tk.Label(self, text="Resistance Value (in ohms):")
        self.resistance_label.grid(row=0, column=0)
        
        self.resistance_entry = tk.Entry(self)
        self.resistance_entry.grid(row=0, column=1)
        
        self.generate_button = tk.Button(self, text="Generate Color Code", command=self.generate_color_code)
        self.generate_button.grid(row=1, columnspan=2)
        
        self.color_code_label = tk.Label(self, text="")
        self.color_code_label.grid(row=2, columnspan=2)
        
        # Resistor Color Picker GUI elements
        self.resistor = tk.Canvas(self, width=300, height=100)
        self.resistor.config(bg="white")
        self.resistor.create_rectangle((10, 10, 290, 90), fill="#F3C967")
        self.resistor.grid(row=3, column=0, columnspan=2)

        self.band_labels = ["First band:", "Second band:", "Third band:", "Fourth band:"]
        self.band_canvas = [tk.Canvas(self, width=200, height=50) for _ in range(4)]
        for i, label in enumerate(self.band_labels):
            tk.Label(self, text=label).grid(row=i+4, column=0)
            self.draw_colors(self.band_canvas[i])
            self.band_canvas[i].grid(row=i+4, column=1, columnspan=2)
            self.band_canvas[i].bind("<Button 1>", lambda event, index=i: self.band_clicked(event, index))

        self.band4 = tk.Canvas(self, width=200, height=50)
        self.band4.create_rectangle((0, 0, 100, 50), fill="gold", outline="gold")
        self.band4.create_rectangle((100, 0, 200, 50), fill="gray", outline="gray")
        self.band4.create_text((50, 25), text="+/- 5%")
        self.band4.create_text((150, 25), text="+/- 10%")
        self.band4.grid(row=8, column=1, columnspan=2)
        self.band4.bind("<Button 1>", lambda event: self.band4_clicked(event))

        self.result = tk.Text(self, width=55, height=1)
        self.result.grid(row=9, column=0, columnspan=3)

        self.current_colors = ["orange", "orange", "brown", "gold"]
        self.update()

    def generate_color_code(self):
        resistance = int(self.resistance_entry.get())
        color_bands = self.calculate(resistance)
        self.color_code_label.config(text="Resistor Color Code: " + " -> ".join(color_bands))

    def calculate(self, resistance):
        color_bands = []
        significant_digits = str(resistance)[:2]
        color_bands.extend([ResistorColorCodeApplication.colors[int(digit)] for digit in significant_digits])
        magnitude = len(str(resistance)) - 2
        color_bands.append(ResistorColorCodeApplication.colors[magnitude])
        return color_bands

    def draw_colors(self, canv):
        for i in range(10):
            canv.create_rectangle((20*i, 1, 20+20*i, 50), fill=ResistorColorCodeApplication.colors[i], outline=ResistorColorCodeApplication.colors[i])

    def update(self):
        for i in range(4):
            self.resistor.create_rectangle((60*i+40, 10, 60*i+70, 90), fill=self.current_colors[i])
        resistance_ohms = self.calculate_resistance()
        self.result.delete(0.0, tk.END)
        self.result.insert(tk.END, f"Resistance Value: {resistance_ohms} Ω")

    def band_clicked(self, event, index):
        self.change(index, self.xToc(event.x))

    def band4_clicked(self, event):
        if event.x <= 100:
            self.change(3, "gold")
        else:
            self.change(3, "gray")

    def change(self, band, color):
        self.current_colors[band] = color
        self.update()

    def xToc(self, x):
        return ResistorColorCodeApplication.colors[int(x/20)]

    def calculate_resistance(self):
        val = str(int(ResistorColorCodeApplication.colors.index(self.current_colors[0]))) + \
              str(int(ResistorColorCodeApplication.colors.index(self.current_colors[1])))
        for i in range(int(ResistorColorCodeApplication.colors.index(self.current_colors[2]))):
            val += "0"
        return int(val)

root = tk.Tk()
app = ResistorColorCodeApplication(root)
root.mainloop()
