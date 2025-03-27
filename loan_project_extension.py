import tkinter as tk
from tkinter import messagebox
import numpy as np
from typing import Any
import matplotlib.pyplot as plt


def calculate_monthly_payment(principal: float, monthly_interest_rate: float, number_of_payments: int) -> float:    
    return ( principal * monthly_interest_rate ) / ( 1 - (1 + monthly_interest_rate) ** (-number_of_payments) )


def calculate_loan_values(loan: dict[str, Any]):
    principal = loan['Principal']
    apr = loan['APR']
    months = loan['Months']
    monthly_interest_rate = apr / 100 / 12

    monthly_payment = calculate_monthly_payment(principal, monthly_interest_rate, months)
    loan_values = np.zeros(months)

    remaining_balance = principal
    for i in range(months):
        interest = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest
        remaining_balance -= principal_payment
        loan_values[i] = max(remaining_balance, 0)

    return loan_values

def plot_graph(loans: list[dict[str, Any]]):
    loan_values_list = []
    max_length = 0

    for loan in loans:
        loan_values = calculate_loan_values(loan)
        loan_values_list.append(loan_values)
        max_length = max(max_length, len(loan_values))

    padded_loan_values_list = [
        np.pad(loan_values, (0, max_length - len(loan_values)), constant_values=0.0)
        for loan_values in loan_values_list
    ]

    plt.figure(figsize=(10, 6))
    for i, loan_values in enumerate(padded_loan_values_list):
        plt.plot(loan_values, label=f"Loan {i + 1}")

    plt.title("Loan Balance Over Time")
    plt.xlabel("Months")
    plt.ylabel("Remaining Balance")
    plt.legend()
    plt.grid(True)
    plt.show()


class LoanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Comparison")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Loan Comparison", font=("Arial", 16)).grid(row=0, column=0, columnspan=4, pady=10)

        # Loan 1
        tk.Label(self.root, text="Loan 1").grid(row=1, column=0, pady=5)
        self.principal1 = self.create_placeholder_entry("Principal", 1, 1)
        self.apr1 = self.create_placeholder_entry("APR", 1, 2)
        self.months1 = self.create_placeholder_entry("Number of Months", 1, 3)

        # Loan 2
        tk.Label(self.root, text="Loan 2").grid(row=2, column=0, pady=5)
        self.principal2 = self.create_placeholder_entry("Principal", 2, 1)
        self.apr2 = self.create_placeholder_entry("APR", 2, 2)
        self.months2 = self.create_placeholder_entry("Number of Months", 2, 3)

        # Plot Button
        self.plot_button = tk.Button(self.root, text="Plot Graph", bg="lightgreen", command=self.on_plot)
        self.plot_button.grid(row=3, column=1, columnspan=2, pady=10)

    def create_placeholder_entry(self, placeholder, row, column):
        entry = tk.Entry(self.root, fg='gray')
        entry.insert(0, placeholder)

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='black')

        def on_focus_out(event):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(fg='gray')

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        entry.grid(row=row, column=column, padx=5)
        return entry

    def on_plot(self):
        try:
            loans_data = [
                {
                    'Principal': float(self.get_value(self.principal1, "Principal")),
                    'APR': float(self.get_value(self.apr1, "APR")),
                    'Months': int(self.get_value(self.months1, "Number of Months"))
                },
                {
                    'Principal': float(self.get_value(self.principal2, "Principal")),
                    'APR': float(self.get_value(self.apr2, "APR")),
                    'Months': int(self.get_value(self.months2, "Number of Months"))
                }
            ]
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        plot_graph(loans_data)

    def get_value(self, entry, placeholder):
        value = entry.get()
        if value == placeholder or value == '':
            raise ValueError("Invalid input")
        return value

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanApp(root)
    root.mainloop()
