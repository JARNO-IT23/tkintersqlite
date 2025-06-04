import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT, last_name TEXT,
                email TEXT, phone TEXT, image TEXT)""")
conn.commit()

def refresh():
    tree.delete(*tree.get_children())
    cur.execute("SELECT * FROM users")
    for row in cur.fetchall():
        tree.insert("", "end", values=row)

def add():
    if not all([e1.get(), e2.get(), e3.get(), e4.get()]):
        messagebox.showwarning("Error", "Please fill all required fields")
        return
    cur.execute("INSERT INTO users VALUES (NULL,?,?,?,?,?)", 
                (e1.get(), e2.get(), e3.get(), e4.get(), e5.get()))
    conn.commit()
    refresh()

def delete():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select a record")
        return
    cur.execute("DELETE FROM users WHERE id=?", (tree.item(selected[0])['values'][0],))
    conn.commit()
    refresh()

def update():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Please select a record")
        return
    cur.execute("""UPDATE users SET first_name=?, last_name=?, 
                email=?, phone=?, image=? WHERE id=?""",
                (e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), 
                 tree.item(selected[0])['values'][0]))
    conn.commit()
    refresh()

def search():
    query = search_entry.get()
    tree.delete(*tree.get_children())
    cur.execute("SELECT * FROM users WHERE first_name LIKE ? OR last_name LIKE ?", 
                (f"%{query}%", f"%{query}%"))
    for row in cur.fetchall():
        tree.insert("", "end", values=row)

root = tk.Tk()
root.title("User Database")
root.geometry("800x500")

fields = ["First Name", "Last Name", "Email", "Phone", "Image"]
entries = []
for i, field in enumerate(fields):
    tk.Label(root, text=field).grid(row=i, column=0, padx=5, pady=5)
    entry = tk.Entry(root, width=30)
    entry.grid(row=i, column=1, padx=5, pady=5)
    entries.append(entry)
e1, e2, e3, e4, e5 = entries

tk.Button(root, text="Add", command=add).grid(row=5, column=0, pady=10)
tk.Button(root, text="Update", command=update).grid(row=5, column=1)
tk.Button(root, text="Delete", command=delete).grid(row=5, column=2)

tk.Label(root, text="Search:").grid(row=6, column=0)
search_entry = tk.Entry(root, width=30)
search_entry.grid(row=6, column=1)
tk.Button(root, text="Search", command=search).grid(row=6, column=2)

tree = ttk.Treeview(root, columns=("ID", *fields[:-1]), show="headings", height=10)
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

scroll = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
scroll.grid(row=7, column=3, sticky="ns")

refresh()
root.mainloop()
