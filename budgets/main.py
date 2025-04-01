# Started based off of territory progress
import json
import os
import time

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class ExpenseManager():
    def __init__(self):
        self.file_path = "./expenses.json"
        self.init_file()

    def init_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w+') as f:
                json.dump({}, f)

            expense_name = input("Please enter your first expense: ").lower()
            expense_cost = int(input("How much with this expense cost: "))
            self.create_expense(expense_name,expense_cost)

    def load_data(self):
        with open(self.file_path, "r") as expenses:
            data = json.load(expenses)
        return data

    def dump_data(self, data):
        with open(self.file_path, "w") as expenses:
            json.dump(data, expenses)

    def create_expense(self, name: str, cost: float):
        if len(name) > 15:
            clear_screen()
            print("That expense name is too long! Please choose something under 15 characters.")
            time.sleep(3)
            return

        data = self.load_data()
        data.update({name: { "cost": cost, "allocated": 0}})
        self.dump_data(data)

    def allocate_funds(self, expense_name: str, amount: float):
        data = self.load_data()
        expense = data.get(expense_name)
        if expense:
            data[expense_name].update({"allocated": data[expense_name]["allocated"] + amount})
        else:
            print("Sorry that expense doesn't exist.")
            time.sleep(2)
            return
        self.dump_data(data)

    def pay_expense(self, expense_name: str, amount_spent: float):
        data = self.load_data()
        expense = data.get(expense_name)
        if expense:
            data[expense_name].update({"allocated": data[expense_name]["allocated"] - amount_spent})
        else:
            print("Sorry that expense doesn't exist.")
            time.sleep(2)
            return
        self.dump_data(data)

    def check_completion_all(self):
        data = self.load_data()
        completed = 0
        total = 0
        for key in data:
            total += 1
            if data[key]["cost"] <= data[key]["allocated"]:
                completed += 1
        percent_complete = round(completed / total * 100, 2)
        print(UIManager().generate_progress_bar(percent_complete))

    def check_completion_all_individual(self):
        data = self.load_data()
        line_length = 58
        print("-" * line_length + "+")
        print(f"Name{' '* 11} | Cost   | Funds   | Progress{' ' * 13}|")
        print("-" * line_length + "+")
        for key in data:
            percent_complete = round(data[key]["allocated"] / data[key]["cost"] * 100, 2)
            progress_bar = UIManager().generate_progress_bar(percent_complete)
            title_padding = ' ' * (15 - len(key))
            cost_padding = ' ' * (5 - len(str(data[key]['cost'])))
            allocated_fund_padding = ' ' * (6 - len(str(data[key]['allocated'])))
            progress_bar_padding = ' ' * (20 - len(progress_bar))
            print(f"{key.title()}{title_padding} | ${data[key]['cost']}{cost_padding} | ${data[key]['allocated']}{allocated_fund_padding} | {progress_bar}{progress_bar_padding} |")

        print("-" * line_length + "+\n")


class UIManager():
    def __init__(self):
        self.name = "UIManager"
        self.green = "\033[32m"
        self.red = "\033[31m"
        self.default = "\033[0m"

    def generate_progress_bar(self, percent):
        if percent >= 100:
            return f"{self.green}[{'■' * 10}] {percent}%{self.default} "
        elif percent < 0:
            return f"{self.red}[{' ' * 10}] {percent}%{self.default} "
        return(f"[{'■' * round(percent / 10)}{'-' * round((100 - percent) / 10)}] {percent}%")

    def handle_options(self):
        clear_screen()
        ExpenseManager().check_completion_all_individual()
        print("Please choose an option:")
        print("1. Add an expense")
        print("2. Add funds")
        print("3. Pay expense")
        choice = int(input())
        if choice == 1:
            clear_screen()
            ExpenseManager().check_completion_all_individual()
            expense_name = input("What expense would you like to add: ").lower()
            expense_cost = float(input("How much does this expense cost: "))
            ExpenseManager().create_expense(expense_name, expense_cost)
        elif choice == 2:
            clear_screen()
            ExpenseManager().check_completion_all_individual()
            expense_name = input("Which expense would you like to allocate funds to: ").lower()
            allocated_funds = float(input("How much would you like to allocate: "))
            ExpenseManager().allocate_funds(expense_name, allocated_funds)
        elif choice == 3:
            clear_screen()
            ExpenseManager().check_completion_all_individual()
            expense_name = input("Which expense did you pay from: ").lower()
            amount_spent = float(input("How much did you pay: "))
            ExpenseManager().pay_expense(expense_name, amount_spent)
        self.handle_options()

def main():
    expense_manager = ExpenseManager()
    ui_manager = UIManager()
    ui_manager.handle_options()

try:
    while True:
        if __name__ == "__main__":
            main()
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
    # Perform cleanup actions here, if necessary
    print("Exiting...")
