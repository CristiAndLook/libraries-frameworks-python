import database as db
import helpers
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING

class centerWindowMixin:
    def center(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

class CreateClientWindow(Toplevel, centerWindowMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Client")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (8 ints and 1 upper char)").grid(row=0, column=0)
        dni = Entry(frame)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        dni.grid(row=1, column=0)

        Label(frame, text="Name (between 2 chars and 30)").grid(row=2, column=0)
        name = Entry(frame)
        name.bind("<KeyRelease>", lambda event: self.validate(event ,1))
        name.grid(row=3, column=0)

        Label(frame, text="Last Name (between 2 chars and 30)").grid(row=4, column=0)
        last_name = Entry(frame)
        last_name.bind("<KeyRelease>", lambda event: self.validate(event, 2))
        last_name.grid(row=5, column=0)

        frame_buttons = Frame(self)
        frame_buttons.pack(pady=20)

        add_button = Button(frame_buttons, text="Add", command=self.add)
        add_button.grid(row=0, column=0)
        add_button.config(state=DISABLED)

        Button(frame_buttons, text="Cancel", command=self.close).grid(row=0, column=1)

        self.validations = [0, 0, 0]
        self.add_button = add_button 
        self.dni = dni
        self.name = name
        self.last_name = last_name

    def add(self):
        self.master.treeview.insert(
            parent="", index="end",iid=self.dni.get(), 
            values=(self.dni.get(), self.name.get(), self.last_name.get()))
        db.Clients.add_client(self.dni.get(), self.name.get(), self.last_name.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()
        
    def validate(self, event, index):
        entry = event.widget.get()
        valid = helpers.dni_validate(entry, db.Clients.list_clients) if index == 0 \
            else entry.isalpha() and len(entry) >= 2 and len(entry) <= 30
        event.widget.config(bg="green") if valid else event.widget.config(bg="red")
        self.validations[index] = valid
        self.add_button.config(state=NORMAL if self.validations == [1, 1, 1] else DISABLED)

class EditClientWindow(Toplevel, centerWindowMixin):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Modify Client")
        self.build()
        self.center()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        Label(frame, text="DNI (No edit)").grid(row=0, column=0)
        dni = Entry(frame)
        dni.grid(row=1, column=0)

        Label(frame, text="Name (between 2 chars and 30)").grid(row=2, column=0)
        name = Entry(frame)
        name.bind("<KeyRelease>", lambda event: self.validate(event ,0))
        name.grid(row=3, column=0)

        Label(frame, text="Last Name (between 2 chars and 30)").grid(row=4, column=0)
        last_name = Entry(frame)
        last_name.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        last_name.grid(row=5, column=0)

        client = self.master.treeview.focus()
        camps = self.master.treeview.item(client, "values")
        dni.insert(0, camps[0])
        dni.config(state=DISABLED)
        name.insert(0, camps[1])
        last_name.insert(0, camps[2])


        frame_buttons = Frame(self)
        frame_buttons.pack(pady=20)

        update_button = Button(frame_buttons, text="Modify", command=self.update_client)
        update_button.grid(row=0, column=0)

        Button(frame_buttons, text="Cancel", command=self.close).grid(row=0, column=1)

        self.validations = [1, 1]
        self.update_button = update_button 
        self.dni = dni
        self.name = name
        self.last_name = last_name

    def update_client(self):
        client = self.master.treeview.focus()
        self.master.treeview.item(client, values=(self.dni.get(), self.name.get(), self.last_name.get()))
        db.Clients.modify_client(self.dni.get(), self.name.get(), self.last_name.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()
        
    def validate(self, event, index):
        entry = event.widget.get()
        valid = entry.isalpha() and len(entry) >= 2 and len(entry) <= 30
        event.widget.config(bg="green") if valid else event.widget.config(bg="red")
        self.validations[index] = valid
        self.update_button.config(state=NORMAL if self.validations == [1, 1] else DISABLED)

class MainWindow(Tk, centerWindowMixin):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Clientes")
        self.build()
        self.center()

    def build(self):
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame, columns=("DNI", "Name", "Last Name"))
        treeview.heading("#0", text="ID")
        treeview.heading("DNI", text="DNI")
        treeview.heading("Name", text="Name")
        treeview.heading("Last Name", text="Last Name")
        treeview.column("#0", width=0, stretch=NO)

        scrollbar = Scrollbar(frame, orient="vertical", command=treeview.yview)
        scrollbar.pack(side="right", fill="y")
        treeview.configure(yscrollcommand=scrollbar.set)

        clients = db.Clients.list_clients
        for client in clients:
            treeview.insert(parent="", index="end",iid=client.dni, values=(client.dni, client.name, client.last_name))

        treeview.pack()

        buttons_frame = Frame(self)

        Button(buttons_frame, text="Add", command=self.add_client).grid(row=0, column=0)
        Button(buttons_frame, text="Modify", command=self.modify_client).grid(row=0, column=1)
        Button(buttons_frame, text="Delete", command=self.delete).grid(row=0, column=2)

        buttons_frame.pack(pady=20)

        self.treeview = treeview

    def delete(self):
        client = self.treeview.focus()
        if client: 
            camps = self.treeview.item(client, "values")
            comfirm = askokcancel(
                title="Are you sure you want to delete this client?",
                message=f'¿Are you sure you want to delete the client with DNI {camps[0]}, {camps[1], camps[2]}?',
                icon=WARNING
            )
            if comfirm:
                self.treeview.delete(client)
                db.Clients.delete_client(camps[0])
    
    def add_client(self):
        CreateClientWindow(self)
    
    def modify_client(self):
        if self.treeview.focus():
            EditClientWindow(self)

    
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()