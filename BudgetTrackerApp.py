import tkinter as tk
from tkinter import messagebox
import json
from datetime import datetime


class BudgetTrackerApp:

    def __init__(self, root):

        self.root = root

        self.root.title("BudgetBreeze")
        self.root.config(bg="skyblue")

        self.expenses = []

        self.load_data()

        self.label_product = tk.Label(root, text="Product:", bg="skyblue", width=70)
        self.label_product.pack()

        self.product_entry = tk.Entry(root, width=70)
        self.product_entry.pack()

        self.label_price = tk.Label(root, text="Price:", bg="skyblue", width=70)
        self.label_price.pack()

        self.price_entry = tk.Entry(root, width=70)
        self.price_entry.pack()

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense, bg="skyblue", width=70)
        self.add_button.pack(pady=3)

        self.sum_button = tk.Button(root, text="Calculate Total", command=self.calculate_total, bg="skyblue", width=70)
        self.sum_button.pack(pady=3)

        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_all, bg="skyblue", width=70)
        self.clear_button.pack(pady=3)

        self.remove_button = tk.Button(root, text="Remove Expense", command=self.remove_expense, bg="skyblue", width=70, fg="red")
        self.remove_button.pack(pady=3)

        self.expense_listbox = tk.Listbox(root, width=82, bg="skyblue")
        self.expense_listbox.pack(pady=5)
        self.update_listbox()

        self.root.bind("<Return>", self.add_expense_with_enter)  # Bind Enter key to add_expense_with_enter

        root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle app close

    def add_expense(self):
        product = self.product_entry.get()
        price = self.price_entry.get()

        try:
            price = float(price)
        except ValueError:
            return messagebox.showwarning("Error", "Enter a valid price!")

        if product:
            now = datetime.now()
            formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
            self.expenses.append({"product": product, "price": price, "date": formatted_date})
            self.update_listbox()
            self.save_data()
            self.product_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a valid product.")

    def add_expense_with_enter(self, event):
        self.add_expense()

    def calculate_total(self):
        total = sum(float(expense["price"]) for expense in self.expenses)
        messagebox.showinfo("Total Expenses", f"The total sum of expenses is ${total:.2f}")

    def clear_all(self):
        self.expenses = []
        self.update_listbox()
        self.save_data()

    def remove_expense(self):
        selected_index = self.expense_listbox.curselection()

        if selected_index:
            index = selected_index[0]
            self.expense_listbox.delete(index)
            del self.expenses[index]
            self.update_listbox()
            self.save_data()
        else:
            messagebox.showwarning("Warning", "Please select an expense to remove.")

    def update_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        for expense in self.expenses:
            self.expense_listbox.insert(tk.END, f"Product: {expense['product']}, "
                                                f"Price: {expense['price']}, Date: {expense['date']}")

    def save_data(self):
        with open("../expenses.json", "w") as f:
            json.dump(self.expenses, f)

    def load_data(self):
        try:
            with open("../expenses.json", "r") as f:
                self.expenses = json.load(f)
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_data()
        self.root.destroy()


root = tk.Tk()
app = BudgetTrackerApp(root)
root.mainloop()
