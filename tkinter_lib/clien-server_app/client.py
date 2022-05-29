import tkinter as tk
from tkinter import ttk, colorchooser, messagebox


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Client")
        self.geometry('1200x500')
        self.minsize(1200, 500)

        # =========
        # LEFT PART
        # =========

        # table of functions
        heads = ["ID", "Function", "Line thickness", "Line color", "Line type", "Grid", "From", "To"]
        self.func_table = ttk.Treeview(self, columns=heads, show="headings")

        for header in heads:
            self.func_table.heading(header, text=header, anchor="center")
            self.func_table.column(header, width=1, anchor="center")

        self.func_table.place(relx=0.01, relheight=0.9, relwidth=0.7)
        self.id = 1  # id for functions in the table
        self.functions = dict()  # contains all the functions (class) in the table

        # buttons under the table
        self.btn_save = ttk.Button(self, text="Save graph to file", command=self.save_graph)
        self.btn_save.place(relx=0.06, rely=0.91, relwidth=0.1, relheight=0.08)

        self.btn_save = ttk.Button(self, text="Get graph", command=self.get_graph)
        self.btn_save.place(relx=0.31, rely=0.91, relwidth=0.1, relheight=0.08)

        self.btn_save = ttk.Button(self, text="Delete", command=self.del_func_from_table)
        self.btn_save.place(relx=0.56, rely=0.91, relwidth=0.1, relheight=0.08)

        # ==========
        # RIGHT PART
        # ==========

        # IP input field
        tk.Label(self, text="IP").place(relx=0.72, relheight=0.05)

        self.ip_var = tk.StringVar()
        self.ip_input = ttk.Entry(self, textvariable=self.ip_var)
        self.ip_input.place(relx=0.72, rely=0.05, relwidth=0.27, relheight=0.04)

        # port input field
        tk.Label(self, text="Port").place(relx=0.72, rely=0.12, relheight=0.05)

        self.port_var = tk.StringVar()
        self.port_input = ttk.Entry(self, textvariable=self.port_var)
        self.port_input.place(relx=0.72, rely=0.17, relwidth=0.27, relheight=0.04)

        # function input field
        tk.Label(self, text="Function").place(relx=0.72, rely=0.24, relheight=0.05)

        tk.Label(self, text="f(x) = ").place(relx=0.72, rely=0.29, relheight=0.04)
        self.func_var = tk.StringVar()
        self.func_input = ttk.Entry(self, textvariable=self.func_var)
        self.func_input.place(relx=0.75, rely=0.29, relwidth=0.24, relheight=0.04)

        # segment input field
        tk.Label(self, text="Construct a function on a segment").place(relx=0.72, rely=0.36, relheight=0.05)

        tk.Label(self, text="from").place(relx=0.72, rely=0.42, relwidth=0.03, relheight=0.04)
        self.from_var = tk.StringVar()
        self.from_input = ttk.Entry(self, textvariable=self.from_var)
        self.from_input.place(relx=0.75, rely=0.42, relwidth=0.1, relheight=0.04)

        tk.Label(self, text="to").place(relx=0.86, rely=0.42, relwidth=0.03, relheight=0.04)
        self.to_var = tk.StringVar()
        self.to_input = ttk.Entry(self, textvariable=self.to_var)
        self.to_input.place(relx=0.89, rely=0.42, relwidth=0.1, relheight=0.04)

        # graph grid choice
        self.grid_var = tk.BooleanVar()
        self.grid_checkbtn = ttk.Checkbutton(self, text='Graph grid', variable=self.grid_var)
        self.grid_checkbtn.place(relx=0.72, rely=0.49, relwidth=0.1, relheight=0.04)

        # line width scale
        tk.Label(self, text="Line thickness").place(relx=0.72, rely=0.56, relheight=0.05)

        self.lwidth_scale = ttk.Scale(self, from_=1, to=10, command=self.scale_label)
        self.lwidth_scale.place(relx=0.72, rely=0.62, relwidth=0.2, relheight=0.04)

        self.scale_var = tk.IntVar()  # this label shows number on the scale
        self.scale_var.set(1)  # default value
        ttk.Label(self, text=0, textvariable=self.scale_var).place(relx=0.93, rely=0.62, relwidth=0.07, relheight=0.04)

        # line type choice
        tk.Label(self, text="Line type").place(relx=0.72, rely=0.69, relheight=0.05)

        self.lrype_var = tk.StringVar()
        self.lrype_var.set("-")

        ttk.Radiobutton(self, text="-", variable=self.lrype_var, value="-").place(relx=0.72, rely=0.74)
        ttk.Radiobutton(self, text="-.-", variable=self.lrype_var, value="-.-").place(relx=0.82, rely=0.74)
        ttk.Radiobutton(self, text="--", variable=self.lrype_var, value="--").place(relx=0.92, rely=0.74)

        # right buttons
        self.btn_color = ttk.Button(self, text="Color", command=self.choose_color)
        self.btn_color.place(relx=0.74, rely=0.91, relwidth=0.1, relheight=0.08)
        self.line_color = "black"  # default line color

        self.btn_add = ttk.Button(self, text="Add function", command=self.add_func_to_table)
        self.btn_add.place(relx=0.88, rely=0.91, relwidth=0.1, relheight=0.08)

    def save_graph(self):
        pass

    def get_graph(self):
        pass

    def del_func_from_table(self):
        selection = self.func_table.selection()
        for index in selection[::-1]:
            self.functions.pop(index)
            self.func_table.delete(index)

    def scale_label(self, value):
        value = int(float(value))
        self.scale_var.set(value)

    def choose_color(self):
        color_code = tk.colorchooser.askcolor(title="Choose color:")
        self.line_color = color_code[1]

    def add_func_to_table(self):
        try:
            # need to process invalid input
            func_data = [self.id,
                         self.func_var.get(),
                         self.scale_var.get(),
                         self.line_color,
                         self.lrype_var.get(),
                         self.grid_var.get(),
                         self.from_var.get(),
                         self.to_var.get()
                         ]
            self.functions[self.func_table.insert(parent="", index=tk.END, values=func_data, iid=str(self.id))] = \
                Function(*func_data[1:])
            self.id += 1
        except Exception:
            messagebox.showerror("Error", "Invalid input")


class Function:
    def __init__(self, function, lwidth, lcolor, ltype, grid, from_, to):
        self.function, self.lwidth, self.lcolor, self.ltype = function, lwidth, lcolor, ltype
        self.from_, self.to, self.rborder = grid, from_, to


if __name__ == '__main__':
    app = App()
    app.mainloop()
