# Started based off of territory progress
# NoAI
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
        if cost != 0:
            data.update({name: { "cost": cost, "allocated": 0.00}})
        else:
            data.update({name: { "allocated": 0.00}})
        self.dump_data(data)

    def remove_expense(self, expense_name: str):
        data = self.load_data()
        clear_screen()
        UIManager().display_confirmation_dialogue()
        if input("Y / N: ").lower() == "y":
            del data[expense_name]
        self.dump_data(data)

    def allocate_funds(self, expense_name: str, amount: float):
        data = self.load_data()
        expense = data.get(expense_name)
        if expense:
            data[expense_name].update({"allocated": round(data[expense_name]["allocated"] + amount,2)})
        else:
            print("Sorry that expense doesn't exist.")
            time.sleep(2)
            return
        self.dump_data(data)

    def pay_expense(self, expense_name: str, amount_spent: float):
        data = self.load_data()
        expense = data.get(expense_name)
        if expense and "cost" in expense:
            data[expense_name].update({"allocated": round(data[expense_name]["allocated"] - amount_spent, 2)})
        else:
            print("Sorry that expense doesn't exist.")
            time.sleep(2)
            return
        self.dump_data(data)

    def check_completion_all(self):
        data = self.load_data()
        total_cost = 0
        total_allocated = 0
        for key in data:
            if not "cost" in data[key]:
                continue
            total_cost += data[key]["cost"]
            total_allocated += data[key]["allocated"]
        percent_complete = round(total_allocated / total_cost * 100, 2)
        progress_bar = UIManager().generate_progress_bar(percent_complete)
        progress_bar_padding = ' ' * (20 - len(str(progress_bar)))
        progress_bar = UIManager().add_progress_color(progress_bar, percent_complete)
        total_allocated = round(total_allocated, 2)
        print(f"{'Total':15} | ${total_cost:<6} | ${total_allocated:<8} | {progress_bar}{progress_bar_padding} |")

    def check_completion_all_individual(self):
        data = self.load_data()
        line_length = 61
        print("-" * line_length + "+")
        print(f"Name{' '* 11} | Cost    | Funds   | Progress{' ' * 13}|")
        print("-" * line_length + "+")
        for key in data:
            title_padding = ' ' * (15 - len(key))
            if not "cost" in data[key]:
                print(f"{key.title():15} | {' ' * 7} | {UIManager().green}${data[key]['allocated']:<8}{UIManager().default} | {' ' * 20} |")
                continue
            percent_complete = round(data[key]["allocated"] / data[key]["cost"] * 100, 2)
            progress_bar = UIManager().generate_progress_bar(percent_complete)
            progress_bar_padding = ' ' * (20 - len(str(progress_bar)))
            progress_bar = UIManager().add_progress_color(progress_bar,percent_complete)
            print(f"{key.title():15} | ${data[key]['cost']:<6} | ${data[key]['allocated']:<6} | {progress_bar}{progress_bar_padding} |")

        print("-" * line_length + "+")
        self.check_completion_all()
        print("-" * line_length + "+\n")

class UIManager():
    def __init__(self):
        self.name = "UIManager"
        self.green = "\033[32m"
        self.red = "\033[31m"
        self.default = "\033[0m"

    def generate_progress_bar(self, percent: float):
        if percent >= 100:
            return f"[{'■' * 10}] {percent}%"
        elif percent < 0:
            return f"[{' ' * 10}] {percent}%"
        return f"[{'■' * round(percent / 10)}{'-' * round((100 - percent) / 10)}] {percent}%"

    def add_progress_color(self, string: str, percent: float):
        if percent >= 100:
            return f"{self.green}{string}{self.default}"
        elif percent < 0:
            return f"{self.red}{string}{self.default}"
        return string

    def display_confirmation_dialogue(self):
        print(f"{self.red}-----------------------------------------------+")
        print("Are you sure you want to delete this expense? |")
        print(f"-----------------------------------------------+ {self.default}")

    def handle_options(self):
        clear_screen()
        ExpenseManager().check_completion_all_individual()
        print("Please choose an option:")
        print("1. Add an expense")
        print("2. Remove an expense")
        print("3. Add funds")
        print("4. Pay expense")
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
            expense_name = input("What expense would you like to remove: ").lower()
            ExpenseManager().remove_expense(expense_name)
        elif choice == 3:
            clear_screen()
            ExpenseManager().check_completion_all_individual()
            expense_name = input("Which expense would you like to allocate funds to: ").lower()
            allocated_funds = float(input("How much would you like to allocate: "))
            ExpenseManager().allocate_funds(expense_name, allocated_funds)
        elif choice == 4:
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
