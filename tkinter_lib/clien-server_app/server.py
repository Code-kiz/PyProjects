import tkinter as tk
from tkinter import ttk, messagebox
import socket
import pickle
from client import Function
import matplotlib.pyplot as plt
import numpy
import numexpr as ne
import os


class ServerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Server")
        self.geometry('300x400')
        self.minsize(300, 400)

        # server control buttons
        self.start_btn = ttk.Button(self, text="Start the server", command=self.start_server)
        self.start_btn.place(relx=0.01, rely=0.02, relwidth=0.98, relheight=0.1)

        self.stop_btn = ttk.Button(self, text="Stop the server", command=self.stop_server)
        self.stop_btn.place(relx=0.01, rely=0.14, relwidth=0.98, relheight=0.1)

        # input address to ban
        tk.Label(self, text="IP for ban").place(relx=0.01, rely=0.3, relheight=0.05)

        self.ip_var = tk.StringVar()
        self.ip_input = ttk.Entry(self, textvariable=self.ip_var)
        self.ip_input.place(relx=0.01, rely=0.35, relwidth=0.98, relheight=0.05)

        # add button
        self.add_ip_btn = ttk.Button(self, text="Add", command=self.add_address)
        self.add_ip_btn.place(relx=0.01, rely=0.41, relwidth=0.98, relheight=0.08)

        # table of ip addresses
        heads = ["ID", "IP address"]
        self.ip_table = ttk.Treeview(self, columns=heads, show="headings")

        for header in heads:
            self.ip_table.heading(header, text=header, anchor="center")
            self.ip_table.column(header, width=1, anchor="center")

        self.ip_table.place(relx=0.01, rely=0.54, relheight=0.35, relwidth=0.98)
        self.id = 1  # id for addresses in the table

        # del button
        self.add_ip_btn = ttk.Button(self, text="Delete", command=self.del_address)
        self.add_ip_btn.place(relx=0.01, rely=0.9, relwidth=0.98, relheight=0.08)

    def start_server(self):
        # start server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 2000))
        server.listen(4)

        for _ in range(4):
            # connect to client
            client_socket, client_address = server.accept()

            if str(client_address) in self.ip_table:
                print("Banned ip")
                continue

            # get function information from client
            data = client_socket.recv(2048)
            function = pickle.loads(data)  # convert information to a Function object

            # give information to build a graph
            self.plot_func(function)

            # open plot image after plot_func, read and send it
            file = open("plot.jpg", mode="rb")

            data = file.read(2048)
            while data:
                client_socket.send(data)
                data = file.read(2048)

            file.close()
            client_socket.close()  # disconnect

            # delete plot after sending
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "plot.jpg")
            os.remove(path)

    @staticmethod
    def plot_func(function: Function):
        # configure graph
        plt.title("Graph of the function y = " + function.expression)
        plt.xlabel("x")
        plt.ylabel("y")
        x = numpy.arange(float(function.from_), float(function.to), 0.1)

        # plot graph
        if function.grid:
            plt.grid()

        plt.plot(x, ne.evaluate(function.expression),
                 color=function.lcolor,
                 linestyle=function.ltype,
                 linewidth=function.lwidth)

        plt.savefig("plot.jpg")
        fig, ax = plt.subplots()
        fig.clear(True)

    def stop_server(self):
        pass

    def add_address(self):
        address = self.ip_var.get()
        # if ip is correct, add it to the table
        if len(address.split(".")) == 4:
            self.ip_var.set("")  # clear entry
            lst = [str(self.id), address]

            self.ip_table.insert(parent="", index=tk.END, values=lst, iid=str(self.id))
            self.id += 1
        else:
            messagebox.showerror("Error", "Wrong IP address!")

    def del_address(self):
        indexes = self.ip_table.selection()
        for index in indexes:
            self.ip_table.delete(index)


if __name__ == '__main__':
    app = ServerApp()
    app.mainloop()

