import json
import os
import time

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

class TerritoryManager():
    def __init__(self):
        self.file_path = "territories.json"
        self.init_file()

    def init_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w+') as f:
                json.dump({}, f)

            quantity = input("How many territories are there?\n")
            self.create_territory_json(quantity)

    def load_data(self):
        with open("territories.json", "r") as territories:
            data = json.load(territories)
        return data

    def dump_data(self, data):
        with open("territories.json", "w") as territories:
            json.dump(data, territories)

    def create_territory_json(self, quantity):
        data = self.load_data()
        for i in range(int(quantity)):
            data.update({i+1: { "isDone": False }})
        self.dump_data(data)

    def complete_territory(self, territory_number):
        data = self.load_data()
        territory = data.get(territory_number)
        if territory:
            data.update({territory_number: {"isDone": True}})
        else:
            print("Sorry that territory doesn't exist.")
            time.sleep(2)
            return
        self.dump_data(data)

    def check_completion(self):
        data = self.load_data()
        completed = 0
        total = 0
        for key in data:
            total += 1
            if data[key]["isDone"]:
                completed += 1
        percent_complete = round(completed / total * 100)
        UIManager().display_progress_bar(percent_complete)


class UIManager():
    def __init__(self):
        self.name = "UIManager"

    def display_progress_bar(self, percent):
        print(f"[{'■' * round(percent / 10)}{'-' * round((100 - percent) / 10)}] {percent}%")

    def handle_options(self):
        clear_screen()
        TerritoryManager().check_completion()
        print("Please choose an option:")
        print("1. Complete a territory")
        print("2. Add a territory")
        choice = input()
        if choice == "1":
            clear_screen()
            territory_number = input("Which territory was completed?\n")
            TerritoryManager().complete_territory(territory_number)
        self.handle_options()

def main():
    territory_manager = TerritoryManager()
    ui_manager = UIManager()
    ui_manager.handle_options()

if __name__ == "__main__":
    main()
